from __future__ import annotations

import shutil
import subprocess
import os
from dataclasses import dataclass
from pathlib import Path

from ..models import Failure, FailureCategory, GateReport, Status


@dataclass(frozen=True)
class ToolResult:
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    available: bool


def resolve_tool(executable: str) -> str | None:
    resolved = shutil.which(executable)
    if resolved is None and executable == "kicad-cli":
        candidate = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
        resolved = str(candidate) if candidate.is_file() else None
    return resolved


def tool_version(executable: str) -> str | None:
    resolved = resolve_tool(executable)
    if resolved is None:
        return None
    completed = subprocess.run([resolved, "version"], capture_output=True, text=True, timeout=30, check=False)
    return completed.stdout.strip() or completed.stderr.strip() or None


def run_tool(executable: str, arguments: list[str], cwd: Path, timeout: int = 300, env: dict[str, str] | None = None) -> ToolResult:
    resolved = resolve_tool(executable)
    command = [executable, *arguments]
    if resolved is None:
        return ToolResult(command, None, "", f"Executable not found: {executable}", False)
    completed = subprocess.run([resolved, *arguments], cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False, env={**os.environ, **(env or {})})
    return ToolResult(command, completed.returncode, completed.stdout, completed.stderr, True)


def tool_report(gate: str, result: ToolResult, artifacts: list[str] | None = None) -> GateReport:
    backend = {"command": result.command, "returncode": result.returncode, "stdout": result.stdout[-8000:], "stderr": result.stderr[-8000:], "available": result.available}
    if not result.available:
        failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", result.stderr, details={"command": result.command})
        return GateReport(gate, Status.BLOCKED, [failure], backend=backend)
    if result.returncode != 0:
        failure = Failure(FailureCategory.TOOL_ERROR, "tool_failed", f"{result.command[0]} exited with status {result.returncode}", details=backend)
        return GateReport(gate, Status.FAIL, [failure], backend=backend)
    return GateReport(gate, Status.PASS, artifacts=artifacts or [], backend=backend)
