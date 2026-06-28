from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from ..io import write_json
from ..models import Failure, FailureCategory, GateReport, Status


class FreeroutingBackend:
    VERSION = "2.2.4"

    def __init__(self, root: Path):
        self.root = root

    def route(self, project: Path, max_passes: int = 20, threads: int = 4) -> GateReport:
        target = project / "electronics" / "generated" / "kicad"
        board = target / f"{project.name}.kicad_pcb"
        dsn = target / f"{project.name}.dsn"
        ses = target / f"{project.name}.ses"
        routed = target / f"{project.name}.routed.kicad_pcb"
        routing_report = target / "routing.json"
        if board.is_file() and routing_report.is_file():
            cached = json.loads(routing_report.read_text(encoding="utf-8"))
            if cached.get("status") == "pass" and cached.get("signal_routing") == "complete":
                return GateReport(
                    "autoroute",
                    Status.PASS,
                    metrics={"unrouted": 0, "max_passes": cached.get("max_passes"), "cached": True},
                    artifacts=[str(board), str(routing_report)],
                    backend={"name": "freerouting", "version": cached.get("freerouting_version", self.VERSION), "cached": True},
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
            return GateReport("autoroute", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists")])

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
            completed = subprocess.run(command, cwd=project.resolve(), capture_output=True, text=True, timeout=600, check=False)
        except subprocess.TimeoutExpired as exc:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.TOOL_ERROR, "autoroute_timeout", "Freerouting exceeded the 600 second limit", details={"stdout": (exc.stdout or "")[-8000:], "stderr": (exc.stderr or "")[-8000:]})],
                backend=self._backend(command, None, tools),
            )
        log = f"{completed.stdout}\n{completed.stderr}"
        unrouted = self._final_unrouted(log)
        if completed.returncode != 0 or not ses.is_file():
            return self._failure("autoroute_failed", "Freerouting did not produce a session file", completed, tools, command)
        if unrouted not in {None, 0}:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.EDA_ERROR, "routing_incomplete", f"Freerouting left {unrouted} connection(s) unrouted", details={"unrouted": unrouted})],
                metrics={"unrouted": unrouted, "max_passes": max_passes},
                artifacts=[str(dsn), str(ses)],
                backend=self._backend(command, completed.returncode, tools, log),
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
            "mode": "plane_preseeded_freerouting",
            "signal_routing": "complete",
            "freerouting_version": self.VERSION,
            "unrouted": 0,
            "max_passes": max_passes,
            "failures": [],
        })
        return GateReport(
            "autoroute",
            Status.PASS,
            metrics={"unrouted": 0, "max_passes": max_passes},
            artifacts=[str(board), str(dsn), str(ses), str(routing_report)],
            backend=self._backend(command, completed.returncode, tools, log),
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

    @staticmethod
    def _pcbnew(executable: Path, code: str, *arguments: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(executable), "-c", code, *(str(item) for item in arguments)], capture_output=True, text=True, timeout=60, check=False)

    @staticmethod
    def _final_unrouted(log: str) -> int | None:
        # Parse the "session completed" line which has the authoritative final score.
        # Format: "final score: S.SS (N unrouted)" or "final score: S.SS" (0 unrouted).
        session = re.search(r"session completed:.*?final score:\s*[\d.]+\s*(?:\((\d+) unrouted\))?", log)
        if session:
            return int(session.group(1)) if session.group(1) is not None else 0
        # Fallback: last "(N unrouted)" occurrence from pass lines.
        matches = re.findall(r"\((\d+) unrouted\)", log)
        return int(matches[-1]) if matches else None

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
