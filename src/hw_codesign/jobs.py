from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
import uuid
from contextlib import AbstractContextManager
from ctypes import wintypes
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .io import write_json
from .workspace import PROJECT_NAME

TERMINAL_JOB_STATES = frozenset({"complete", "failed", "cancelled"})
SUPPORTED_JOB_TOOLS = frozenset({
    "hw_generate_all",
    "hw_generate_electronics_source",
    "hw_generate_mechanical",
    "hw_generate_firmware",
    "hw_run_erc",
    "hw_run_drc",
    "hw_build_firmware",
    "hw_run_all_checks",
    "hw_design_candidate",
    "hw_explore_design_space",
    "hw_run_design_iteration",
    "hw_design_until_release",
    "hw_export_release_bundle",
    "hw_export_candidate_bundle",
})


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def process_alive(pid: int | None) -> bool:
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        # ``os.kill(pid, 0)`` is not a reliable existence probe on Windows:
        # it can report access denied for a live process and leave stale lock
        # owners looking alive forever.  OpenProcess distinguishes the
        # invalid-PID error from an access restriction without terminating the
        # process.
        try:
            import ctypes

            process_query_limited_information = 0x1000
            invalid_parameter = 87
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL
            handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
            if not handle:
                return ctypes.get_last_error() != invalid_parameter
            kernel32.CloseHandle(handle)
            return True
        except (AttributeError, OSError):
            # Keep a conservative fallback for restricted Python runtimes.
            pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class ProjectWriterLock(AbstractContextManager["ProjectWriterLock"]):
    """Cross-process single-writer lock with stale-owner recovery."""

    def __init__(self, runtime_root: Path, project: str, job_id: str, *, timeout_seconds: float = 30.0):
        if not PROJECT_NAME.fullmatch(project):
            raise ValueError(f"Invalid project name: {project!r}")
        self.path = runtime_root / "locks" / f"{project}.lock"
        self.project = project
        self.job_id = job_id
        self.timeout_seconds = timeout_seconds
        self.acquired = False

    def acquire(self) -> "ProjectWriterLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        wall_deadline = time.time() + self.timeout_seconds
        payload = {
            "project": self.project,
            "job_id": self.job_id,
            "pid": os.getpid(),
            "created_at": utc_now(),
        }
        while True:
            try:
                fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except FileExistsError:
                try:
                    observed = self.path.stat()
                except FileNotFoundError:
                    continue
                owner = _read_json(self.path)
                if _lock_owner_is_stale(self.path, owner) and _same_file_version(self.path, observed):
                    self.path.unlink(missing_ok=True)
                    continue
                if time.monotonic() >= deadline or time.time() >= wall_deadline:
                    raise TimeoutError(
                        f"Project {self.project} is locked by job {owner.get('job_id', 'unknown')} "
                        f"(pid {owner.get('pid', 'unknown')})"
                    )
                time.sleep(0.1)
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
            self.acquired = True
            return self

    def release(self) -> None:
        if not self.acquired:
            return
        owner = _read_json(self.path)
        if owner.get("job_id") == self.job_id and _as_int(owner.get("pid")) == os.getpid():
            self.path.unlink(missing_ok=True)
        self.acquired = False

    def __enter__(self) -> "ProjectWriterLock":
        return self.acquire()

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.release()


class JobManager:
    """Persistent async jobs executed in isolated copy-on-write workspaces."""

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.runtime_root = self.root / ".hw-runtime"
        self.jobs_root = self.runtime_root / "jobs"
        self.jobs_root.mkdir(parents=True, exist_ok=True)
        self._processes: dict[str, subprocess.Popen[bytes]] = {}

    def submit(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.recover_orphans()
        if tool not in SUPPORTED_JOB_TOOLS:
            raise ValueError(f"Tool {tool!r} is not supported by the isolated job runner")
        project = str(arguments.get("project", ""))
        if not PROJECT_NAME.fullmatch(project):
            raise ValueError("Job arguments must contain a valid project name")
        project_path = self.root / "projects" / project / "project.yaml"
        if not project_path.is_file():
            raise FileNotFoundError(f"Project does not exist: {project}")

        job_id = uuid.uuid4().hex
        job_dir = self.jobs_root / job_id
        job_dir.mkdir(parents=True)
        metadata = {
            "job_id": job_id,
            "tool": tool,
            "arguments": arguments,
            "project": project,
            "status": "queued",
            "submitted_at": utc_now(),
            "started_at": None,
            "finished_at": None,
            "pid": None,
            "pgid": None,
            "gate_events": [],
            "result": None,
            "error": None,
            "committed": False,
            "workspace": str(job_dir / "workspace"),
            "stdout_log": str(job_dir / "stdout.log"),
            "stderr_log": str(job_dir / "stderr.log"),
        }
        write_json(job_dir / "job.json", metadata)
        write_json(job_dir / "request.json", {"tool": tool, "arguments": arguments})

        stdout_handle = (job_dir / "stdout.log").open("ab", buffering=0)
        stderr_handle = (job_dir / "stderr.log").open("ab", buffering=0)
        worker_env = os.environ.copy()
        source_root = str(Path(__file__).resolve().parent.parent)
        worker_env["PYTHONPATH"] = os.pathsep.join(
            item for item in (source_root, worker_env.get("PYTHONPATH", "")) if item
        )
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "hw_codesign.job_worker", str(self.root), job_id],
                cwd=self.root,
                env=worker_env,
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                start_new_session=True,
                close_fds=True,
            )
        finally:
            stdout_handle.close()
            stderr_handle.close()
        self._processes[job_id] = process
        current = self._read(job_id)
        if current.get("status") not in TERMINAL_JOB_STATES:
            current.update({"pid": process.pid, "pgid": process.pid})
            write_json(job_dir / "job.json", current)
        return self.status(job_id)

    def status(self, job_id: str) -> dict[str, Any]:
        metadata = self._read(job_id)
        process = self._processes.get(job_id)
        if metadata.get("status") not in TERMINAL_JOB_STATES and process is not None:
            return_code = process.poll()
            if return_code is not None:
                self._processes.pop(job_id, None)
                metadata = self._read(job_id)
                if metadata.get("status") not in TERMINAL_JOB_STATES:
                    stderr_path = self.jobs_root / job_id / "stderr.log"
                    stderr_tail = _tail_text(stderr_path)
                    metadata.update({
                        "status": "failed",
                        "finished_at": utc_now(),
                        "error": {
                            "code": "worker_process_exited",
                            "message": f"Worker exited with code {return_code} before recording a terminal state",
                            "stderr_tail": stderr_tail,
                        },
                    })
                    write_json(self.jobs_root / job_id / "job.json", metadata)
        result_path = self.jobs_root / job_id / "result.json"
        if result_path.is_file():
            metadata["result"] = _read_json(result_path)
        return metadata

    def cancel(self, job_id: str, *, grace_seconds: float = 2.0) -> dict[str, Any]:
        metadata = self._read(job_id)
        if metadata.get("status") in TERMINAL_JOB_STATES:
            process = self._processes.pop(job_id, None)
            if process is not None:
                process.poll()
            return self.status(job_id)
        pgid = _as_int(metadata.get("pgid"))
        pid = _as_int(metadata.get("pid"))
        target_group = pgid or pid
        if target_group:
            try:
                _terminate_process_tree(target_group, force=False)
            except ProcessLookupError:
                pass
            deadline = time.monotonic() + grace_seconds
            while pid and process_alive(pid) and time.monotonic() < deadline:
                time.sleep(0.05)
            if pid and process_alive(pid):
                try:
                    _terminate_process_tree(target_group, force=True)
                except (ProcessLookupError, PermissionError):
                    pass
        metadata.update({
            "status": "cancelled",
            "finished_at": utc_now(),
            "committed": False,
            "error": {"code": "job_cancelled", "message": "Job and its process group were cancelled"},
        })
        write_json(self.jobs_root / job_id / "job.json", metadata)
        process = self._processes.pop(job_id, None)
        if process is not None:
            process.poll()
        self._remove_owned_lock(metadata)
        return self.status(job_id)

    def recover_orphans(self) -> dict[str, Any]:
        recovered_jobs: list[str] = []
        recovered_locks: list[str] = []
        for job_file in sorted(self.jobs_root.glob("*/job.json")):
            metadata = _read_json(job_file)
            if metadata.get("status") not in {"queued", "running"}:
                continue
            pid = _as_int(metadata.get("pid"))
            if metadata.get("status") == "queued" and pid is None and _age_seconds(metadata.get("submitted_at")) < 30.0:
                continue
            if pid and process_alive(pid):
                continue
            metadata.update({
                "status": "failed",
                "finished_at": utc_now(),
                "committed": False,
                "error": {"code": "orphaned_worker", "message": "Worker exited without recording a terminal state"},
            })
            write_json(job_file, metadata)
            self._remove_owned_lock(metadata)
            recovered_jobs.append(str(metadata.get("job_id")))
        locks_dir = self.runtime_root / "locks"
        for lock_path in sorted(locks_dir.glob("*.lock")) if locks_dir.is_dir() else []:
            try:
                observed = lock_path.stat()
            except FileNotFoundError:
                continue
            owner = _read_json(lock_path)
            if _lock_owner_is_stale(lock_path, owner) and _same_file_version(lock_path, observed):
                lock_path.unlink(missing_ok=True)
                recovered_locks.append(lock_path.stem)
        return {"status": "pass", "recovered_jobs": recovered_jobs, "recovered_locks": recovered_locks}

    def _read(self, job_id: str) -> dict[str, Any]:
        if not job_id or any(character not in "0123456789abcdef" for character in job_id.lower()):
            raise ValueError("Invalid job ID")
        path = self.jobs_root / job_id / "job.json"
        if not path.is_file():
            raise FileNotFoundError(f"Unknown job: {job_id}")
        return _read_json(path)

    def _remove_owned_lock(self, metadata: dict[str, Any]) -> None:
        project = metadata.get("project")
        if not isinstance(project, str) or not PROJECT_NAME.fullmatch(project):
            return
        lock_path = self.runtime_root / "locks" / f"{project}.lock"
        owner = _read_json(lock_path)
        if owner.get("job_id") == metadata.get("job_id"):
            lock_path.unlink(missing_ok=True)


def atomic_replace_project(source: Path, staged: Path, backup: Path) -> None:
    """Atomically promote a staged project, restoring the old tree on failure."""

    if backup.exists():
        shutil.rmtree(backup)
    os.replace(source, backup)
    try:
        os.replace(staged, source)
    except BaseException:
        os.replace(backup, source)
        raise
    shutil.rmtree(backup)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _tail_text(path: Path, limit: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[-limit:]
    except OSError:
        return ""


def _age_seconds(value: Any) -> float:
    try:
        timestamp = datetime.fromisoformat(str(value))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=UTC)
        return max(0.0, (datetime.now(UTC) - timestamp).total_seconds())
    except (TypeError, ValueError):
        return float("inf")


def _lock_owner_is_stale(path: Path, owner: dict[str, Any]) -> bool:
    pid = _as_int(owner.get("pid"))
    if pid is not None:
        return not process_alive(pid)
    try:
        return time.time() - path.stat().st_mtime > 5.0
    except FileNotFoundError:
        return False


def _same_file_version(path: Path, observed: os.stat_result) -> bool:
    try:
        current = path.stat()
    except FileNotFoundError:
        return False
    return (
        current.st_ino == observed.st_ino
        and current.st_mtime_ns == observed.st_mtime_ns
        and current.st_size == observed.st_size
    )


def _terminate_process_tree(process_group: int, *, force: bool) -> None:
    if os.name == "nt":
        command = ["taskkill", "/PID", str(process_group), "/T"]
        if force:
            command.append("/F")
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode not in {0, 128} and "not found" not in completed.stderr.lower():
            raise ProcessLookupError(completed.stderr.strip())
        return
    os.killpg(process_group, signal.SIGKILL if force else signal.SIGTERM)
