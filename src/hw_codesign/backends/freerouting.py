from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from ..io import write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..processes import run_process_group


class FreeroutingBackend:
    VERSION = "2.2.4"
    DEFAULT_TIMEOUT_SECONDS = 600

    def __init__(self, root: Path):
        self.root = root

    def route(self, project: Path, max_passes: int = 20, threads: int = 4, timeout_seconds: int | None = None) -> GateReport:
        timeout_seconds = _timeout_seconds(timeout_seconds, "HW_FREEROUTING_TIMEOUT_SECONDS", self.DEFAULT_TIMEOUT_SECONDS)
        target = project / "electronics" / "generated" / "kicad"
        board = target / f"{project.name}.kicad_pcb"
        dsn = target / f"{project.name}.dsn"
        ses = target / f"{project.name}.ses"
        routed = target / f"{project.name}.routed.kicad_pcb"
        routing_report = target / "routing.json"
        source_routing: dict[str, object] = {}
        if board.is_file() and routing_report.is_file():
            source_routing = json.loads(routing_report.read_text(encoding="utf-8"))
            board_sha256 = hashlib.sha256(board.read_bytes()).hexdigest()
            if (
                source_routing.get("status") == "pass"
                and source_routing.get("signal_routing") == "complete"
                and source_routing.get("plane_connectivity") == "copper_zones"
                and source_routing.get("board_sha256") == board_sha256
            ):
                return GateReport(
                    "autoroute",
                    Status.PASS,
                    metrics={"unrouted": 0, "max_passes": source_routing.get("max_passes"), "cached": True},
                    artifacts=[str(board), str(routing_report)],
                    backend={"name": "freerouting", "version": source_routing.get("freerouting_version", self.VERSION), "cached": True},
                )
        tools = self._tools()
        missing = [name for name, path in tools.items() if path is None]
        if missing:
            return GateReport(
                "autoroute",
                Status.BLOCKED,
                [Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", f"Missing autorouter tools: {', '.join(missing)}")],
                backend={"name": "freerouting", "version": self.VERSION, "tools": {key: str(value) if value else None for key, value in tools.items()}},
            )
        if not board.is_file():
            return GateReport("autoroute", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists — electronics compile gate must pass first")])

        export = self._pcbnew(
            tools["kicad_python"],
            "import pcbnew,sys; b=pcbnew.LoadBoard(sys.argv[1]); raise SystemExit(0 if pcbnew.ExportSpecctraDSN(b,sys.argv[2]) else 2)",
            board,
            dsn,
        )
        if export.returncode != 0:
            return self._failure("dsn_export_failed", "KiCad failed to export Specctra DSN", export, tools)

        command = [
            str(tools["java"]), "-Djava.awt.headless=true", "-jar", str(tools["jar"]),
            "-de", str(dsn.resolve()), "-do", str(ses.resolve()),
            "-mp", str(max_passes), "-mt", str(threads), "-l", "en",
        ]
        try:
            completed = run_process_group(command, cwd=project.resolve(), timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.TOOL_ERROR, "autoroute_timeout", f"Freerouting exceeded the {timeout_seconds} second limit", details={"timeout_seconds": timeout_seconds, "stdout": (exc.stdout or "")[-8000:], "stderr": (exc.stderr or "")[-8000:]})],
                backend={**self._backend(command, None, tools), "timeout_seconds": timeout_seconds},
            )
        log = f"{completed.stdout}\n{completed.stderr}"
        unrouted, violations = self._final_routing_metrics(log)
        if completed.returncode != 0 or not ses.is_file():
            return self._failure("autoroute_failed", "Freerouting did not produce a session file", completed, tools, command)
        if unrouted is None:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.EDA_ERROR, "routing_completion_unverified", "Freerouting produced a session but no authoritative final-score line was found")],
                metrics={"unrouted": None, "violations": violations, "max_passes": max_passes},
                artifacts=[str(dsn), str(ses)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        if unrouted != 0:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.EDA_ERROR, "routing_incomplete", f"Freerouting left {unrouted} connection(s) unrouted", details={"unrouted": unrouted})],
                metrics={"unrouted": unrouted, "violations": violations, "max_passes": max_passes},
                artifacts=[str(dsn), str(ses)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        if violations not in {None, 0}:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.EDA_ERROR, "routing_violations", f"Freerouting completed with {violations} rule violation(s)", details={"violations": violations})],
                metrics={"unrouted": unrouted, "violations": violations, "max_passes": max_passes},
                artifacts=[str(dsn), str(ses)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )

        imported = self._pcbnew(
            tools["kicad_python"],
            "import pcbnew,sys; b=pcbnew.LoadBoard(sys.argv[1]); ok=pcbnew.ImportSpecctraSES(b,sys.argv[2]); pcbnew.SaveBoard(sys.argv[3],b); raise SystemExit(0 if ok else 2)",
            board,
            ses,
            routed,
        )
        if imported.returncode != 0 or not routed.is_file():
            return self._failure("ses_import_failed", "KiCad failed to import the Freerouting session", imported, tools)
        os.replace(routed, board)
        write_json(routing_report, {
            "status": "pass",
            "mode": "zone_connected_planes_freerouting",
            "plane_connectivity": "copper_zones",
            "zone_nets": source_routing.get("zone_nets", []),
            "signal_routing": "complete",
            "freerouting_version": self.VERSION,
            "unrouted": 0,
            "violations": 0,
            "max_passes": max_passes,
            "failures": [],
        })
        routed_payload = json.loads(routing_report.read_text(encoding="utf-8"))
        routed_payload["board_sha256"] = hashlib.sha256(board.read_bytes()).hexdigest()
        write_json(routing_report, routed_payload)
        return GateReport(
            "autoroute",
            Status.PASS,
            metrics={"unrouted": 0, "max_passes": max_passes},
            artifacts=[str(board), str(dsn), str(ses), str(routing_report)],
            backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
        )

    def _tools(self) -> dict[str, Path | None]:
        java = os.environ.get("HW_JAVA")
        jar = os.environ.get("HW_FREEROUTING_JAR")
        kicad_python = os.environ.get("HW_KICAD_PYTHON")
        java_path = Path(java).resolve() if java else (self.root / ".toolchains" / "java25" / "Contents" / "Home" / "bin" / "java").resolve()
        jar_path = Path(jar).resolve() if jar else (self.root / ".toolchains" / "freerouting" / f"freerouting-{self.VERSION}.jar").resolve()
        kicad_path = Path(kicad_python).resolve() if kicad_python else Path("/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9")
        if not java_path.is_file():
            resolved = shutil.which("java")
            java_path = Path(resolved).resolve() if resolved else None
        return {
            "java": java_path if java_path and java_path.is_file() else None,
            "jar": jar_path if jar_path.is_file() else None,
            "kicad_python": kicad_path if kicad_path.is_file() else None,
        }

    def tools(self) -> dict[str, Path | None]:
        return self._tools()

    @staticmethod
    def _pcbnew(executable: Path, code: str, *arguments: Path) -> subprocess.CompletedProcess[str]:
        return run_process_group([str(executable), "-c", code, *(str(item) for item in arguments)], timeout=60)

    @staticmethod
    def _final_unrouted(log: str) -> int | None:
        return FreeroutingBackend._final_routing_metrics(log)[0]

    @staticmethod
    def _final_routing_metrics(log: str) -> tuple[int | None, int | None]:
        """Return final ``(unrouted, violations)`` from Freerouting's last score line."""
        score_lines = re.findall(r"final score:[^\r\n]*", log, flags=re.IGNORECASE)
        if not score_lines:
            return None, None
        final = score_lines[-1]
        unrouted_match = re.search(r"\b(\d+)\s+unrouted\b", final, flags=re.IGNORECASE)
        violations_match = re.search(r"\b(\d+)\s+violations?\b", final, flags=re.IGNORECASE)
        return (
            int(unrouted_match.group(1)) if unrouted_match else 0,
            int(violations_match.group(1)) if violations_match else 0,
        )

    def _failure(self, code, message, completed, tools, command=None):
        details = {"returncode": completed.returncode, "stdout": completed.stdout[-8000:], "stderr": completed.stderr[-8000:]}
        return GateReport(
            "autoroute",
            Status.FAIL,
            [Failure(FailureCategory.TOOL_ERROR, code, message, details=details)],
            backend=self._backend(command or completed.args, completed.returncode, tools, f"{completed.stdout}\n{completed.stderr}"),
        )

    def _backend(self, command, returncode, tools, log=""):
        return {
            "name": "freerouting",
            "version": self.VERSION,
            "command": [str(item) for item in command],
            "returncode": returncode,
            "log_tail": log[-8000:],
            "tools": {key: str(value) if value else None for key, value in tools.items()},
        }


def _timeout_seconds(value: int | None, env_name: str, default: int) -> int:
    raw = value if value is not None else os.environ.get(env_name, default)
    try:
        parsed = int(raw)
    except (TypeError, ValueError):
        return default
    return max(1, parsed)
