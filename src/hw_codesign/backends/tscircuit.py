from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ..io import atomic_write_text, write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..provenance import artifact_provenance


class TSCircuitBackend:
    VERSION = "0.1.1491"

    def __init__(self, platform_root: Path):
        self.platform_root = platform_root

    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        target = project / "electronics" / "source" / "tscircuit"
        target.mkdir(parents=True, exist_ok=True)
        components = []
        esm_components = []
        for item in graph.get("components", []):
            labels = {f"pin{pin['number']}": f"{self._identifier(pin['name'])}_{pin['number']}" for pin in item.get("pins", [])}
            connections = {f"pin{pin['number']}": f"sel.net.{self._identifier(pin['net'])}" for pin in item.get("pins", [])}
            labels_js = json.dumps(labels, sort_keys=True)
            conn_js = "{" + ", ".join(f"{json.dumps(key)}: {value}" for key, value in connections.items()) + "}"
            components.append(f'      <chip name={json.dumps(item["ref"])} pinLabels={{{labels_js}}} connections={{{conn_js}}} />')
            esm_components.append(f'    React.createElement("chip", {{ name: {json.dumps(item["ref"])}, pinLabels: {labels_js}, connections: {conn_js} }})')
        envelope = spec["mechanical"]["envelope"]
        source = "import React from \"react\"\nimport { sel } from \"tscircuit\"\n\nexport default () => (\n" + f'  <board name="RobotController" width="{envelope["board_width_mm"]}mm" height="{envelope["board_height_mm"]}mm" pcbDisabled routingDisabled>\n' + "\n".join(components) + "\n  </board>\n)\n"
        entry = target / "board.tsx"
        atomic_write_text(entry, source)
        compiler_entry = target / "board.compiler.mjs"
        esm = "import React from \"react\"\nimport { sel } from \"tscircuit\"\n\nexport default () => React.createElement(\n  \"board\",\n  { name: \"RobotController\", pcbDisabled: true, routingDisabled: true },\n" + ",\n".join(esm_components) + "\n)\n"
        atomic_write_text(compiler_entry, esm)
        write_json(target / "source_manifest.json", {"backend": "tscircuit", "compiler_version": self.VERSION, "provenance": artifact_provenance(spec, self.platform_root / "parts", "tscircuit", compiler_version=self.VERSION, command=self.command(entry), release_eligible=True)})
        return [str(entry), str(compiler_entry), str(target / "source_manifest.json")]

    def command(self, entry: Path) -> list[str]:
        compiler_entry = entry.with_name("board.compiler.mjs")
        return [str(self.platform_root / "node_modules" / ".bin" / "tsx"), str(self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js"), "build", str(compiler_entry), "--ignore-config", "--disable-pcb", "--routing-disabled", "--disable-parts-engine"]

    def compile(self, project: Path, graph: dict[str, Any]) -> list[GateReport]:
        entry = project / "electronics" / "source" / "tscircuit" / "board.tsx"
        cli = self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js"
        if shutil.which("node") is None or not cli.is_file() or not (self.platform_root / "node_modules" / ".bin" / "tsx").is_file():
            failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "Pinned Node.js tscircuit CLI is unavailable; run npm ci")
            return [GateReport(name, Status.BLOCKED, [failure], backend={"name": "tscircuit", "version": self.VERSION, "offline": True}) for name in ("tscircuit_compile", "tscircuit_netlist_extract", "tscircuit_graph_parity")]
        if not entry.is_file():
            failure = Failure(FailureCategory.EDA_ERROR, "missing_design_source", "Generate tscircuit source before compilation")
            return [GateReport(name, Status.BLOCKED, [failure]) for name in ("tscircuit_compile", "tscircuit_netlist_extract", "tscircuit_graph_parity")]
        shutil.rmtree(entry.parent / "dist", ignore_errors=True)
        result = subprocess.run(self.command(entry), cwd=entry.parent, capture_output=True, text=True, timeout=600)
        backend = {"name": "tscircuit", "version": self.VERSION, "offline": True, "command": self.command(entry), "returncode": result.returncode, "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]}
        if result.returncode != 0:
            failure = Failure(FailureCategory.EDA_ERROR, "tscircuit_compile_failed", "Pinned tscircuit compiler returned nonzero", details={"returncode": result.returncode, "stderr": result.stderr[-2000:]})
            return [GateReport("tscircuit_compile", Status.FAIL, [failure], backend=backend), GateReport("tscircuit_netlist_extract", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "compile_prerequisite_failed", "Netlist extraction requires successful compile")]), GateReport("tscircuit_graph_parity", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "netlist_prerequisite_failed", "Graph parity requires a compiled netlist")])]
        candidates = sorted([*entry.parent.rglob("*.circuit.json"), *entry.parent.rglob("circuit.json")], key=lambda p: p.stat().st_mtime, reverse=True)
        candidates.extend(sorted((self.platform_root / "dist").rglob("circuit.json"), key=lambda p: p.stat().st_mtime, reverse=True) if (self.platform_root / "dist").is_dir() else [])
        if not candidates:
            failure = Failure(FailureCategory.EDA_ERROR, "compiled_netlist_missing", "tscircuit completed without a Circuit JSON output")
            return [GateReport("tscircuit_compile", Status.PASS, backend=backend), GateReport("tscircuit_netlist_extract", Status.FAIL, [failure]), GateReport("tscircuit_graph_parity", Status.BLOCKED, [failure])]
        compiled_path = candidates[0]
        compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
        netlist = self.extract_netlist(compiled)
        netlist_path = project / "electronics" / "generated" / "tscircuit_netlist.json"
        write_json(netlist_path, netlist)
        expected = self.graph_netlist(graph)
        parity_failures = [] if netlist == expected else [Failure(FailureCategory.EDA_ERROR, "graph_parity_mismatch", "Python resolved graph differs from compiled tscircuit netlist", details={"expected": expected, "compiled": netlist})]
        return [GateReport("tscircuit_compile", Status.PASS, metrics={"circuit_elements": len(compiled)}, artifacts=[str(compiled_path)], backend=backend), GateReport("tscircuit_netlist_extract", Status.PASS, metrics={"nets": len(netlist)}, artifacts=[str(netlist_path)], backend=backend), GateReport("tscircuit_graph_parity", Status.FAIL if parity_failures else Status.PASS, parity_failures, metrics={"expected_nets": len(expected), "compiled_nets": len(netlist)}, backend=backend)]

    @staticmethod
    def _identifier(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9_]", "_", value)

    @staticmethod
    def graph_netlist(graph: dict[str, Any]) -> dict[str, list[str]]:
        return {item["name"]: sorted(item.get("connected_pins", [])) for item in graph.get("nets", [])}

    @staticmethod
    def extract_netlist(circuit_json: list[dict[str, Any]]) -> dict[str, list[str]]:
        source_components = {item.get("source_component_id"): item.get("name") for item in circuit_json if item.get("source_component_id") and item.get("name")}
        ports = {item.get("source_port_id"): (source_components.get(item.get("source_component_id")), str(item.get("pin_number") or item.get("name", "")).removeprefix("pin")) for item in circuit_json if item.get("type") == "source_port"}
        net_objects = {item.get("source_net_id"): item.get("name") for item in circuit_json if item.get("type") == "source_net"}
        nets: dict[str, set[str]] = {}
        for item in circuit_json:
            if item.get("type") != "source_trace": continue
            net_ids = item.get("connected_source_net_ids") or []
            name = net_objects.get(net_ids[0]) if net_ids else None
            if not name: continue
            for port_id in item.get("connected_source_port_ids") or []:
                ref, number = ports.get(port_id, (None, None))
                if ref and number: nets.setdefault(name, set()).add(f"{ref}.{number}")
        return {name: sorted(values) for name, values in sorted(nets.items())}
