from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from ..artifacts import deterministic_zip
from ..io import atomic_write_text, write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..provenance import artifact_provenance
from .command import resolve_kicad_python, resolve_tool, run_tool
from .electronics import ElectronicsBackendAdapter

# Footprint library directories, tried in order
_FP_LIB_CANDIDATES = [
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints",  # macOS bundle
    "/usr/share/kicad/footprints",                                        # Linux system
]

# Compact pcbnew script: reads JSON from stdin, writes .kicad_pcb to sys.argv[1]
_PCBNEW_GEN = r"""
import pcbnew, json, math, os, sys
data = json.loads(sys.stdin.read())
nets_data = data["nets"]
fps_data = data["footprints"]
w = data.get("width_mm", 100); h = data.get("height_mm", 80)
board = pcbnew.BOARD()
seg = pcbnew.PCB_SHAPE(board); seg.SetShape(pcbnew.SHAPE_T_RECT); seg.SetLayer(pcbnew.Edge_Cuts)
seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(0)))
seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(w), pcbnew.FromMM(h))); board.Add(seg)
net_obj = {}
for nn in nets_data:
    n = pcbnew.NETINFO_ITEM(board, nn); board.Add(n); net_obj[nn] = n
pin_net = {p: nn for nn, ps in nets_data.items() for p in ps}
fp_dir = next((d for d in """ + repr(_FP_LIB_CANDIDATES) + r""" if os.path.isdir(d)), None)
n_fps = max(1, len(fps_data)); cols = max(1, int(math.ceil(math.sqrt(n_fps)))); placed = 0
for i, (ref, meta) in enumerate(fps_data.items()):
    lib_id = meta.get("library_id", "")
    if ":" not in lib_id or fp_dir is None: continue
    lib, fpn = lib_id.rsplit(":", 1); lp = os.path.join(fp_dir, lib + ".pretty")
    if not os.path.isdir(lp): continue
    try: fp = pcbnew.FootprintLoad(lp, fpn)
    except Exception: continue
    if fp is None: continue
    col = i % cols; row = i // cols
    fp.SetReference(ref); fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(5 + col * 15), pcbnew.FromMM(5 + row * 15)))
    for pad in fp.Pads():
        nm = pin_net.get(f"{ref}.{pad.GetNumber()}")
        if nm and nm in net_obj: pad.SetNet(net_obj[nm])
    board.Add(fp); placed += 1
pcbnew.SaveBoard(sys.argv[1], board); print(f"placed={placed}")
"""


class PythonNetlistBackend(ElectronicsBackendAdapter):
    name = "python_netlist"

    def __init__(self, platform_root: Path):
        self.platform_root = platform_root

    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        target = project / "electronics" / "source" / self.name
        target.mkdir(parents=True, exist_ok=True)
        source = target / "design.py"
        compiled = target / "compiled_netlist.json"
        payload = {
            "nets": self.graph_netlist(graph),
            "footprints": {component["ref"]: component.get("footprint_metadata", {}) for component in graph.get("components", [])},
        }
        atomic_write_text(source, "import json\nfrom pathlib import Path\n\nPAYLOAD = " + repr(payload) + "\nPath(__file__).with_name('compiled_netlist.json').write_text(json.dumps(PAYLOAD, sort_keys=True, indent=2) + '\\n', encoding='utf-8')\n")
        manifest = target / "source_manifest.json"
        write_json(manifest, {
            "backend": self.name,
            "backend_release_capable": True,
            "source_release_eligible": True,
            "release_tier": "fabrication",
            "sources": self.source_entries(target, [source]),
            "contract_gates": list(self.gate_names),
            "release_blocking_gates": [
                f"{self.name}_compile",
                f"{self.name}_netlist_extract",
                f"{self.name}_graph_parity",
                f"{self.name}_footprint_parity",
            ],
            "provenance": artifact_provenance(spec, self.platform_root / "parts", self.name, compiler_version=sys.version.split()[0], command=[sys.executable, str(source)], release_eligible=True),
        })
        compiled.unlink(missing_ok=True)
        return [str(source), str(manifest)]

    def evaluate(self, project: Path, graph: dict[str, Any]) -> list[GateReport]:
        source = project / "electronics" / "source" / self.name / "design.py"
        output = source.with_name("compiled_netlist.json")
        if not source.is_file():
            return self.blocked_contract("missing_design_source", "Generate Python netlist source before evaluation", category=FailureCategory.EDA_ERROR)
        result = subprocess.run([sys.executable, str(source)], capture_output=True, text=True, timeout=60)
        backend = {"name": self.name, "command": [sys.executable, str(source)], "returncode": result.returncode}
        if result.returncode != 0:
            failure = Failure(FailureCategory.EDA_ERROR, "python_netlist_compile_failed", "Python netlist source returned nonzero", details={"stderr": result.stderr[-2000:]})
            return self.complete_contract([GateReport(f"{self.name}_compile", Status.FAIL, [failure], backend=backend)])
        if not output.is_file():
            failure = Failure(FailureCategory.EDA_ERROR, "compiled_netlist_missing", "Python backend did not emit compiled_netlist.json")
            return self.complete_contract([GateReport(f"{self.name}_compile", Status.PASS, backend=backend), GateReport(f"{self.name}_netlist_extract", Status.FAIL, [failure], backend=backend)])
        compiled = json.loads(output.read_text(encoding="utf-8"))
        parity_failures = [] if compiled.get("nets") == self.graph_netlist(graph) else [Failure(FailureCategory.EDA_ERROR, "graph_parity_mismatch", "Python compiled netlist differs from resolved graph")]
        footprint_failures = []
        for component in graph.get("components", []):
            if compiled.get("footprints", {}).get(component["ref"]) != component.get("footprint_metadata", {}):
                footprint_failures.append(Failure(FailureCategory.EDA_ERROR, "footprint_parity_mismatch", f"Footprint metadata differs for {component['ref']}"))
        fab_dir = project / "exports" / "candidates" / "backend-validation" / self.name
        fab_reports = self._fabrication_gates(project, compiled, fab_dir)
        return self.complete_contract([
            GateReport(f"{self.name}_compile", Status.PASS, artifacts=[str(output)], backend=backend),
            GateReport(f"{self.name}_netlist_extract", Status.PASS, artifacts=[str(output)], backend=backend),
            GateReport(f"{self.name}_graph_parity", Status.FAIL if parity_failures else Status.PASS, parity_failures, backend=backend),
            GateReport(f"{self.name}_footprint_parity", Status.FAIL if footprint_failures else Status.PASS, footprint_failures, backend=backend),
            *fab_reports,
        ])

    def export_manufacturing(self, project: Path, release: Path) -> GateReport:
        """Generate fabrication artifacts into release directory, for use in prepare_release."""
        compiled_path = project / "electronics" / "source" / self.name / "compiled_netlist.json"
        if not compiled_path.is_file():
            return GateReport(
                f"{self.name}_manufacturing_export",
                Status.BLOCKED,
                [Failure(FailureCategory.EDA_ERROR, "compiled_netlist_missing", "Run evaluate with python_netlist backend first")],
                backend={"name": self.name},
            )
        compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
        return self._fabrication_gates(project, compiled, release, gate_name=f"{self.name}_manufacturing_export")[1]

    def _fabrication_gates(self, project: Path, compiled: dict[str, Any], fab_dir: Path, *, gate_name: str | None = None) -> list[GateReport]:
        """Return [layout_completeness, manufacturing_export] gate reports."""
        kicad_py = resolve_kicad_python()
        kicad_cli = resolve_tool("kicad-cli")
        if kicad_py is None or kicad_cli is None:
            blocked = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "KiCad toolchain not available; install KiCad to enable PCB fabrication output")
            return [
                GateReport(f"{self.name}_layout_completeness", Status.BLOCKED, [blocked], backend={"name": self.name}),
                GateReport(gate_name or f"{self.name}_manufacturing_export", Status.BLOCKED, [blocked], backend={"name": self.name}),
            ]

        pcb_path = project / "electronics" / "generated" / "python_netlist_board.kicad_pcb"
        gen_result = self._run_pcbnew_gen(compiled, pcb_path, Path(kicad_py))
        if gen_result.returncode != 0 or not pcb_path.is_file():
            fail = Failure(FailureCategory.TOOL_ERROR, "pcbnew_gen_failed", "pcbnew failed to generate KiCad PCB from compiled netlist", details={"stderr": gen_result.stderr[-2000:], "stdout": gen_result.stdout[-2000:]})
            return [
                GateReport(f"{self.name}_layout_completeness", Status.FAIL, [fail], backend={"name": self.name}),
                GateReport(gate_name or f"{self.name}_manufacturing_export", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "gate_not_run", "PCB generation failed")], backend={"name": self.name}),
            ]

        board_text = pcb_path.read_text(encoding="utf-8")
        placed_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', board_text))
        expected_refs = set(compiled.get("footprints", {}).keys())
        layout_failures: list[Failure] = []
        for ref in sorted(expected_refs - placed_refs):
            layout_failures.append(Failure(FailureCategory.EDA_ERROR, "component_unplaced", f"{ref} could not be placed (footprint library not found)"))
        if not re.search(r"\((?:segment|arc|via)\s", board_text):
            layout_failures.append(Failure(FailureCategory.EDA_ERROR, "pcb_traces_absent", "Generated PCB has no routed traces — board is placed only, not routed"))
        layout_report = GateReport(f"{self.name}_layout_completeness", Status.FAIL if layout_failures else Status.PASS, layout_failures, artifacts=[str(pcb_path)], backend={"name": self.name, "pcbnew": True})

        mfg_report = self._kicad_export(project, pcb_path, fab_dir, compiled, kicad_cli, gate_name=gate_name or f"{self.name}_manufacturing_export")
        return [layout_report, mfg_report]

    def _run_pcbnew_gen(self, compiled: dict[str, Any], pcb_out: Path, kicad_py: Path) -> subprocess.CompletedProcess[str]:
        pcb_out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(_PCBNEW_GEN)
            script = f.name
        try:
            return subprocess.run(
                [str(kicad_py), script, str(pcb_out)],
                input=json.dumps(compiled),
                capture_output=True, text=True, timeout=120,
            )
        finally:
            os.unlink(script)

    def _kicad_export(self, project: Path, pcb_path: Path, fab_dir: Path, compiled: dict[str, Any], kicad_cli: str, *, gate_name: str) -> GateReport:
        native = fab_dir / "fabrication" / "native_python_netlist"
        shutil.rmtree(native, ignore_errors=True)
        native.mkdir(parents=True)

        gerber = run_tool("kicad-cli", ["pcb", "export", "gerbers", "--output", str(native), "--layers", "F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts", str(pcb_path)], project)
        if not gerber.available or gerber.returncode != 0:
            fail = Failure(FailureCategory.EDA_ERROR, "gerber_export_failed", "kicad-cli gerber export failed", details={"stderr": gerber.stderr[-2000:]})
            return GateReport(gate_name, Status.FAIL if gerber.available else Status.BLOCKED, [fail], backend={"name": self.name, "kicad_cli": True})

        drill = run_tool("kicad-cli", ["pcb", "export", "drill", "--output", str(native), str(pcb_path)], project)
        if drill.returncode != 0:
            fail = Failure(FailureCategory.EDA_ERROR, "drill_export_failed", "kicad-cli drill export failed")
            return GateReport(gate_name, Status.FAIL, [fail], backend={"name": self.name})

        pos_csv = native / "positions.csv"
        pos = run_tool("kicad-cli", ["pcb", "export", "pos", "--format", "csv", "--units", "mm", "--output", str(pos_csv), str(pcb_path)], project)
        if pos.returncode != 0 or not pos_csv.is_file():
            fail = Failure(FailureCategory.EDA_ERROR, "position_export_failed", "kicad-cli position export failed")
            return GateReport(gate_name, Status.FAIL, [fail], backend={"name": self.name})

        gerbers = [(item, item.name) for item in native.iterdir() if item.suffix.lower() not in {".drl", ".xln", ".pdf"} and item != pos_csv]
        drills = [(item, item.name) for item in native.iterdir() if item.suffix.lower() in {".drl", ".xln"}]
        if not gerbers:
            fail = Failure(FailureCategory.EDA_ERROR, "manufacturing_files_missing", "kicad-cli produced no Gerber files")
            return GateReport(gate_name, Status.FAIL, [fail], backend={"name": self.name})

        fab = fab_dir / "fabrication"
        fab.mkdir(parents=True, exist_ok=True)
        deterministic_zip(fab / "gerbers.zip", gerbers)
        if drills:
            deterministic_zip(fab / "drill.zip", drills)
        shutil.copy2(pos_csv, fab / "pick_and_place.csv")

        bom_rows = ["Reference,Footprint,Value"]
        for ref, meta in compiled.get("footprints", {}).items():
            fp = meta.get("library_id", "")
            bom_rows.append(f"{ref},{fp},")
        (fab / "bom.csv").write_text("\n".join(bom_rows) + "\n", encoding="utf-8")

        artifacts = [str(fab / "gerbers.zip"), str(fab / "pick_and_place.csv"), str(fab / "bom.csv")]
        if drills:
            artifacts.append(str(fab / "drill.zip"))
        return GateReport(gate_name, Status.PASS, [], artifacts=artifacts, metrics={"gerber_files": len(gerbers), "drill_files": len(drills), "release_tier": "fabrication"}, backend={"name": self.name, "kicad_cli": True, "pcbnew": True})
