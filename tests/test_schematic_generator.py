from __future__ import annotations

import json
import re

import pytest

from hw_codesign import reference_backend
from hw_codesign.schematic_generator import generate_kicad_schematic


def _component(pins: list[dict[str, object]]) -> dict[str, object]:
    return {
        "ref": "J1",
        "value": "TEST_CONNECTOR",
        "footprint": "Connector_Generic:Conn_01x02",
        "mpn": "TEST",
        "manufacturer": "test",
        "supplier_sku": "TEST",
        "pins": pins,
    }


def test_kicad_schematic_marks_declared_unconnected_pin(tmp_path):
    graph = {
        "components": [_component([
            {"number": "1", "name": "SIGNAL", "net": "SIGNAL", "role": "signal"},
            {"number": "2", "name": "NC", "net": None, "role": "no_connect"},
        ])],
        "nets": [{"name": "SIGNAL"}],
    }
    output = tmp_path / "declared_no_connect.kicad_sch"

    generate_kicad_schematic("declared_no_connect", graph, output)

    text = output.read_text(encoding="utf-8")
    assert text.count("(no_connect") == 1
    assert '"SIGNAL"' in text
    assert not re.search(r'\(label\s+""', text)


def test_kicad_schematic_rejects_undeclared_unconnected_pin(tmp_path):
    graph = {
        "components": [_component([
            {"number": "1", "name": "SIGNAL", "net": "SIGNAL", "role": "signal"},
            {"number": "2", "name": "MISSING", "net": None, "role": "signal"},
        ])],
        "nets": [{"name": "SIGNAL"}],
    }

    with pytest.raises(
        ValueError,
        match=r"Unconnected schematic pin J1\.2 must declare role=no_connect",
    ):
        generate_kicad_schematic(
            "undeclared_no_connect",
            graph,
            tmp_path / "undeclared_no_connect.kicad_sch",
        )


def test_kicad_schematic_generation_report_tracks_current_attempt(tmp_path, monkeypatch):
    project = tmp_path / "report_lifecycle"
    spec = {
        "manufacturing": {
            "pcb": {
                "layers": 2,
                "min_clearance_mm": 0.15,
                "min_track_width_mm": 0.15,
            },
        },
    }
    graph = {
        "components": [_component([
            {"number": "1", "name": "SIGNAL", "net": "SIGNAL", "role": "signal"},
            {"number": "2", "name": "NC", "net": None, "role": "no_connect"},
        ])],
        "nets": [{"name": "SIGNAL"}],
    }
    monkeypatch.setattr(reference_backend, "_kicad_board", lambda _spec, _graph: ("(kicad_pcb)\n", []))
    report = project / "electronics" / "generated" / "kicad" / "schematic_generation.json"
    schematic = report.with_name("report_lifecycle.kicad_sch")

    def fail_first(_name, _graph, _output):
        raise ValueError("first attempt failed")

    monkeypatch.setattr(reference_backend, "generate_kicad_schematic", fail_first)
    reference_backend.generate_kicad(project, spec, graph)
    assert json.loads(report.read_text(encoding="utf-8"))["message"] == "first attempt failed"

    def succeed(_name, _graph, output):
        output.write_text("(kicad_sch current-success)\n", encoding="utf-8")

    monkeypatch.setattr(reference_backend, "generate_kicad_schematic", succeed)
    files = reference_backend.generate_kicad(project, spec, graph)
    assert not report.exists()
    assert str(report) not in files
    assert schematic.read_text(encoding="utf-8") == "(kicad_sch current-success)\n"

    def fail_current(_name, _graph, _output):
        raise ValueError("current attempt failed")

    monkeypatch.setattr(reference_backend, "generate_kicad_schematic", fail_current)
    reference_backend.generate_kicad(project, spec, graph)
    current = json.loads(report.read_text(encoding="utf-8"))
    assert current["status"] == "blocked"
    assert current["message"] == "current attempt failed"


def test_kicad_generation_preserves_same_prefix_user_files(tmp_path, monkeypatch):
    project = tmp_path / "golden_rp2040_usb_hid"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    protected = {
        "golden_rp2040_usb_hid 2.kicad_pcb": "protected board\n",
        "golden_rp2040_usb_hid 2.kicad_pro": "protected project\n",
        "golden_rp2040_usb_hid 2.ses": "protected session\n",
        "golden_rp2040_usb_hid 2.dsn": "protected dsn\n",
        "golden_rp2040_usb_hid 2.kicad_prl": "protected board prefs\n",
        "golden_rp2040_usb_hid.routed 2.kicad_prl": "protected routed prefs\n",
    }
    for filename, content in protected.items():
        (target / filename).write_text(content, encoding="utf-8")

    spec = {
        "manufacturing": {
            "pcb": {
                "layers": 2,
                "min_clearance_mm": 0.15,
                "min_track_width_mm": 0.15,
            },
        },
    }
    graph = {
        "components": [_component([
            {"number": "1", "name": "SIGNAL", "net": "SIGNAL", "role": "signal"},
            {"number": "2", "name": "NC", "net": None, "role": "no_connect"},
        ])],
        "nets": [{"name": "SIGNAL"}],
    }
    monkeypatch.setattr(reference_backend, "_kicad_board", lambda _spec, _graph: ("(kicad_pcb)\n", []))
    monkeypatch.setattr(
        reference_backend,
        "generate_kicad_schematic",
        lambda _name, _graph, output: output.write_text("(kicad_sch)\n", encoding="utf-8"),
    )

    files = reference_backend.generate_kicad(project, spec, graph)

    assert {
        filename: (target / filename).read_text(encoding="utf-8")
        for filename in protected
    } == protected
    assert all(" 2." not in filename and "routed 2." not in filename for filename in files)
