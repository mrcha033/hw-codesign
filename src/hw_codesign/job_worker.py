from __future__ import annotations

import json
import os
import shutil
import sys
import traceback
from pathlib import Path
from typing import Any

from .io import write_json
from .jobs import ProjectWriterLock, atomic_replace_project, utc_now
from .service import HardwareService


def _invoke(service: HardwareService, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
    project = str(arguments["project"])
    if tool == "hw_generate_all":
        return service.generate_all(project)
    if tool == "hw_generate_electronics_source":
        return service.generate_electronics_source(project)
    if tool == "hw_generate_mechanical":
        return service.generate_mechanical_source(project)
    if tool == "hw_generate_firmware":
        return service.generate_firmware_source(project)
    if tool == "hw_run_erc":
        return service.kicad.run_erc(service.workspace.require_project(project)).to_dict()
    if tool == "hw_run_drc":
        return service.kicad.run_drc(service.workspace.require_project(project)).to_dict()
    if tool == "hw_build_firmware":
        spec = service.read_spec(project)
        return service.zephyr.build(service.workspace.require_project(project), spec["firmware"]["target"]).to_dict()
    if tool == "hw_run_all_checks":
        return service.run_all_checks(project, bool(arguments.get("include_external", True)))
    if tool == "hw_design_candidate":
        return service.design_candidate(
            project,
            requirements_text=arguments.get("requirements_text"),
            include_external=bool(arguments.get("include_external", False)),
            with_review_bundle=bool(arguments.get("with_review_bundle", True)),
        )
    if tool == "hw_explore_design_space":
        return service.explore_design_space(project, int(arguments.get("max_candidates", 8)))
    if tool == "hw_run_design_iteration":
        return service.run_design_iteration(project, bool(arguments.get("include_external", True)))
    if tool == "hw_design_until_release":
        if arguments.get("user_approved_autonomous_iteration") is not True:
            return {
                "status": "blocked",
                "code": "autonomous_iteration_approval_required",
                "message": "Set user_approved_autonomous_iteration=true to run autonomous iterations",
            }
        return service.design_until_release(
            project,
            int(arguments.get("max_iterations", 8)),
            bool(arguments.get("include_external", False)),
        )
    if tool == "hw_export_release_bundle":
        return service.export_release_bundle(project)
    if tool == "hw_export_candidate_bundle":
        return service.export_candidate_bundle(project)
    raise ValueError(f"Unsupported job tool: {tool}")


def _rewrite_paths(value: Any, staged_project: Path, destination_project: Path) -> Any:
    if isinstance(value, str):
        return value.replace(str(staged_project), str(destination_project))
    if isinstance(value, list):
        return [_rewrite_paths(item, staged_project, destination_project) for item in value]
    if isinstance(value, dict):
        return {key: _rewrite_paths(item, staged_project, destination_project) for key, item in value.items()}
    return value


def run(root: Path, job_id: str) -> int:
    root = root.resolve()
    runtime_root = root / ".hw-runtime"
    job_dir = runtime_root / "jobs" / job_id
    metadata_path = job_dir / "job.json"
    request = json.loads((job_dir / "request.json").read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    project = str(request["arguments"]["project"])
    metadata.update({
        "status": "running",
        "started_at": utc_now(),
        "pid": os.getpid(),
        "pgid": os.getpgrp() if hasattr(os, "getpgrp") else os.getpid(),
    })
    write_json(metadata_path, metadata)

    source_project = root / "projects" / project
    workspace_root = job_dir / "workspace"
    staged_project = workspace_root / "projects" / project
    backup_project = job_dir / "previous-project"
    try:
        timeout = float(os.environ.get("HW_JOB_LOCK_TIMEOUT_SECONDS", "30"))
        with ProjectWriterLock(runtime_root, project, job_id, timeout_seconds=timeout):
            if workspace_root.exists():
                shutil.rmtree(workspace_root)
            staged_project.parent.mkdir(parents=True)
            shutil.copytree(
                source_project,
                staged_project,
                copy_function=shutil.copy2,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
            service = HardwareService(workspace_root)
            result = _invoke(service, str(request["tool"]), dict(request["arguments"]))
            write_json(job_dir / "result.json", result)
            if str(result.get("status", "")).lower() in {"fail", "blocked", "cancelled"}:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                metadata.update({
                    "status": "failed",
                    "finished_at": utc_now(),
                    "result": result,
                    "committed": False,
                    "error": {
                        "code": "operation_not_committed",
                        "message": f"Tool returned {result.get('status')}; isolated project changes were not applied",
                    },
                })
                write_json(metadata_path, metadata)
                return 1
            atomic_replace_project(source_project, staged_project, backup_project)
            result = _rewrite_paths(result, staged_project, source_project)
            write_json(job_dir / "result.json", result)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update({"status": "complete", "finished_at": utc_now(), "result": result, "committed": True, "error": None})
        write_json(metadata_path, metadata)
        return 0
    except BaseException as exc:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {"job_id": job_id}
        if metadata.get("status") != "cancelled":
            metadata.update({
                "status": "failed",
                "finished_at": utc_now(),
                "committed": False,
                "error": {
                    "code": "job_execution_failed",
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "traceback": traceback.format_exc(limit=20),
                },
            })
            write_json(metadata_path, metadata)
        return 1


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: python -m hw_codesign.job_worker ROOT JOB_ID")
    raise SystemExit(run(Path(sys.argv[1]), sys.argv[2]))


if __name__ == "__main__":
    main()
