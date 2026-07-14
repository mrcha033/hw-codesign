from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from hw_codesign.jobs import JobManager, ProjectWriterLock
from hw_codesign.service import HardwareService


def _wait(manager: JobManager, job_id: str, timeout: float = 20.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = manager.status(job_id)
        if status["status"] in {"complete", "failed", "cancelled"}:
            return status
        time.sleep(0.05)
    raise AssertionError(f"job {job_id} did not finish")


def test_isolated_job_promotes_complete_project_atomically(tmp_path: Path):
    service = HardwareService(tmp_path)
    service.create_project("job_project", template="sensor_data_logger")
    manager = JobManager(tmp_path)

    submitted = manager.submit("hw_generate_electronics_source", {"project": "job_project"})
    status = _wait(manager, submitted["job_id"])

    assert status["status"] == "complete"
    assert status["result"]["status"] == "generated"
    assert status["committed"] is True
    assert status["pid"] > 0
    assert status["pgid"] == status["pid"]
    assert not (tmp_path / ".hw-runtime" / "locks" / "job_project.lock").exists()
    assert (tmp_path / "projects" / "job_project" / "project.yaml").is_file()
    assert not (tmp_path / ".hw-runtime" / "jobs" / submitted["job_id"] / "previous-project").exists()

    schema = json.loads((Path(__file__).parents[1] / "schemas" / "job_status.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(status)) == []


def test_blocked_job_does_not_promote_partial_workspace(tmp_path: Path):
    service = HardwareService(tmp_path)
    service.create_project("blocked_project", template="sensor_data_logger")
    manager = JobManager(tmp_path)

    submitted = manager.submit("hw_generate_firmware", {"project": "blocked_project"})
    status = _wait(manager, submitted["job_id"])

    assert status["status"] == "failed"
    assert status["result"]["status"] == "blocked"
    assert status["committed"] is False
    assert status["error"]["code"] == "operation_not_committed"
    assert not (tmp_path / "projects" / "blocked_project" / "firmware" / "generated" / "pinmap.json").exists()


def test_failed_job_leaves_original_project_unchanged(tmp_path: Path):
    service = HardwareService(tmp_path)
    service.create_project("rollback_project", template="sensor_data_logger")
    project_file = tmp_path / "projects" / "rollback_project" / "project.yaml"
    original = project_file.read_bytes()
    (tmp_path / "projects" / "rollback_project" / "spec" / "system.yaml").write_text("compute: [invalid\n", encoding="utf-8")
    corrupt = (tmp_path / "projects" / "rollback_project" / "spec" / "system.yaml").read_bytes()
    manager = JobManager(tmp_path)

    submitted = manager.submit("hw_generate_all", {"project": "rollback_project"})
    status = _wait(manager, submitted["job_id"])

    assert status["status"] == "failed"
    assert status["error"]["code"] == "job_execution_failed"
    assert project_file.read_bytes() == original
    assert (tmp_path / "projects" / "rollback_project" / "spec" / "system.yaml").read_bytes() == corrupt


def test_project_writer_lock_rejects_second_live_writer(tmp_path: Path):
    runtime = tmp_path / ".hw-runtime"
    with ProjectWriterLock(runtime, "locked_project", "first", timeout_seconds=0.1):
        with pytest.raises(TimeoutError):
            ProjectWriterLock(runtime, "locked_project", "second", timeout_seconds=0.1).acquire()


def test_cancel_terminates_worker_process_group(tmp_path: Path):
    if os.name == "nt":
        pytest.skip("POSIX process-group assertion")
    manager = JobManager(tmp_path)
    job_id = "a" * 32
    job_dir = manager.jobs_root / job_id
    job_dir.mkdir(parents=True)
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); time.sleep(60)",
        ],
        start_new_session=True,
    )
    metadata = {
        "job_id": job_id,
        "tool": "hw_generate_all",
        "arguments": {"project": "cancel_project"},
        "project": "cancel_project",
        "status": "running",
        "pid": process.pid,
        "pgid": process.pid,
        "gate_events": [],
        "result": None,
        "error": None,
    }
    (job_dir / "job.json").write_text(json.dumps(metadata), encoding="utf-8")

    status = manager.cancel(job_id, grace_seconds=0.5)
    process.wait(timeout=5)

    assert status["status"] == "cancelled"
    assert status["error"]["code"] == "job_cancelled"
    with pytest.raises(ProcessLookupError):
        os.killpg(process.pid, 0)


def test_recover_orphans_marks_job_failed_and_reclaims_lock(tmp_path: Path):
    manager = JobManager(tmp_path)
    job_id = "b" * 32
    job_dir = manager.jobs_root / job_id
    job_dir.mkdir(parents=True)
    metadata = {
        "job_id": job_id,
        "project": "orphan_project",
        "status": "running",
        "pid": 99999999,
        "pgid": 99999999,
        "gate_events": [],
        "result": None,
    }
    (job_dir / "job.json").write_text(json.dumps(metadata), encoding="utf-8")
    lock = manager.runtime_root / "locks" / "orphan_project.lock"
    lock.parent.mkdir(parents=True)
    lock.write_text(json.dumps({"job_id": job_id, "pid": 99999999}), encoding="utf-8")

    result = manager.recover_orphans()

    assert job_id in result["recovered_jobs"]
    assert manager.status(job_id)["status"] == "failed"
    assert not lock.exists()


def test_recovery_does_not_claim_a_fresh_queued_job_or_partial_lock(tmp_path: Path):
    manager = JobManager(tmp_path)
    job_id = "c" * 32
    job_dir = manager.jobs_root / job_id
    job_dir.mkdir(parents=True)
    metadata = {
        "job_id": job_id,
        "project": "starting_project",
        "status": "queued",
        "submitted_at": "2999-01-01T00:00:00+00:00",
        "pid": None,
        "pgid": None,
        "gate_events": [],
        "result": None,
    }
    (job_dir / "job.json").write_text(json.dumps(metadata), encoding="utf-8")
    lock = manager.runtime_root / "locks" / "starting_project.lock"
    lock.parent.mkdir(parents=True)
    lock.touch()

    result = manager.recover_orphans()

    assert result["recovered_jobs"] == []
    assert result["recovered_locks"] == []
    assert manager.status(job_id)["status"] == "queued"
    assert lock.exists()
