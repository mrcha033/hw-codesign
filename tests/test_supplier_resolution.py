from __future__ import annotations

import copy
import shutil
from pathlib import Path

import yaml

from hw_codesign.io import read_yaml, write_yaml
from hw_codesign.reference_backend import build_graph
from hw_codesign.resolver import ComponentResolver
from hw_codesign.supplier_adapters import DistributorMetadataAdapter, LcscJlcpcbAdapter


def _parts_copy(tmp_path: Path) -> Path:
    source = Path(__file__).parents[1] / "parts"
    target = tmp_path / "parts"
    shutil.copytree(source, target)
    return target


def _template_spec() -> dict:
    path = Path(__file__).parents[1] / "src" / "hw_codesign" / "templates" / "robotics_controller_full.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _available_records(parts_root: Path, provider: str) -> list[dict]:
    components = yaml.safe_load((parts_root / "components" / "robotics_controller.yaml").read_text(encoding="utf-8"))["components"]
    records = []
    for component in components:
        common = {
            "component_id": component["id"],
            "availability": "available",
            "observed_at": "2026-06-15T00:00:00Z",
        }
        if provider == "lcsc_jlcpcb":
            common.update({"lcsc_part_number": f"TEST-{component['id']}", "jlcpcb_part_class": "unknown", "jlcpcb_stock": 100})
        else:
            common.update({"sku": f"TEST-{component['id']}", "stock": 100})
        records.append(common)
    return records


def test_supplier_adapters_normalize_equivalent_metadata():
    lcsc = LcscJlcpcbAdapter().normalize({
        "component_id": "part",
        "lcsc_part_number": "C123",
        "availability": "available",
        "jlcpcb_stock": 50,
        "observed_at": "2026-06-15T00:00:00Z",
    })
    digikey = DistributorMetadataAdapter("digikey").normalize({
        "component_id": "part",
        "sku": "123-ND",
        "availability": "available",
        "stock": 50,
        "observed_at": "2026-06-15T00:00:00Z",
    })
    assert (lcsc.availability, lcsc.stock) == (digikey.availability, digikey.stock)
    assert lcsc.provider == "lcsc_jlcpcb"
    assert digikey.provider == "digikey"


def test_changing_supplier_source_preserves_gate_semantics(tmp_path):
    template_spec = _template_spec()
    parts_root = _parts_copy(tmp_path)
    graph = build_graph(template_spec)
    statuses = []
    for provider in ("lcsc_jlcpcb", "digikey"):
        catalog = {"provider": provider, "records": _available_records(parts_root, provider)}
        (parts_root / "suppliers" / f"{provider}.yaml").write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
        spec = copy.deepcopy(template_spec)
        spec["sourcing"] = {"provider": provider}
        resolver = ComponentResolver(parts_root)
        resolved, resolution = resolver.resolve(spec, "robotics_controller", graph["components"])
        statuses.append((resolution.status.value, resolver.supplier_availability_report.status.value))
        assert all(item.provenance["supplier_provider"] == provider for item in resolved)
        assert all(item.provenance["supplier_catalog_sha256"] for item in resolved)
    assert statuses == [("pass", "pass"), ("pass", "pass")]


def test_supplier_availability_distinguishes_fail_and_blocked(tmp_path):
    template_spec = _template_spec()
    parts_root = _parts_copy(tmp_path)
    graph = build_graph(template_spec)
    records = _available_records(parts_root, "digikey")
    records[0]["availability"] = "out_of_stock"
    records[1]["availability"] = "unknown"
    (parts_root / "suppliers" / "digikey.yaml").write_text(yaml.safe_dump({"provider": "digikey", "records": records}, sort_keys=False), encoding="utf-8")
    spec = copy.deepcopy(template_spec)
    spec["sourcing"] = {"provider": "digikey"}
    resolver = ComponentResolver(parts_root)
    resolver.resolve(spec, "robotics_controller", graph["components"])
    report = resolver.supplier_availability_report
    assert report.status.value == "fail"
    assert {failure.code for failure in report.failures} >= {"supplier_unavailable", "supplier_availability_unknown"}

    records[1].update({"availability": "available", "sku": "RESTORED", "observed_at": "2026-06-15T00:00:00Z"})
    (parts_root / "suppliers" / "digikey.yaml").write_text(yaml.safe_dump({"provider": "digikey", "records": records}, sort_keys=False), encoding="utf-8")
    resolver = ComponentResolver(parts_root)
    resolver.resolve(spec, "robotics_controller", graph["components"])
    assert resolver.supplier_availability_report.status.value == "fail"

    records[0].update({"availability": "available", "sku": "RESTORED-0", "observed_at": "2026-06-15T00:00:00Z"})
    records[1].update({"availability": "unknown", "sku": "RESTORED-1", "observed_at": None})
    (parts_root / "suppliers" / "digikey.yaml").write_text(yaml.safe_dump({"provider": "digikey", "records": records}, sort_keys=False), encoding="utf-8")
    resolver = ComponentResolver(parts_root)
    resolver.resolve(spec, "robotics_controller", graph["components"])
    assert resolver.supplier_availability_report.status.value == "blocked"


def test_missing_evidence_and_duplicate_component_id_block_resolution(tmp_path):
    template_spec = _template_spec()
    parts_root = _parts_copy(tmp_path)
    graph = build_graph(template_spec)
    evidence_path = parts_root / "evidence" / "datasheets.yaml"
    evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
    evidence["evidence"] = [item for item in evidence["evidence"] if item["component_id"] != "stm32h743vit6"]
    evidence_path.write_text(yaml.safe_dump(evidence, sort_keys=False), encoding="utf-8")
    resolver = ComponentResolver(parts_root)
    resolver.resolve(template_spec, "robotics_controller", graph["components"])
    assert resolver.datasheet_evidence_report.status.value == "fail"
    assert "datasheet_evidence_missing" in {failure.code for failure in resolver.datasheet_evidence_report.failures}

    component_path = parts_root / "components" / "robotics_controller.yaml"
    database = yaml.safe_load(component_path.read_text(encoding="utf-8"))
    database["components"].append(copy.deepcopy(database["components"][0]))
    component_path.write_text(yaml.safe_dump(database, sort_keys=False), encoding="utf-8")
    _, report = ComponentResolver(parts_root).resolve(template_spec, "robotics_controller", graph["components"])
    assert report.status.value == "fail"
    assert "ambiguous_component_id" in {failure.code for failure in report.failures}


def test_generated_graph_contains_supplier_and_datasheet_provenance(service, project):
    assert service.read_spec(project)["sourcing"]["provider"] == "curated"
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    by_gate = {item["gate"]: item for item in checks["reports"]}
    assert by_gate["supplier_availability"]["status"] == "blocked"
    assert by_gate["datasheet_evidence"]["status"] == "pass"
    assert by_gate["sourcing_resilience"]["status"] == "pass"
    graph = yaml.safe_load((service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    assert all(component["resolution_provenance"]["database_file_sha256"] for component in graph["components"])
    assert all(component["datasheet_evidence"] for component in graph["components"])


def test_sourcing_resilience_rejects_unjustified_critical_roles(service, project):
    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    graph = yaml.safe_load((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    role_data = read_yaml(service.parts_root / "role_sets" / "robotics_controller.yaml")
    role_data["alternatives"] = {}
    role_data["single_source_justifications"] = {}

    report = service._sourcing_resilience_report(service.read_spec(project), graph, role_data_override=role_data)

    assert report.status == "fail"
    assert "critical_role_resilience_missing" in {failure.code for failure in report.failures}


def test_project_role_override_selects_curated_alternative(service, project):
    spec_path = service.workspace.require_project(project) / "spec" / "system.yaml"
    system = read_yaml(spec_path)
    system["electronics"].setdefault("role_overrides", {})["resistor_4k7"] = {
        "component_id": "rc0603_10k",
        "resolution": "curated",
        "reason": "Lower pull-up current candidate selected from curated alternatives.",
    }
    write_yaml(spec_path, system)

    result = service.generate_electronics_only(project)
    graph_path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
    graph = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    pullups = [component for component in graph["components"] if component.get("category") == "pullup"]

    assert result["resolution_report"]["status"] == "pass"
    assert pullups
    assert {component["component_id"] for component in pullups} == {"rc0603_10k"}
    assert {item["component_id"] for item in graph["component_resolution"] if item["role"] == "resistor_4k7"} == {"rc0603_10k"}
    provenance = pullups[0]["resolution_provenance"]["role_override"]
    assert provenance["source"] == "project_spec.electronics.role_overrides.resistor_4k7"
    assert provenance["base_component_id"] == "rc0603_4k7"
    assert provenance["required_reviews"] == ["i2c_rise_time"]


def test_project_role_override_rejects_unlisted_component(service, project):
    spec_path = service.workspace.require_project(project) / "spec" / "system.yaml"
    system = read_yaml(spec_path)
    system["electronics"].setdefault("role_overrides", {})["mcu"] = {
        "component_id": "rc0603_10k",
        "resolution": "curated",
        "reason": "Invalid component substitution.",
    }
    write_yaml(spec_path, system)

    result = service.generate_electronics_only(project)
    failures = result["resolution_report"]["failures"]

    assert result["resolution_report"]["status"] == "fail"
    assert "role_override_not_allowed" in {failure["code"] for failure in failures}


def test_esp32s3_library_metadata_is_verified():
    root = Path(__file__).parents[1]
    component_db = yaml.safe_load((root / "parts" / "components" / "sensor_data_logger.yaml").read_text(encoding="utf-8"))
    esp32 = next(component for component in component_db["components"] if component["id"] == "esp32s3_wroom_1")
    expected_pins = {str(number) for number in range(1, 42)}

    assert esp32["review_status"] == "approved"
    assert esp32["resolution_provenance"]["reviewed_at"] != "pending"
    assert esp32["symbol"]["verified"] is True
    assert esp32["footprint"]["verified"] is True
    assert esp32["symbol"]["library_id"] == "RF_Module:ESP32-S3-WROOM-1"
    assert esp32["footprint"]["library_id"] == "RF_Module:ESP32-S3-WROOM-1"
    assert set(esp32["symbol"]["expected_pins"]) == expected_pins
    assert set(esp32["footprint"]["expected_pads"]) == expected_pins

    evidence = yaml.safe_load((root / "parts" / "evidence" / "datasheets.yaml").read_text(encoding="utf-8"))["evidence"]
    esp32_evidence = [item for item in evidence if item["component_id"] == "esp32s3_wroom_1"]
    assert any(
        item["review_status"] == "approved"
        and {"identity", "pins", "symbol", "package", "footprint"}.issubset(set(item["supports"]))
        for item in esp32_evidence
    )

    supplier_records = yaml.safe_load((root / "parts" / "suppliers" / "curated.yaml").read_text(encoding="utf-8"))["records"]
    assert any(record["component_id"] == "esp32s3_wroom_1" for record in supplier_records)


def test_stale_observed_at_blocks_availability(tmp_path):
    template_spec = _template_spec()
    parts_root = _parts_copy(tmp_path)
    graph = build_graph(template_spec)
    records = _available_records(parts_root, "digikey")
    # One record has a fresh timestamp (within 90 days of today).
    # One record has a timestamp well outside the 90-day window.
    records[0]["observed_at"] = "2020-01-01T00:00:00Z"  # definitely stale
    (parts_root / "suppliers" / "digikey.yaml").write_text(
        yaml.safe_dump({"provider": "digikey", "records": records}, sort_keys=False), encoding="utf-8"
    )
    spec = copy.deepcopy(template_spec)
    spec["sourcing"] = {"provider": "digikey"}
    resolver = ComponentResolver(parts_root)
    resolver.resolve(spec, "robotics_controller", graph["components"])
    report = resolver.supplier_availability_report
    assert report.status.value == "blocked"
    stale = [f for f in report.failures if f.code == "supplier_evidence_stale"]
    assert stale
    assert stale[0].details["observed_at"] == "2020-01-01T00:00:00Z"
    assert stale[0].details["max_age_days"] == 90


def test_fresh_observed_at_does_not_trigger_staleness(tmp_path):
    from datetime import UTC, datetime, timedelta
    template_spec = _template_spec()
    parts_root = _parts_copy(tmp_path)
    graph = build_graph(template_spec)
    records = _available_records(parts_root, "digikey")
    fresh_ts = (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for record in records:
        record["observed_at"] = fresh_ts
    (parts_root / "suppliers" / "digikey.yaml").write_text(
        yaml.safe_dump({"provider": "digikey", "records": records}, sort_keys=False), encoding="utf-8"
    )
    spec = copy.deepcopy(template_spec)
    spec["sourcing"] = {"provider": "digikey"}
    resolver = ComponentResolver(parts_root)
    resolver.resolve(spec, "robotics_controller", graph["components"])
    report = resolver.supplier_availability_report
    assert report.status.value == "pass"
    assert not any(f.code == "supplier_evidence_stale" for f in report.failures)


def test_supplier_provider_is_persistent_project_state(service, project):
    service.update_spec(project, "sourcing", {"provider": "digikey"})
    assert service.read_spec(project)["sourcing"] == {"provider": "digikey"}
    service.generate_electronics_only(project)
    checks = service.run_all_checks(project, include_external=False)
    availability = next(item for item in checks["reports"] if item["gate"] == "supplier_availability")
    assert availability["status"] == "blocked"
    assert availability["backend"]["provider"] == "digikey"
    assert "supplier_record_missing" in {failure["code"] for failure in availability["failures"]}
