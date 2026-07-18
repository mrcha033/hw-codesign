from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

import pytest

from hw_codesign.artifacts import sha256
from hw_codesign.backends import command as backend_command
from hw_codesign.backends.command import ToolResult
from hw_codesign.backends.electronics import CONTRACT_STAGES
from hw_codesign.backends.tscircuit import TSCircuitBackend
from hw_codesign.io import read_yaml, write_yaml
from hw_codesign.models import GateReport, Status


def _set_backend(service, project: str, backend: str) -> None:
    path = service.workspace.require_project(project) / "spec" / "system.yaml"
    payload = read_yaml(path)
    payload["electronics"]["backend"] = backend
    write_yaml(path, payload)


@pytest.mark.parametrize("backend_name", ["tscircuit", "kicad", "python_netlist", "atopile"])
def test_backend_adapters_emit_manifest_with_same_contract(service, project, backend_name):
    _set_backend(service, project, backend_name)
    service.generate_electronics_only(project)
    source = service.workspace.require_project(project) / "electronics" / "source" / backend_name
    manifest = json.loads((source / "source_manifest.json").read_text(encoding="utf-8"))
    release_tiers = {
        "tscircuit": "fabrication",
        "kicad": "fabrication",
        "python_netlist": "netlist",
        "atopile": "hdl_source",
    }
    assert manifest["backend"] == backend_name
    assert manifest["release_tier"] == release_tiers[backend_name]
    assert manifest["provenance"]["release_tier"] == release_tiers[backend_name]
    assert manifest["contract_gates"] == [f"{backend_name}_{stage}" for stage in CONTRACT_STAGES]
    assert set(manifest["release_blocking_gates"]).issubset(set(manifest["contract_gates"]))
    assert {"netlist_release_eligible", "hdl_source_release_eligible", "fabrication_release_eligible"} <= set(manifest)
    assert manifest["sources"]
    assert all(len(entry["sha256"]) == 64 for entry in manifest["sources"])
    assert all((source / entry["path"]).is_file() for entry in manifest["sources"])


def test_python_netlist_compile_and_parity_gates_pass(service, project):
    _set_backend(service, project, "python_netlist")
    service.generate_electronics_only(project)
    checks = service.run_all_checks(project, include_external=False)
    reports = {item["gate"]: item for item in checks["reports"]}
    for stage in ("compile", "netlist_extract", "graph_parity", "footprint_parity"):
        assert reports[f"python_netlist_{stage}"]["status"] == "pass"
    # Layout and manufacturing are not applicable to the netlist release tier.
    assert reports["python_netlist_layout_completeness"]["status"] == "blocked"
    assert reports["python_netlist_manufacturing_export"]["status"] == "blocked"


def test_missing_kicad_tool_blocks_every_contract_gate(service, project, monkeypatch):
    _set_backend(service, project, "kicad")
    service.generate_electronics_only(project)
    monkeypatch.setattr("hw_codesign.backends.kicad.resolve_tool", lambda _: None)
    graph_path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
    reports = service.kicad.evaluate(service.workspace.require_project(project), json.loads(graph_path.read_text(encoding="utf-8")))
    assert [report.gate for report in reports] == [f"kicad_{stage}" for stage in CONTRACT_STAGES]
    assert all(report.status == "blocked" for report in reports)
    assert all(report.failures[0].code == "tool_unavailable" for report in reports)


def test_tscircuit_timeout_is_bounded_and_reported(tmp_path, monkeypatch):
    project = tmp_path / "project"
    source = project / "electronics" / "source" / "tscircuit"
    source.mkdir(parents=True)
    (source / "board.tsx").write_text("export default () => null\n", encoding="utf-8")
    (source / "board.compiler.mjs").write_text("export default () => null\n", encoding="utf-8")
    cli = tmp_path / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js"
    cli.parent.mkdir(parents=True)
    cli.write_text("", encoding="utf-8")
    tsx = tmp_path / "node_modules" / ".bin" / ("tsx.cmd" if sys.platform == "win32" else "tsx")
    tsx.parent.mkdir(parents=True)
    tsx.write_text("", encoding="utf-8")
    observed = {}

    monkeypatch.setattr("hw_codesign.backends.tscircuit.shutil.which", lambda _: "/usr/bin/node")

    def fake_run(command, **kwargs):
        observed["timeout"] = kwargs["timeout"]
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output="partial", stderr="still running")

    monkeypatch.setattr("hw_codesign.backends.tscircuit.subprocess.run", fake_run)

    reports = TSCircuitBackend(tmp_path).compile(project, {}, timeout_seconds=4)
    compile_report = reports[0]

    assert observed["timeout"] == 4
    assert compile_report.gate == "tscircuit_compile"
    assert compile_report.status.value == "blocked"
    assert compile_report.failures[0].code == "tool_timeout"
    assert compile_report.failures[0].details["timeout_seconds"] == 4
    assert compile_report.backend["timeout_seconds"] == 4


def test_tscircuit_source_uses_solver_coordinates(service, project):
    _set_backend(service, project, "tscircuit")
    service.generate_electronics_only(project)
    project_path = service.workspace.require_project(project)
    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    component = next(item for item in graph["components"] if item["ref"] == "U1")
    width = float(graph["placement"]["board_width_mm"])
    height = float(graph["placement"]["board_height_mm"])
    expected_x = float(component["pcb_position_mm"][0]) - width / 2.0
    expected_y = float(component["pcb_position_mm"][1]) - height / 2.0
    expected_rotation = float(component["pcb_rotation_deg"])
    source = project_path / "electronics" / "source" / "tscircuit"
    tsx_line = next(line for line in (source / "board.tsx").read_text(encoding="utf-8").splitlines() if 'name="U1"' in line)
    compiler_line = next(line for line in (source / "board.compiler.mjs").read_text(encoding="utf-8").splitlines() if 'name: "U1"' in line)
    manifest = json.loads((source / "source_manifest.json").read_text(encoding="utf-8"))

    assert f"pcbX={{{expected_x:.3f}}}" in tsx_line
    assert f"pcbY={{{expected_y:.3f}}}" in tsx_line
    assert f"pcbRotation={{{expected_rotation:.3f}}}" in tsx_line
    assert f"pcbX: {expected_x:.3f}" in compiler_line
    assert f"pcbY: {expected_y:.3f}" in compiler_line
    assert f"pcbRotation: {expected_rotation:.3f}" in compiler_line
    assert manifest["placement_contract"]["source"] == "electrical_graph.components[].pcb_position_mm + pcb_rotation_deg"
    assert manifest["placement_contract"]["missing_solver_placements"] == []
    assert manifest["placement_contract"]["solver_placements"] == len(graph["components"])


def test_tscircuit_source_refreshes_after_agent_placement(service, project):
    _set_backend(service, project, "tscircuit")
    service.generate_electronics_only(project)
    project_path = service.workspace.require_project(project)
    source_path = project_path / "electronics" / "source" / "tscircuit" / "board.tsx"
    before = source_path.read_text(encoding="utf-8")

    result = service.set_placement_constraint(project, {
        "ref": "R1",
        "relationship": "adjacent_to",
        "target": "U1",
        "max_distance_mm": 5.0,
    })

    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    component = next(item for item in graph["components"] if item["ref"] == "R1")
    expected_x = float(component["pcb_position_mm"][0]) - float(graph["placement"]["board_width_mm"]) / 2.0
    expected_y = float(component["pcb_position_mm"][1]) - float(graph["placement"]["board_height_mm"]) / 2.0
    after = source_path.read_text(encoding="utf-8")
    line = next(line for line in after.splitlines() if 'name="R1"' in line)

    assert result["status"] == "pass"
    assert result["regenerated_sources"]
    assert after != before
    assert f"pcbX={{{expected_x:.3f}}}" in line
    assert f"pcbY={{{expected_y:.3f}}}" in line


def test_tscircuit_manifest_blocks_missing_solver_placements(tmp_path):
    project = tmp_path / "project"
    spec = {"mechanical": {"envelope": {"board_width_mm": 40.0, "board_height_mm": 30.0}}}
    graph = {
        "components": [{
            "ref": "R1",
            "footprint_metadata": {
                "library_id": "Resistor_SMD:R_0603_1608Metric",
                "backend_footprints": {"tscircuit": "0603"},
            },
            "pins": [],
        }],
    }

    TSCircuitBackend(tmp_path).generate_source(project, spec, graph)
    manifest = json.loads((project / "electronics" / "source" / "tscircuit" / "source_manifest.json").read_text(encoding="utf-8"))

    assert manifest["source_release_eligible"] is False
    assert manifest["fabrication_release_eligible"] is False
    assert manifest["placement_contract"]["missing_solver_placements"] == ["R1"]


def test_tscircuit_canonical_usb_footprint_uses_numeric_backend_pin_aliases(tmp_path):
    footprint = "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal"
    pin_numbers = [
        "A1", "A4", "A5", "A6", "A7", "A8", "A9", "A12",
        "B1", "B4", "B5", "B6", "B7", "B8", "B9", "B12", "SH",
    ]
    component = {
        "ref": "J1",
        "footprint": footprint,
        "footprint_metadata": {"library_id": footprint, "expected_pads": pin_numbers},
        "pcb_position_mm": [10.0, 10.0],
        "pcb_rotation_deg": 0.0,
        "pins": [
            {"number": number, "name": f"PAD_{number}", "net": "GND" if number in {"A1", "SH"} else None}
            for number in pin_numbers
        ],
    }
    graph_to_backend, backend_to_graph = TSCircuitBackend._pin_number_maps(component, footprint)
    canonical = TSCircuitBackend._canonical_footprint_elements(footprint, graph_to_backend)

    assert graph_to_backend == {number: str(index) for index, number in enumerate(pin_numbers, start=1)}
    assert backend_to_graph["1"] == "A1"
    assert backend_to_graph["17"] == "SH"
    assert canonical is not None
    elements, footprint_hash = canonical
    assert len(elements) == 22  # 16 contacts, four shield stakes, two locating holes
    assert len(footprint_hash) == 64
    assert any(name == "smtpad" and props.get("portHints") == ["pin1", "A1"] for name, props in elements)
    assert sum(name == "platedhole" and props.get("portHints") == ["pin17", "SH"] for name, props in elements) == 4

    spec = {"mechanical": {"envelope": {"board_width_mm": 40.0, "board_height_mm": 30.0}}}
    project = tmp_path / "canonical-usb"
    backend = TSCircuitBackend(Path(__file__).parents[1])
    backend.generate_source(project, spec, {"components": [component]})
    compiler_source = (project / "electronics/source/tscircuit/board.compiler.mjs").read_text(encoding="utf-8")
    manifest = json.loads((project / "electronics/source/tscircuit/source_manifest.json").read_text(encoding="utf-8"))

    assert '"pin1": ["PAD_A1_A1", "A1"]' in compiler_source
    assert '"pinA1"' not in compiler_source
    assert '"pin1": sel.net.GND' in compiler_source
    assert 'React.createElement("smtpad"' in compiler_source
    assert manifest["pin_number_aliases"]["J1"]["backend_to_graph"]["17"] == "SH"
    assert manifest["canonical_footprints"][0]["library_id"] == footprint


def test_tscircuit_canonical_rp2040_footprint_preserves_pad_57_via_array():
    footprint = "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm"
    component = {
        "ref": "U2",
        "footprint": footprint,
        "pins": [
            {
                "number": str(number),
                "name": "GND" if number == 57 else f"PIN_{number}",
                "net": "GND" if number == 57 else None,
            }
            for number in range(1, 58)
        ],
    }
    graph_to_backend, _backend_to_graph = TSCircuitBackend._pin_number_maps(
        component,
        footprint,
    )

    canonical = TSCircuitBackend._canonical_footprint_elements(
        footprint,
        graph_to_backend,
    )

    assert canonical is not None
    elements, _footprint_hash = canonical
    pad_57_hints = ["pin57", "57"]
    assert sum(
        name == "platedhole" and props.get("portHints") == pad_57_hints
        for name, props in elements
    ) == 9
    assert sum(
        name == "smtpad" and props.get("portHints") == pad_57_hints
        for name, props in elements
    ) == 1
    assert {
        (props["pcbX"], props["pcbY"])
        for name, props in elements
        if name == "platedhole" and props.get("portHints") == pad_57_hints
    } == {
        (x_mm, y_mm)
        for x_mm in (-1.275, 0.0, 1.275)
        for y_mm in (-1.275, 0.0, 1.275)
    }


def test_tscircuit_netlist_extract_restores_graph_pad_identifiers():
    compiled = [
        {"type": "source_component", "source_component_id": "source_component_0", "name": "J1"},
        {
            "type": "source_port",
            "source_port_id": "source_port_0",
            "source_component_id": "source_component_0",
            "pin_number": 1,
        },
        {"type": "source_net", "source_net_id": "source_net_0", "name": "GND"},
        {
            "type": "source_trace",
            "connected_source_net_ids": ["source_net_0"],
            "connected_source_port_ids": ["source_port_0"],
        },
    ]

    netlist = TSCircuitBackend.extract_netlist(compiled, {"J1": {"1": "A1"}})

    assert netlist == {"GND": ["J1.A1"]}


def test_tscircuit_pcb_validation_errors_do_not_block_compiled_parity():
    circuit_json = [
        {"type": "pcb_pad_pad_clearance_error", "message": "pads overlap"},
        {"type": "pcb_component_outside_board_error", "message": "outside board"},
        {"type": "source_failed_to_create_component_error", "message": "invalid pin labels"},
    ]

    compile_errors, pcb_errors = TSCircuitBackend._partition_circuit_errors(circuit_json)

    assert [item["type"] for item in compile_errors] == ["source_failed_to_create_component_error"]
    assert [item["type"] for item in pcb_errors] == [
        "pcb_pad_pad_clearance_error",
        "pcb_component_outside_board_error",
    ]


def test_tscircuit_compiled_placement_must_match_solver_coordinates():
    graph = {
        "placement": {"board_width_mm": 100.0, "board_height_mm": 60.0},
        "components": [{
            "ref": "U1",
            "pcb_position_mm": [20.0, 10.0],
            "placement_source": "solver_agent_adjacent_to",
        }],
    }
    compiled = [
        {"type": "source_component", "source_component_id": "source_component_0", "name": "U1"},
        {
            "type": "pcb_component",
            "source_component_id": "source_component_0",
            "center": {"x": -30.0, "y": -20.0},
        },
    ]

    failures, checked = TSCircuitBackend.placement_parity_failures(compiled, graph)
    drifted = deepcopy(compiled)
    drifted[1]["center"] = {"x": -20.0, "y": -20.0}
    drift_failures, drift_checked = TSCircuitBackend.placement_parity_failures(drifted, graph)

    assert checked == 1
    assert failures == []
    assert drift_checked == 1
    assert [failure.code for failure in drift_failures] == ["placement_coordinate_mismatch"]
    assert drift_failures[0].details["error_mm"] == 10.0


def test_tscircuit_placement_uses_footprint_origin_for_asymmetric_geometry():
    graph = {
        "placement": {"board_width_mm": 65.0, "board_height_mm": 30.0},
        "components": [{
            "ref": "J1",
            "pcb_position_mm": [5.321, 15.0],
            "pcb_rotation_deg": 0.0,
        }],
    }
    compiled = [
        {"type": "source_component", "source_component_id": "source_component_0", "name": "J1"},
        {
            "type": "pcb_component",
            "source_component_id": "source_component_0",
            "center": {"x": -27.179, "y": 1.14},
            "display_offset_x": -27.179,
            "display_offset_y": 0.0,
            "rotation": 0.0,
        },
    ]

    failures, checked = TSCircuitBackend.placement_parity_failures(compiled, graph)

    assert checked == 1
    assert failures == []


def test_tscircuit_compiled_rotation_must_match_solver_rotation():
    graph = {
        "placement": {"board_width_mm": 100.0, "board_height_mm": 60.0},
        "components": [{
            "ref": "U1",
            "pcb_position_mm": [20.0, 10.0],
            "pcb_rotation_deg": 180.0,
            "placement_source": "solver_edge_antenna",
        }],
    }
    compiled = [
        {"type": "source_component", "source_component_id": "source_component_0", "name": "U1"},
        {
            "type": "pcb_component",
            "source_component_id": "source_component_0",
            "center": {"x": -30.0, "y": -20.0},
            "rotation": "180deg",
        },
    ]

    failures, checked = TSCircuitBackend.placement_parity_failures(compiled, graph)
    drifted = deepcopy(compiled)
    drifted[1]["rotation"] = 0.0
    drift_failures, drift_checked = TSCircuitBackend.placement_parity_failures(drifted, graph)

    assert checked == 1
    assert failures == []
    assert drift_checked == 1
    assert [failure.code for failure in drift_failures] == ["placement_rotation_mismatch"]
    assert drift_failures[0].details["rotation_error_deg"] == 180.0


def test_tscircuit_compiled_rotation_may_be_omitted_only_for_zero_rotation():
    compiled = [
        {"type": "source_component", "source_component_id": "source_component_0", "name": "U1"},
        {
            "type": "pcb_component",
            "source_component_id": "source_component_0",
            "center": {"x": -30.0, "y": -20.0},
        },
    ]
    graph = {
        "placement": {"board_width_mm": 100.0, "board_height_mm": 60.0},
        "components": [{"ref": "U1", "pcb_position_mm": [20.0, 10.0], "pcb_rotation_deg": 0.0}],
    }

    zero_failures, zero_checked = TSCircuitBackend.placement_parity_failures(compiled, graph)
    graph["components"][0]["pcb_rotation_deg"] = 180.0
    rotated_failures, rotated_checked = TSCircuitBackend.placement_parity_failures(compiled, graph)

    assert zero_checked == 1
    assert zero_failures == []
    assert rotated_checked == 1
    assert [failure.code for failure in rotated_failures] == ["compiled_component_rotation_missing"]


def test_tscircuit_backend_is_not_executed_when_external_checks_disabled(service, project, monkeypatch):
    _set_backend(service, project, "tscircuit")
    service.generate_electronics_only(project)

    def fail_if_called(*_args, **_kwargs):
        pytest.fail("tscircuit backend subprocess should not run when include_external=False")

    monkeypatch.setattr(service.tscircuit, "evaluate", fail_if_called)

    checks = service.run_all_checks(project, include_external=False)
    reports = {item["gate"]: item for item in checks["reports"]}

    assert reports["tscircuit_compile"]["status"] == "blocked"
    assert reports["tscircuit_compile"]["failures"][0]["code"] == "external_gate_not_run"
    assert reports["tscircuit_footprint_parity"]["status"] == "blocked"
    assert reports["tscircuit_layout_completeness"]["status"] == "blocked"


def test_kicad_backend_is_not_executed_when_external_checks_disabled(service, project, monkeypatch):
    _set_backend(service, project, "kicad")
    service.generate_electronics_only(project)

    def fail_if_called(*_args, **_kwargs):
        pytest.fail("KiCad backend subprocess should not run when include_external=False")

    monkeypatch.setattr(service.kicad, "evaluate", fail_if_called)

    checks = service.run_all_checks(project, include_external=False)
    reports = {item["gate"]: item for item in checks["reports"]}

    assert reports["kicad_compile"]["status"] == "blocked"
    assert reports["kicad_compile"]["failures"][0]["code"] == "external_gate_not_run"
    assert reports["kicad_footprint_parity"]["status"] == "blocked"
    assert reports["kicad_manufacturing_export"]["status"] == "blocked"


def test_tool_version_timeout_degrades_to_unknown(monkeypatch):
    monkeypatch.setattr(backend_command, "resolve_tool", lambda _: "/bin/hung-tool")

    def fake_run(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(backend_command.subprocess, "run", fake_run)

    assert backend_command.tool_version("kicad-cli") is None


def test_atopile_emits_real_ato_source_and_compile_gate_runs(service, project):
    _set_backend(service, project, "atopile")
    service.generate_electronics_only(project)
    source = service.workspace.require_project(project) / "electronics" / "source" / "atopile"
    # Real .ato source is generated (not a placeholder comment file)
    ato_files = list(source.glob("*.ato"))
    assert ato_files, "atopile adapter must generate .ato source"
    assert (source / "ato.yaml").is_file(), "atopile adapter must generate ato.yaml project file"
    ato_content = (source / "design.ato").read_text(encoding="utf-8")
    assert "module" in ato_content, ".ato file must contain a module declaration"
    # Signals declared in the .ato file cover all graph nets (no truncation)
    assert ato_content.count("\n    signal ") >= 1, ".ato must declare at least one signal"
    checks = service.run_all_checks(project, include_external=False)
    reports = {item["gate"]: item for item in checks["reports"]}
    compile_status = reports["atopile_compile"]["status"]
    assert compile_status in ("pass", "fail", "blocked"), f"compile gate should be active, got {compile_status}"
    if compile_status == "pass":
        # Source-AST parity: netlist_extract and graph_parity implemented via .ato parsing
        assert reports["atopile_netlist_extract"]["status"] == "pass"
        assert reports["atopile_graph_parity"]["status"] == "pass"
        # Footprint assignment deferred to KiCad plugin; layout/manufacturing require plugin
        assert reports["atopile_footprint_parity"]["status"] == "blocked"
        assert reports["atopile_footprint_parity"]["failures"][0]["code"] == "footprint_assignment_deferred"
        for stage in ("layout_completeness", "manufacturing_export"):
            assert reports[f"atopile_{stage}"]["status"] == "blocked"
            assert reports[f"atopile_{stage}"]["failures"][0]["code"] == "kicad_plugin_required"
    else:
        # When compile is blocked/failed, remaining gates are also blocked
        for stage in ("netlist_extract", "graph_parity", "footprint_parity", "layout_completeness", "manufacturing_export"):
            assert reports[f"atopile_{stage}"]["status"] == "blocked"


def test_atopile_missing_cli_only_blocks_compile_as_tool_unavailable(service, project, monkeypatch):
    _set_backend(service, project, "atopile")
    service.generate_electronics_only(project)
    monkeypatch.setattr("hw_codesign.backends.atopile.shutil.which", lambda _: None)
    graph_path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
    reports = {
        report.gate: report
        for report in service.atopile.evaluate(
            service.workspace.require_project(project),
            json.loads(graph_path.read_text(encoding="utf-8")),
        )
    }

    assert reports["atopile_compile"].status == "blocked"
    assert reports["atopile_compile"].failures[0].code == "tool_unavailable"
    # When compile is blocked (tool missing), remaining gates are filled with gate_not_run
    for stage in ("netlist_extract", "graph_parity", "footprint_parity", "layout_completeness", "manufacturing_export"):
        report = reports[f"atopile_{stage}"]
        assert report.status == "blocked"
        assert report.failures[0].code == "gate_not_run"


def test_non_release_backend_cannot_prepare_release(service, project):
    # reference backend is candidate-only by design and must block prepare_release
    from hw_codesign.io import read_yaml, write_yaml
    project_path = service.workspace.require_project(project)
    system_path = project_path / "spec" / "system.yaml"
    system = read_yaml(system_path)
    system["electronics"]["backend"] = "reference"
    write_yaml(system_path, system)
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    result = service.prepare_release(project, checks, native_checks_confirmed=True)
    assert result["status"] == "blocked"
    assert not (project_path / "exports" / "releases").exists()


def test_atopile_backend_is_release_eligible(service, project):
    _set_backend(service, project, "atopile")
    service.generate_electronics_only(project)
    source = service.workspace.require_project(project) / "electronics" / "source" / "atopile"
    manifest = json.loads((source / "source_manifest.json").read_text(encoding="utf-8"))
    assert manifest["backend_release_capable"] is True
    assert manifest["release_tier"] == "hdl_source"
    assert manifest["provenance"]["release_tier"] == "hdl_source"
    assert manifest["source_release_eligible"] is True
    assert manifest["hdl_source_release_eligible"] is True
    assert manifest["netlist_release_eligible"] is False
    assert manifest["fabrication_release_eligible"] is False
    blocking = set(manifest["release_blocking_gates"])
    # footprint/layout/manufacturing are not release-blocking (environmental constraints)
    assert "atopile_footprint_parity" not in blocking
    assert "atopile_layout_completeness" not in blocking
    assert "atopile_manufacturing_export" not in blocking
    # compile/netlist/graph parity are required
    assert "atopile_compile" in blocking
    assert "atopile_netlist_extract" in blocking
    assert "atopile_graph_parity" in blocking
    checks = service.run_all_checks(project, include_external=False)
    gate = service.check_release_gate(project, [service._report_from_dict(item) for item in checks["reports"]])
    codes = {failure["code"] for failure in gate["failures"]}
    assert "compiled_electronics_backend_required" not in codes


def test_python_netlist_backend_is_release_eligible(service, project):
    _set_backend(service, project, "python_netlist")
    service.generate_all(project)
    source = service.workspace.require_project(project) / "electronics" / "source" / "python_netlist"
    manifest = json.loads((source / "source_manifest.json").read_text(encoding="utf-8"))
    assert manifest["backend_release_capable"] is True
    assert manifest["release_tier"] == "netlist"
    assert manifest["provenance"]["release_tier"] == "netlist"
    assert manifest["source_release_eligible"] is False
    assert manifest["netlist_release_eligible"] is True
    assert manifest["hdl_source_release_eligible"] is False
    assert manifest["fabrication_release_eligible"] is False
    # layout/manufacturing gates are not release-blocking because this is a netlist tier.
    blocking = set(manifest["release_blocking_gates"])
    assert "python_netlist_layout_completeness" not in blocking
    assert "python_netlist_manufacturing_export" not in blocking


def test_python_netlist_release_gate_requires_netlist_not_fabrication(service, project):
    _set_backend(service, project, "python_netlist")
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    gate = service.check_release_gate(project, [service._report_from_dict(item) for item in checks["reports"]])
    missing_paths = {failure["path"] for failure in gate["failures"] if failure["code"] == "missing_export"}

    assert any(path.endswith("netlist/compiled_netlist.json") for path in missing_paths)
    assert not any(path.endswith("fabrication/gerbers.zip") for path in missing_paths)
    assert not any(path.endswith("fabrication/pick_and_place.csv") for path in missing_paths)


def test_python_netlist_manufacturing_export_never_creates_fabrication_artifacts(service, project):
    _set_backend(service, project, "python_netlist")
    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    release = project_path / "exports" / "tmp-python-netlist-export"

    report = service.python_netlist.export_manufacturing(project_path, release)

    assert report.gate == "python_netlist_manufacturing_export"
    assert report.status == Status.BLOCKED
    assert report.metrics["release_tier"] == "netlist"
    assert report.backend["fabrication_release_eligible"] is False
    assert not report.artifacts
    assert not (release / "fabrication").exists()


def test_prepare_release_filters_python_netlist_nonfabrication_gates(service, project):
    _set_backend(service, project, "python_netlist")
    reports = [
        GateReport("python_netlist_compile", Status.PASS),
        GateReport("python_netlist_netlist_extract", Status.PASS),
        GateReport("python_netlist_graph_parity", Status.PASS),
        GateReport("python_netlist_footprint_parity", Status.PASS),
        GateReport("python_netlist_layout_completeness", Status.BLOCKED),
        GateReport("python_netlist_manufacturing_export", Status.BLOCKED),
        GateReport("physical_qualification", Status.BLOCKED),
    ]

    result = service.prepare_release(
        project,
        {"reports": [report.to_dict() for report in reports]},
        native_checks_confirmed=True,
    )

    returned_gates = {report["gate"] for report in result["reports"]}
    assert result["status"] == "blocked"
    assert result["code"] == "release_gates_not_passed"
    assert "physical_qualification" in returned_gates
    assert "python_netlist_layout_completeness" not in returned_gates
    assert "python_netlist_manufacturing_export" not in returned_gates


def test_prepare_release_filters_atopile_fabrication_plugin_gates(service, project):
    _set_backend(service, project, "atopile")
    reports = [
        GateReport("atopile_compile", Status.PASS),
        GateReport("atopile_netlist_extract", Status.PASS),
        GateReport("atopile_graph_parity", Status.PASS),
        GateReport("atopile_footprint_parity", Status.BLOCKED),
        GateReport("atopile_layout_completeness", Status.BLOCKED),
        GateReport("atopile_manufacturing_export", Status.BLOCKED),
        GateReport("physical_qualification", Status.BLOCKED),
    ]

    result = service.prepare_release(
        project,
        {"reports": [report.to_dict() for report in reports]},
        native_checks_confirmed=True,
    )

    returned_gates = {report["gate"] for report in result["reports"]}
    assert result["status"] == "blocked"
    assert result["code"] == "release_gates_not_passed"
    assert "physical_qualification" in returned_gates
    assert "atopile_footprint_parity" not in returned_gates
    assert "atopile_layout_completeness" not in returned_gates
    assert "atopile_manufacturing_export" not in returned_gates


def test_atopile_release_gate_requires_source_not_fabrication(service, project):
    _set_backend(service, project, "atopile")
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    gate = service.check_release_gate(project, [service._report_from_dict(item) for item in checks["reports"]])
    missing_paths = {failure["path"] for failure in gate["failures"] if failure["code"] == "missing_export"}

    assert any(path.endswith("source/atopile/design.ato") for path in missing_paths)
    assert not any(path.endswith("fabrication/atopile_source/design.ato") for path in missing_paths)


def test_kicad_netlist_parser_extracts_graph_and_footprints(tmp_path):
    netlist = tmp_path / "design.net"
    netlist.write_text("""<?xml version="1.0"?><export><components><comp ref="R1"><footprint>Resistor_SMD:R_0603</footprint></comp></components><nets><net code="1" name="SIG"><node ref="R1" pin="1"/></net></nets></export>""", encoding="utf-8")
    nets, footprints = service_kicad_parser(netlist)
    assert nets == {"SIG": ["R1.1"]}
    assert footprints == {"R1": "Resistor_SMD:R_0603"}


def service_kicad_parser(path):
    from hw_codesign.backends.kicad import KiCadBackend
    return KiCadBackend._extract_kicad_netlist(path)


def test_kicad_manufacturing_gate_requires_and_exports_all_artifacts(service, project, monkeypatch):
    service.generate_all(project)
    project_path = service.workspace.require_project(project)

    def fake_run_tool(executable, arguments, cwd):
        output = arguments[arguments.index("--output") + 1]
        output_path = project_path.__class__(output)
        if "gerbers" in arguments:
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board-F_Cu.gbr").write_text("gerber", encoding="utf-8")
            (output_path / "board-F_Paste.gtp").write_text("front paste", encoding="utf-8")
        elif "drill" in arguments:
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board.drl").write_text("drill", encoding="utf-8")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                "Ref,Val,Package,PosX,PosY,Rot,Side\nR1,10k,R_0603,1,2,0,top\n"
                if "pos" in arguments
                else "step",
                encoding="utf-8",
            )
        return ToolResult([executable, *arguments], 0, "", "", True)

    monkeypatch.setattr("hw_codesign.backends.kicad.run_tool", fake_run_tool)
    release = project_path / "exports" / "candidates" / "manufacturing-test"
    report = service.kicad.export_manufacturing(project_path, release)
    assert report.status == "pass"
    assert {Path(path).name for path in report.artifacts} >= {"gerbers.zip", "drill.zip", "pick_and_place.csv", "bom.csv", "board.step", "fabrication_manifest.json"}
    assert (release / "fabrication" / "pick_and_place.csv").stat().st_size > 0
    assert (release / "fabrication" / "bom.csv").stat().st_size > 0
    manifest = json.loads((release / "fabrication" / "fabrication_manifest.json").read_text(encoding="utf-8"))
    board = service.kicad._design_file(project_path, "*.kicad_pcb")
    assert board is not None
    assert manifest["candidate_id"].startswith("sha256:")
    assert next(item for item in manifest["inputs"] if item["role"] == "canonical_kicad_board")["sha256"] == sha256(board)
    readiness = json.loads((release / "fabrication" / "readiness_manifest.json").read_text(encoding="utf-8"))
    assert readiness["order_ready"] is False
    assert readiness["board"]["sha256"] == sha256(board)
    assert readiness["routing_binding"]["status"] in {"verified", "unverified", "not_available"}
    assert service.kicad.verify_manufacturing_export(project_path, release).status == "pass"

    (release / "fabrication" / "pick_and_place.csv").write_text("tampered\n", encoding="utf-8")
    integrity = service.kicad.verify_manufacturing_export(project_path, release)
    assert integrity.status == "fail"
    assert {failure.code for failure in integrity.failures} == {"fabrication_checksum_mismatch"}


def test_kicad_manufacturing_export_uses_board_declared_stackup(service, monkeypatch):
    project = "sensor_logger_kicad_export_layers"
    service.create_project(project, template="sensor_data_logger")
    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    captured_layers: list[str] = []

    def fake_run_tool(executable, arguments, cwd):
        output = arguments[arguments.index("--output") + 1]
        output_path = project_path.__class__(output)
        if "gerbers" in arguments:
            captured_layers.append(arguments[arguments.index("--layers") + 1])
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board-F_Cu.gbr").write_text("gerber", encoding="utf-8")
            (output_path / "board-F_Paste.gtp").write_text("front paste", encoding="utf-8")
            (output_path / "board-B_Paste.gbp").write_text("back paste", encoding="utf-8")
        elif "drill" in arguments:
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board.drl").write_text("drill", encoding="utf-8")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                "Ref,Val,Package,PosX,PosY,Rot,Side\nU1,IC,QFN,1,2,0,top\nU2,IC,QFN,3,4,0,bottom\n"
                if "pos" in arguments
                else "step",
                encoding="utf-8",
            )
        return ToolResult([executable, *arguments], 0, "", "", True)

    monkeypatch.setattr("hw_codesign.backends.kicad.run_tool", fake_run_tool)
    release = project_path / "exports" / "candidates" / "manufacturing-layer-test"
    report = service.kicad.export_manufacturing(project_path, release)

    assert report.status == "pass"
    assert captured_layers == ["F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts"]
    assert "In1.Cu" not in report.metrics["export_layers"]
    assert "In2.Cu" not in report.metrics["export_layers"]
    with zipfile.ZipFile(release / "fabrication" / "gerbers.zip") as archive:
        assert {"board-F_Paste.gtp", "board-B_Paste.gbp"} <= set(archive.namelist())


def test_kicad_manufacturing_export_rejects_missing_paste_for_populated_side(service, project, monkeypatch):
    service.generate_all(project)
    project_path = service.workspace.require_project(project)

    def fake_run_tool(executable, arguments, cwd):
        output_path = Path(arguments[arguments.index("--output") + 1])
        if "gerbers" in arguments:
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board-F_Cu.gtl").write_text("gerber", encoding="utf-8")
        elif "drill" in arguments:
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "board.drl").write_text("drill", encoding="utf-8")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                "Ref,Val,Package,PosX,PosY,Rot,Side\nR1,10k,R_0603,1,2,0,top\n"
                if "pos" in arguments
                else "step",
                encoding="utf-8",
            )
        return ToolResult([executable, *arguments], 0, "", "", True)

    monkeypatch.setattr("hw_codesign.backends.kicad.run_tool", fake_run_tool)
    report = service.kicad.export_manufacturing(
        project_path,
        project_path / "exports" / "candidates" / "missing-paste-test",
    )

    assert report.status == "fail"
    assert {failure.code for failure in report.failures} == {"assembly_paste_layer_missing"}
    assert report.failures[0].details == {"missing_layers": ["F.Paste"]}


def test_kicad_manufacturing_export_normalizes_volatile_metadata(service, project, monkeypatch):
    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    cycle = {"value": 0}

    def fake_run_tool(executable, arguments, cwd):
        output = Path(arguments[arguments.index("--output") + 1])
        if "gerbers" in arguments:
            cycle["value"] += 1
        stamp = f"2026-07-{cycle['value'] + 10:02d}T12:34:56+09:00"
        if "gerbers" in arguments:
            output.mkdir(parents=True, exist_ok=True)
            (output / "board-F_Cu.gbr").write_text(
                f"%TF.CreationDate,{stamp}*%\nG04 Created by KiCad (PCBNEW 10.0.3) date {stamp[:-6].replace('T', ' ')}*\nM02*\n",
                encoding="utf-8",
            )
            (output / "board-F_Paste.gtp").write_text("front paste\n", encoding="utf-8")
            (output / "board-job.gbrjob").write_text(json.dumps({"Header": {"CreationDate": stamp}}), encoding="utf-8")
        elif "drill" in arguments:
            output.mkdir(parents=True, exist_ok=True)
            (output / "board.drl").write_text(
                f"M48\n; DRILL file KiCad 10.0.3 date {stamp[:-6]}\n; #@! TF.CreationDate,{stamp}\nM30\n",
                encoding="utf-8",
            )
            (output / "board-drl_map.pdf").write_bytes(f"volatile pdf {stamp}".encode())
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                "Ref,Val,Package,PosX,PosY,Rot,Side\nR1,10k,R_0603,1,2,0,top\n"
                if "pos" in arguments
                else f"ISO-10303-21;\nFILE_NAME('board.step','{stamp[:-6]}',('Pcbnew'),('KiCad'),'','','');\nEND-ISO-10303-21;\n",
                encoding="utf-8",
            )
        return ToolResult([executable, *arguments], 0, "", "", True)

    monkeypatch.setattr("hw_codesign.backends.kicad.run_tool", fake_run_tool)
    monkeypatch.setattr("hw_codesign.backends.kicad.tool_version", lambda _: "10.0.3")
    first = project_path / "exports" / "candidates" / "deterministic-first"
    second = project_path / "exports" / "candidates" / "deterministic-second"

    first_report = service.kicad.export_manufacturing(project_path, first)
    second_report = service.kicad.export_manufacturing(project_path, second)

    assert first_report.status == "pass"
    assert second_report.status == "pass"
    first_manifest = json.loads((first / "fabrication" / "fabrication_manifest.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second / "fabrication" / "fabrication_manifest.json").read_text(encoding="utf-8"))
    assert first_manifest["candidate_id"] == second_manifest["candidate_id"]
    for name in ("gerbers.zip", "drill.zip", "pick_and_place.csv", "bom.csv"):
        assert sha256(first / "fabrication" / name) == sha256(second / "fabrication" / name)
    assert sha256(first / "mechanical" / "board.step") == sha256(second / "mechanical" / "board.step")
    with zipfile.ZipFile(first / "fabrication" / "drill.zip") as archive:
        assert archive.namelist() == ["board.drl"]
        assert b"1970-01-01T00:00:00+00:00" in archive.read("board.drl")
    with zipfile.ZipFile(first / "fabrication" / "gerbers.zip") as archive:
        assert b"1970-01-01T00:00:00+00:00" in archive.read("board-F_Cu.gbr")
        assert json.loads(archive.read("board-job.gbrjob"))["Header"]["CreationDate"] == "1970-01-01T00:00:00+00:00"

    tampered_archive = second / "fabrication" / "gerbers.zip"
    with zipfile.ZipFile(tampered_archive) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    members["board-F_Cu.gbr"] += b"G04 tampered geometry*\n"
    with zipfile.ZipFile(tampered_archive, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, payload in sorted(members.items()):
            archive.writestr(name, payload)
    manifest_path = second / "fabrication" / "fabrication_manifest.json"
    tampered_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    outer_record = next(item for item in tampered_manifest["artifacts"] if item["path"] == "fabrication/gerbers.zip")
    outer_record["bytes"] = tampered_archive.stat().st_size
    outer_record["sha256"] = sha256(tampered_archive)
    canonical = {key: value for key, value in tampered_manifest.items() if key != "candidate_id"}
    tampered_manifest["candidate_id"] = "sha256:" + hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()
    manifest_path.write_text(json.dumps(tampered_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    deep_integrity = service.kicad.verify_manufacturing_export(project_path, second)
    assert deep_integrity.status == "fail"
    assert "fabrication_archive_member_checksum_mismatch" in {failure.code for failure in deep_integrity.failures}


def test_rp2040_readiness_manifest_reports_board_via_geometry_without_order_claim(service):
    from hw_codesign.backends.kicad import _write_fabrication_readiness_manifest

    project = "rp2040_fabrication_readiness"
    service.create_project(project, template="rp2040_usb_device")
    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    board = project_path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb"
    fabrication = project_path / "exports" / "candidates" / "readiness-test" / "fabrication"

    manifest_path = _write_fabrication_readiness_manifest(
        project_path,
        board,
        fabrication,
        {"status": "verified", "receipt_status": "pass", "board_sha256": sha256(board), "board_sha256_match": True},
    )
    readiness = json.loads(manifest_path.read_text(encoding="utf-8"))
    geometry = readiness["via_in_pad"]["observed_geometry"][0]

    assert readiness["order_ready"] is False
    assert readiness["status"] == "blocked"
    assert readiness["board"]["sha256"] == sha256(board)
    assert readiness["via_in_pad"]["declared_count"] == 9
    assert readiness["via_in_pad"]["observed_count"] == 9
    assert readiness["via_in_pad"]["count_matches_board"] is True
    assert geometry["outer_diameter_mm"] == [0.6]
    assert geometry["drill_diameter_mm"] == [0.35]
    assert geometry["grid_pitch_x_mm"] == 1.275
    assert geometry["grid_pitch_y_mm"] == 1.275
    assert {item["code"] for item in readiness["blockers"]} >= {
        "via_in_pad_process_unqualified",
        "fabricator_stackup_confirmation_required",
    }


def test_tscircuit_manufacturing_bridge_replaces_placeholder_gate(service, project, monkeypatch):
    _set_backend(service, project, "tscircuit")
    service.generate_all(project)
    monkeypatch.setattr(service.tscircuit, "evaluate", lambda path, graph: [
        GateReport(f"tscircuit_{stage}", Status.PASS if stage != "manufacturing_export" else Status.BLOCKED)
        for stage in CONTRACT_STAGES
    ])
    monkeypatch.setattr(service.kicad, "export_manufacturing", lambda path, release: GateReport("fabrication_export", Status.PASS, artifacts=[str(release / "fabrication" / "gerbers.zip")]))
    checks = service.run_all_checks(project, include_external=True)
    reports = [item for item in checks["reports"] if item["gate"] == "tscircuit_manufacturing_export"]
    assert len(reports) == 1
    assert reports[0]["status"] == "pass"
    assert reports[0]["backend"]["export_bridge"] == "compiled_graph_to_kicad"


def test_release_gate_requires_every_backend_contract_stage(service, project):
    _set_backend(service, project, "kicad")
    reports = [GateReport(f"kicad_{stage}", Status.PASS) for stage in CONTRACT_STAGES if stage != "manufacturing_export"]
    gate = service.check_release_gate(project, reports=reports, include_external=False)
    assert gate["status"] == "blocked"
    manufacturing_failure = next(failure for failure in gate["failures"] if failure["details"].get("details", {}).get("failure_codes") == ["gate_not_run"])
    assert manufacturing_failure["message"].endswith("kicad_manufacturing_export")
