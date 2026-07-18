from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

from ..io import write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..processes import run_process_group

_MIN_ROUTING_RULE_MM = 0.01
_MAX_ROUTING_RULE_MM = 10.0


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
        project_file = board.with_suffix(".kicad_pro")
        project_rules: tuple[float, float] | None = None
        if board.is_file():
            try:
                project_rules = _project_routing_rules(project_file)
            except (OSError, UnicodeError, ValueError) as exc:
                return GateReport(
                    "autoroute",
                    Status.BLOCKED,
                    [
                        Failure(
                            FailureCategory.EDA_ERROR,
                            "invalid_project_design_rules",
                            "The generated KiCad project has invalid routing rules; DSN export was not attempted",
                            path=str(project_file),
                            details={
                                "error": str(exc),
                                "minimum_mm": _MIN_ROUTING_RULE_MM,
                                "maximum_mm": _MAX_ROUTING_RULE_MM,
                            },
                        )
                    ],
                    backend={"name": "freerouting", "version": self.VERSION},
                )
        if board.is_file() and routing_report.is_file():
            source_routing = json.loads(routing_report.read_text(encoding="utf-8"))
            board_sha256 = hashlib.sha256(board.read_bytes()).hexdigest()
            zone_count, filled_polygon_count = _zone_fill_counts(board.read_text(encoding="utf-8"))
            if (
                source_routing.get("status") == "pass"
                and source_routing.get("signal_routing") == "complete"
                and source_routing.get("plane_connectivity") == "copper_zones"
                and source_routing.get("board_sha256") == board_sha256
                and source_routing.get("design_rules") == _routing_rules_payload(project_rules)
                and source_routing.get("post_import_unconnected") == 0
                and (zone_count == 0 or filled_polygon_count > 0)
            ):
                return GateReport(
                    "autoroute",
                    Status.PASS,
                    metrics={
                        "unrouted": 0,
                        "freerouting_unrouted": source_routing.get("freerouting_unrouted", 0),
                        "max_passes": source_routing.get("max_passes"),
                        "cached": True,
                        "zone_count": zone_count,
                        "filled_polygon_count": filled_polygon_count,
                    },
                    artifacts=[str(board), str(routing_report)],
                    backend={"name": "freerouting", "version": source_routing.get("freerouting_version", self.VERSION), "cached": True},
                )
            cached_failure = _cached_incomplete_plane_failure(
                source_routing,
                board=board,
                board_sha256=board_sha256,
                project_rules=project_rules,
                zone_count=zone_count,
                filled_polygon_count=filled_polygon_count,
                default_version=self.VERSION,
            )
            if cached_failure is not None:
                return cached_failure
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

        export_arguments: list[Path | str] = [board, dsn]
        if project_rules is not None:
            clearance_mm, track_width_mm = project_rules
            export_arguments.extend([format(clearance_mm, ".12g"), format(track_width_mm, ".12g")])
        export = self._pcbnew(
            tools["kicad_python"],
            """import pcbnew
import sys

board = pcbnew.LoadBoard(sys.argv[1])
if len(sys.argv) == 5:
    clearance = pcbnew.FromMM(float(sys.argv[3]))
    track_width = pcbnew.FromMM(float(sys.argv[4]))
    settings = board.GetDesignSettings()
    settings.m_MinClearance = clearance
    settings.m_TrackMinWidth = track_width
    default_netclass = board.GetAllNetClasses()["Default"]
    default_netclass.SetClearance(clearance)
    default_netclass.SetTrackWidth(track_width)
elif len(sys.argv) != 3:
    raise SystemExit(3)
raise SystemExit(0 if pcbnew.ExportSpecctraDSN(board, sys.argv[2]) else 2)
""",
            *export_arguments,
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
        if violations not in {None, 0}:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [Failure(FailureCategory.EDA_ERROR, "routing_violations", f"Freerouting completed with {violations} rule violation(s)", details={"violations": violations})],
                metrics={"unrouted": unrouted, "violations": violations, "max_passes": max_passes},
                artifacts=[str(dsn), str(ses)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )

        import_arguments: list[Path | str] = [board, ses, routed]
        if project_rules is not None:
            clearance_mm, track_width_mm = project_rules
            import_arguments.extend([format(clearance_mm, ".12g"), format(track_width_mm, ".12g")])
        imported = self._pcbnew(
            tools["kicad_python"],
            """import pcbnew
import sys

board = pcbnew.LoadBoard(sys.argv[1])
if len(sys.argv) == 6:
    clearance = pcbnew.FromMM(float(sys.argv[4]))
    track_width = pcbnew.FromMM(float(sys.argv[5]))
    settings = board.GetDesignSettings()
    settings.m_MinClearance = clearance
    settings.m_TrackMinWidth = track_width
    default_netclass = board.GetAllNetClasses()["Default"]
    default_netclass.SetClearance(clearance)
    default_netclass.SetTrackWidth(track_width)
elif len(sys.argv) != 4:
    raise SystemExit(3)
ok = pcbnew.ImportSpecctraSES(board, sys.argv[2])
if ok:
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.BuildConnectivity()
    pcbnew.SaveBoard(sys.argv[3], board)
    print(f"HW_UNCONNECTED={board.GetConnectivity().GetUnconnectedCount(False)}")
raise SystemExit(0 if ok else 2)
""",
            *import_arguments,
        )
        if imported.returncode != 0 or not routed.is_file():
            return self._failure("ses_import_failed", "KiCad failed to import the Freerouting session", imported, tools)
        routed_text = routed.read_text(encoding="utf-8")
        zone_count, filled_polygon_count = _zone_fill_counts(routed_text)
        if zone_count and not filled_polygon_count:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [
                    Failure(
                        FailureCategory.EDA_ERROR,
                        "zone_fill_not_persisted",
                        "KiCad imported the routing session but did not persist filled copper zones",
                        path=str(routed),
                        details={"zone_count": zone_count, "filled_polygon_count": 0},
                    )
                ],
                metrics={
                    "unrouted": unrouted,
                    "freerouting_unrouted": unrouted,
                    "zone_count": zone_count,
                    "filled_polygon_count": 0,
                },
                artifacts=[str(dsn), str(ses), str(routed)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        connectivity_match = re.search(r"(?m)^HW_UNCONNECTED=(\d+)\s*$", imported.stdout)
        if connectivity_match is None:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [
                    Failure(
                        FailureCategory.TOOL_ERROR,
                        "post_import_connectivity_unverified",
                        "KiCad imported the routing session but did not report authoritative connectivity",
                        path=str(routed),
                    )
                ],
                metrics={
                    "unrouted": None,
                    "freerouting_unrouted": unrouted,
                    "zone_count": zone_count,
                    "filled_polygon_count": filled_polygon_count,
                },
                artifacts=[str(dsn), str(ses), str(routed)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        post_import_unconnected = int(connectivity_match.group(1))
        routed_project = routed.with_suffix(".kicad_pro")
        try:
            project_sidecar_promoted = _promote_routed_project(
                routed_project,
                project_file,
                project_rules,
            )
            if project_rules is not None:
                canonical_rules = _project_routing_rules(project_file)
                canonical_payload = json.loads(project_file.read_text(encoding="utf-8"))
                if not isinstance(canonical_payload, dict):
                    raise ValueError("canonical KiCad project must contain a JSON object")
                canonical_default_rules = _project_default_netclass_rules(canonical_payload)
                if canonical_rules != project_rules or canonical_default_rules != project_rules:
                    raise ValueError("canonical KiCad project does not preserve the routed design rules")
        except (OSError, UnicodeError, ValueError) as exc:
            return GateReport(
                "autoroute",
                Status.FAIL,
                [
                    Failure(
                        FailureCategory.EDA_ERROR,
                        "project_rule_persistence_failed",
                        "KiCad imported the routing session but failed to persist matching project/netclass rules",
                        path=str(project_file),
                        details={"error": str(exc)},
                    )
                ],
                metrics={
                    "unrouted": post_import_unconnected,
                    "freerouting_unrouted": unrouted,
                    "zone_count": zone_count,
                    "filled_polygon_count": filled_polygon_count,
                },
                artifacts=[str(dsn), str(ses), str(routed)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        os.replace(routed, board)
        if post_import_unconnected:
            routing_failure = Failure(
                FailureCategory.EDA_ERROR,
                "routing_incomplete_after_zone_fill",
                f"KiCad found {post_import_unconnected} unconnected item(s) after session import and zone fill",
                path=str(board),
                details={"unconnected": post_import_unconnected},
            )
            failure_payload = {
                "status": "fail",
                "mode": "zone_connected_planes_freerouting",
                "plane_connectivity": "incomplete",
                "zone_fill": "persisted" if zone_count else "not_required",
                "zone_count": zone_count,
                "filled_polygon_count": filled_polygon_count,
                "zone_nets": source_routing.get("zone_nets", []),
                "signal_routing": "complete",
                "design_rules": _routing_rules_payload(project_rules),
                "project_sidecar_promoted": project_sidecar_promoted,
                "freerouting_version": self.VERSION,
                "freerouting_unrouted": unrouted,
                "unrouted": post_import_unconnected,
                "post_import_unconnected": post_import_unconnected,
                "violations": 0,
                "max_passes": max_passes,
                "failures": [routing_failure.__dict__],
                "board_sha256": hashlib.sha256(board.read_bytes()).hexdigest(),
            }
            write_json(routing_report, failure_payload)
            return GateReport(
                "autoroute",
                Status.FAIL,
                [routing_failure],
                metrics={
                    "unrouted": post_import_unconnected,
                    "freerouting_unrouted": unrouted,
                    "max_passes": max_passes,
                    "zone_count": zone_count,
                    "filled_polygon_count": filled_polygon_count,
                },
                artifacts=[str(board), str(dsn), str(ses), str(routing_report)],
                backend={**self._backend(command, completed.returncode, tools, log), "timeout_seconds": timeout_seconds},
            )
        write_json(routing_report, {
            "status": "pass",
            "mode": "zone_connected_planes_freerouting",
            "plane_connectivity": "copper_zones",
            "zone_fill": "persisted" if zone_count else "not_required",
            "zone_count": zone_count,
            "filled_polygon_count": filled_polygon_count,
            "zone_nets": source_routing.get("zone_nets", []),
            "signal_routing": "complete",
            "design_rules": _routing_rules_payload(project_rules),
            "project_sidecar_promoted": project_sidecar_promoted,
            "freerouting_version": self.VERSION,
            "freerouting_unrouted": unrouted,
            "unrouted": 0,
            "post_import_unconnected": 0,
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
            metrics={
                "unrouted": 0,
                "freerouting_unrouted": unrouted,
                "max_passes": max_passes,
                "zone_count": zone_count,
                "filled_polygon_count": filled_polygon_count,
            },
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
    def _pcbnew(executable: Path, code: str, *arguments: Path | str) -> subprocess.CompletedProcess[str]:
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


def _project_routing_rules(project_file: Path) -> tuple[float, float] | None:
    """Read generated KiCad routing minima, retaining legacy fallback if no project exists."""
    if not project_file.exists():
        return None
    try:
        payload = json.loads(project_file.read_text(encoding="utf-8"))
        rules = payload["board"]["design_settings"]["rules"]
    except (KeyError, TypeError) as exc:
        raise ValueError("missing board.design_settings.rules") from exc

    values: list[float] = []
    for name in ("min_clearance", "min_track_width"):
        value = rules.get(name) if isinstance(rules, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a numeric millimetre value")
        parsed = float(value)
        if not math.isfinite(parsed) or not _MIN_ROUTING_RULE_MM <= parsed <= _MAX_ROUTING_RULE_MM:
            raise ValueError(
                f"{name} must be finite and between {_MIN_ROUTING_RULE_MM:g} and {_MAX_ROUTING_RULE_MM:g} mm"
            )
        values.append(parsed)
    return values[0], values[1]


def _routing_rules_payload(rules: tuple[float, float] | None) -> dict[str, float] | None:
    if rules is None:
        return None
    return {"min_clearance_mm": rules[0], "min_track_width_mm": rules[1]}


def _cached_incomplete_plane_failure(
    source_routing: dict[str, object],
    *,
    board: Path,
    board_sha256: str,
    project_rules: tuple[float, float] | None,
    zone_count: int,
    filled_polygon_count: int,
    default_version: str,
) -> GateReport | None:
    """Reuse only an authoritative, board-bound post-fill connectivity failure."""
    post_import_unconnected = source_routing.get("post_import_unconnected")
    recorded_zone_count = source_routing.get("zone_count")
    recorded_filled_polygon_count = source_routing.get("filled_polygon_count")
    recorded_failures = source_routing.get("failures")
    if (
        source_routing.get("status") != "fail"
        or source_routing.get("signal_routing") != "complete"
        or source_routing.get("plane_connectivity") != "incomplete"
        or source_routing.get("board_sha256") != board_sha256
        or source_routing.get("design_rules") != _routing_rules_payload(project_rules)
        or source_routing.get("zone_fill") != "persisted"
        or not _positive_int(post_import_unconnected)
        or source_routing.get("unrouted") != post_import_unconnected
        or source_routing.get("violations") != 0
        or not _positive_int(recorded_zone_count)
        or not _positive_int(recorded_filled_polygon_count)
        or recorded_zone_count != zone_count
        or recorded_filled_polygon_count != filled_polygon_count
        or not isinstance(recorded_failures, list)
    ):
        return None
    matching_failure = next(
        (
            item
            for item in recorded_failures
            if isinstance(item, dict)
            and item.get("category") == FailureCategory.EDA_ERROR.value
            and item.get("code") == "routing_incomplete_after_zone_fill"
            and isinstance(item.get("details"), dict)
            and item["details"].get("unconnected") == post_import_unconnected
        ),
        None,
    )
    if matching_failure is None:
        return None

    failure = Failure(
        FailureCategory.EDA_ERROR,
        "routing_incomplete_after_zone_fill",
        f"KiCad found {post_import_unconnected} unconnected item(s) after session import and zone fill",
        path=str(board),
        details={"unconnected": post_import_unconnected},
    )
    return GateReport(
        "autoroute",
        Status.FAIL,
        [failure],
        metrics={
            "unrouted": post_import_unconnected,
            "max_passes": source_routing.get("max_passes"),
            "cached": True,
            "zone_count": zone_count,
            "filled_polygon_count": filled_polygon_count,
        },
        artifacts=[str(board), str(board.parent / "routing.json")],
        backend={
            "name": "freerouting",
            "version": source_routing.get("freerouting_version", default_version),
            "cached": True,
        },
    )


def _positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _promote_routed_project(
    routed_project: Path,
    canonical_project: Path,
    expected_rules: tuple[float, float] | None,
) -> bool:
    if not routed_project.is_file():
        return False
    payload = json.loads(routed_project.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("KiCad routed project sidecar must contain a JSON object")
    if expected_rules is not None:
        routed_rules = _project_routing_rules(routed_project)
        default_rules = _project_default_netclass_rules(payload)
        if routed_rules != expected_rules or default_rules != expected_rules:
            raise ValueError(
                "KiCad routed project sidecar does not preserve the requested clearance and track width"
            )
    if canonical_project.is_file():
        canonical_payload = json.loads(canonical_project.read_text(encoding="utf-8"))
        if not isinstance(canonical_payload, dict):
            raise ValueError("canonical KiCad project must contain a JSON object")
        net_settings = payload.get("net_settings")
        if not isinstance(net_settings, dict):
            raise ValueError("KiCad routed project sidecar has invalid net_settings")
        canonical_payload["net_settings"] = net_settings
        payload = canonical_payload
    meta = payload.setdefault("meta", {})
    if not isinstance(meta, dict):
        raise ValueError("KiCad routed project sidecar has invalid meta data")
    meta["filename"] = canonical_project.name
    write_json(canonical_project, payload)
    routed_project.unlink()
    return True


def _project_default_netclass_rules(payload: dict[str, object]) -> tuple[float, float]:
    net_settings = payload.get("net_settings")
    classes = net_settings.get("classes") if isinstance(net_settings, dict) else None
    if not isinstance(classes, list):
        raise ValueError("missing net_settings Default netclass")
    default = next(
        (item for item in classes if isinstance(item, dict) and item.get("name") == "Default"),
        None,
    )
    if default is None:
        raise ValueError("missing net_settings Default netclass")
    try:
        raw_values = (default["clearance"], default["track_width"])
    except KeyError as exc:
        raise ValueError("Default netclass is missing clearance or track_width") from exc
    values: list[float] = []
    for name, value in zip(("clearance", "track_width"), raw_values, strict=True):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Default netclass {name} must be numeric")
        parsed = float(value)
        if not math.isfinite(parsed) or not _MIN_ROUTING_RULE_MM <= parsed <= _MAX_ROUTING_RULE_MM:
            raise ValueError(f"Default netclass {name} is outside the supported routing-rule bounds")
        values.append(parsed)
    return values[0], values[1]


def _zone_fill_counts(board_text: str) -> tuple[int, int]:
    zone_count = len(re.findall(r"(?m)^\s*\(zone(?:\s*$|\s+\()", board_text))
    filled_polygon_count = len(re.findall(r"(?m)^\s*\(filled_polygon(?:\s*$|\s+\()", board_text))
    return zone_count, filled_polygon_count
