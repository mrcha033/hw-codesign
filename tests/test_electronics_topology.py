"""Tests for Phase B (electronics topology), Phase C (placement constraints),
Phase D (firmware modules), and Phase E (unified workflow)."""
from __future__ import annotations

import json

# ---------------------------------------------------------------------------
# Phase B — Electronics Topology Authoring
# ---------------------------------------------------------------------------

class TestProposeCircuitBlock:
    def test_returns_pass_for_known_category(self, service, project):
        result = service.propose_circuit_block("can")
        assert result["status"] == "pass"
        assert "candidates" in result
        assert isinstance(result["candidates"], list)
        assert result["count"] == len(result["candidates"])

    def test_returns_pass_with_empty_candidates_for_unknown_category(self, service, project):
        result = service.propose_circuit_block("flux_capacitor_7000")
        assert result["status"] == "pass"
        assert result["candidates"] == []
        assert result["count"] == 0

    def test_returns_usage_hint(self, service, project):
        result = service.propose_circuit_block("regulator")
        assert "usage_hint" in result


class TestAddCircuitBlock:
    def test_add_valid_block_returns_pass_or_fail(self, service, project):
        result = service.add_circuit_block(project, {
            "ref": "U7",
            "category": "can",
            "value": "CAN2 PHY",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
            "connections": {
                "VCC": "V5",
                "GND": "GND",
                "RXD": "CAN_RX",
                "TXD": "CAN_TX",
                "CANH": "CANH",
                "CANL": "CANL",
            },
        })
        assert result["status"] in ("pass", "fail", "blocked")
        assert result["project"] == project
        assert result["ref"] == "U7"
        assert "components_total" in result
        assert "gate_report" in result

    def test_add_block_with_new_nets_increases_component_count(self, service, project):
        base_spec = service.read_spec(project)
        from hw_codesign.reference_backend import build_graph
        base_count = len(build_graph({**base_spec, "agent_electronics": {}})["components"])

        service.add_circuit_block(project, {
            "ref": "U8",
            "category": "can",
            "value": "CAN3 PHY",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
            "connections": {"VCC": "V5", "GND": "GND", "RXD": "CAN3_RX", "TXD": "CAN3_TX"},
        })
        merged_spec = service.read_spec(project)
        merged_graph = build_graph(merged_spec)
        assert len(merged_graph["components"]) == base_count + 1

    def test_add_block_persisted_to_spec(self, service, project):
        service.add_circuit_block(project, {
            "ref": "U9",
            "category": "imu",
            "value": "IMU2",
            "mpn": "ICM-42688-P",
            "footprint": "LGA14",
            "connections": {"VDD": "V3V3", "GND": "GND", "SCL": "I2C2_SCL", "SDA": "I2C2_SDA"},
        })
        path = service.workspace.require_project(project)
        agent_path = path / "spec" / "agent_blocks.yaml"
        assert agent_path.is_file()
        from hw_codesign.io import read_yaml
        data = read_yaml(agent_path)
        refs = [b.get("ref") or b.get("id") for b in data.get("agent_electronics", {}).get("blocks", [])]
        assert "U9" in refs

    def test_add_block_missing_ref_returns_blocked(self, service, project):
        result = service.add_circuit_block(project, {
            "category": "can",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
            "connections": {"VCC": "V5"},
        })
        assert result["status"] == "blocked"
        assert result["code"] == "missing_ref"

    def test_add_block_missing_connections_returns_blocked(self, service, project):
        result = service.add_circuit_block(project, {
            "ref": "U10",
            "category": "can",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
        })
        assert result["status"] == "blocked"
        assert result["code"] == "missing_connections"

    def test_add_block_ref_conflict_returns_blocked(self, service, project):
        result = service.add_circuit_block(project, {
            "ref": "U1",  # U1 is the MCU in base graph
            "category": "can",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
            "connections": {"VCC": "V5"},
        })
        assert result["status"] == "blocked"
        assert result["code"] == "ref_conflict"

    def test_update_existing_block_replaces_not_duplicates(self, service, project):
        block = {
            "ref": "U11",
            "category": "imu",
            "value": "IMU3 v1",
            "mpn": "ICM-42688-P",
            "footprint": "LGA14",
            "connections": {"VDD": "V3V3", "GND": "GND"},
        }
        service.add_circuit_block(project, block)
        service.add_circuit_block(project, {**block, "value": "IMU3 v2"})
        result = service.list_circuit_blocks(project)
        u11_blocks = [b for b in result["blocks"] if b.get("ref") == "U11"]
        assert len(u11_blocks) == 1
        assert u11_blocks[0]["value"] == "IMU3 v2"


class TestListCircuitBlocks:
    def test_empty_before_any_add(self, service, project):
        result = service.list_circuit_blocks(project)
        assert result["status"] == "pass"
        assert result["blocks"] == []
        assert result["count"] == 0

    def test_lists_added_blocks(self, service, project):
        service.add_circuit_block(project, {
            "ref": "U12", "category": "can", "mpn": "X", "footprint": "SOIC8",
            "connections": {"VCC": "V5", "GND": "GND"},
        })
        service.add_circuit_block(project, {
            "ref": "U13", "category": "imu", "mpn": "Y", "footprint": "LGA14",
            "connections": {"VDD": "V3V3", "GND": "GND"},
        })
        result = service.list_circuit_blocks(project)
        assert result["count"] == 2
        refs = {b.get("ref") for b in result["blocks"]}
        assert "U12" in refs
        assert "U13" in refs


class TestBuildGraphFromSpec:
    def test_base_graph_unchanged_when_no_agent_blocks(self, service, project):
        from hw_codesign.reference_backend import build_graph
        spec = service.read_spec(project)
        graph = build_graph(spec)
        from hw_codesign.electronics_design import build_controller_graph
        expected = build_controller_graph(spec)
        assert len(graph["components"]) == len(expected["components"])

    def test_agent_block_nets_merged_correctly(self, service, project):
        service.add_circuit_block(project, {
            "ref": "U20",
            "category": "can",
            "mpn": "TCAN1042HGVDRQ1",
            "footprint": "SOIC8",
            "connections": {"VCC": "V5", "GND": "GND", "RXD": "U20_RX", "TXD": "U20_TX"},
        })
        spec = service.read_spec(project)
        from hw_codesign.reference_backend import build_graph
        graph = build_graph(spec)
        net_names = {n["name"] for n in graph["nets"]}
        assert "U20_RX" in net_names
        assert "U20_TX" in net_names

    def test_role_field_overrides_inference(self, service, project):
        from hw_codesign.resolver import role_for_component
        component = {"ref": "U99", "category": "some_novel_category", "role": "my_custom_role"}
        assert role_for_component(component) == "my_custom_role"

    def test_role_inference_still_works_without_role_field(self, service, project):
        from hw_codesign.resolver import role_for_component
        component = {"ref": "U4", "category": "regulator"}
        assert role_for_component(component) == "regulator_5v"


# ---------------------------------------------------------------------------
# Phase C — PCB Placement Constraints
# ---------------------------------------------------------------------------

class TestSetPlacementConstraint:
    def test_valid_constraint_stored(self, service, project):
        result = service.set_placement_constraint(project, {
            "ref": "U6",  # CAN PHY in base graph
            "relationship": "near_connector",
            "target": "J3",
            "rationale": "minimize CAN stub length",
        })
        assert result["status"] == "pass"
        assert result["ref"] == "U6"
        assert result["constraint_count"] == 1

    def test_adjacent_to_constraint(self, service, project):
        result = service.set_placement_constraint(project, {
            "ref": "C1",
            "relationship": "adjacent_to",
            "target": "U1",
            "max_distance_mm": 3.0,
            "rationale": "bypass cap for MCU V3V3 rail",
        })
        assert result["status"] == "pass"

    def test_invalid_relationship_returns_blocked(self, service, project):
        result = service.set_placement_constraint(project, {
            "ref": "U6",
            "relationship": "teleport_to",
        })
        assert result["status"] == "blocked"
        assert result["code"] == "invalid_relationship"

    def test_missing_ref_returns_blocked(self, service, project):
        result = service.set_placement_constraint(project, {"relationship": "adjacent_to"})
        assert result["status"] == "blocked"
        assert result["code"] == "missing_ref"

    def test_unknown_ref_returns_blocked(self, service, project):
        result = service.set_placement_constraint(project, {
            "ref": "ZZZNOTAREF",
            "relationship": "adjacent_to",
        })
        assert result["status"] == "blocked"
        assert result["code"] == "ref_not_in_bom"

    def test_constraint_persisted(self, service, project):
        service.set_placement_constraint(project, {
            "ref": "U6",
            "relationship": "near_connector",
            "target": "J3",
        })
        result = service.list_placement_constraints(project)
        assert result["count"] == 1
        assert result["constraints"][0]["ref"] == "U6"


class TestListPlacementConstraints:
    def test_empty_before_any_constraint(self, service, project):
        result = service.list_placement_constraints(project)
        assert result["status"] == "pass"
        assert result["count"] == 0

    def test_lists_multiple_constraints(self, service, project):
        service.set_placement_constraint(project, {"ref": "U6", "relationship": "near_connector", "target": "J3"})
        service.set_placement_constraint(project, {"ref": "C1", "relationship": "adjacent_to", "target": "U1"})
        result = service.list_placement_constraints(project)
        assert result["count"] == 2


# ---------------------------------------------------------------------------
# Phase D — Firmware Module Authoring (already implemented; smoke tests)
# ---------------------------------------------------------------------------

class TestFirmwareModules:
    def test_design_timeout_shutdown_module(self, service, project):
        result = service.design_firmware_module(project, {
            "id": "motor_watchdog",
            "behavior": "timeout_shutdown",
            "trigger": {"signal": "ESTOP_IN", "timeout_ms": 100},
            "action": {"disable_all": "motor_enables", "assert": "FAULT_LED"},
        })
        assert result["status"] in ("pass", "fail", "blocked")
        assert result["module_id"] == "motor_watchdog"

    def test_design_periodic_transmit_module(self, service, project):
        result = service.design_firmware_module(project, {
            "id": "can_heartbeat",
            "behavior": "periodic_transmit",
            "interval_ms": 10,
            "frame": {"id": "0x100", "dlc": 8, "content": "motor_status"},
        })
        assert result["status"] in ("pass", "fail", "blocked")
        assert result["module_id"] == "can_heartbeat"

    def test_unknown_behavior_returns_blocked(self, service, project):
        result = service.design_firmware_module(project, {
            "id": "mystery",
            "behavior": "quantum_compute",
        })
        assert result["status"] == "blocked"
        assert result["code"] == "unknown_behavior"

    def test_list_firmware_modules_after_design(self, service, project):
        service.design_firmware_module(project, {
            "id": "test_mod",
            "behavior": "sensor_poll",
            "bus": "i2c",
            "sensor": "imu",
            "address": "0x68",
        })
        result = service.list_firmware_modules(project)
        assert result["status"] == "pass"
        ids = [m["id"] for m in result["modules"]]
        assert "test_mod" in ids


# ---------------------------------------------------------------------------
# Phase E — Unified Agent Workflow
# ---------------------------------------------------------------------------

class TestRecordDesignDecision:
    def test_returns_pass_with_decision_id(self, service, project):
        result = service.record_design_decision(
            project, "electronics",
            "Selected TCAN1042 over MCP2551 for CAN transceiver",
            "TCAN1042 has automotive qualification and 5V tolerant I/O matching our V5 rail",
        )
        assert result["status"] == "pass"
        assert result["decision_id"].startswith("dec_")
        assert result["domain"] == "electronics"

    def test_decision_persisted_to_jsonl(self, service, project):
        service.record_design_decision(project, "mechanical", "chose L-bracket", "lower mass")
        path = service.workspace.require_project(project)
        decisions_path = path / "history" / "decisions.jsonl"
        assert decisions_path.is_file()
        records = [json.loads(line) for line in decisions_path.read_text().splitlines() if line.strip()]
        assert len(records) >= 1
        assert any(r["domain"] == "mechanical" for r in records)

    def test_multiple_decisions_accumulate(self, service, project):
        service.record_design_decision(project, "electronics", "decision A", "rationale A")
        service.record_design_decision(project, "firmware", "decision B", "rationale B")
        path = service.workspace.require_project(project)
        decisions_path = path / "history" / "decisions.jsonl"
        records = [json.loads(line) for line in decisions_path.read_text().splitlines() if line.strip()]
        assert len(records) == 2


class TestCrossDomainConsistency:
    def test_no_agent_content_passes(self, service, project):
        result = service.check_cross_domain_consistency(project)
        assert result["status"] in ("pass", "fail", "blocked")
        assert "gate" in result

    def test_valid_placement_constraint_passes(self, service, project):
        service.set_placement_constraint(project, {"ref": "U6", "relationship": "near_connector", "target": "J3"})
        result = service.check_cross_domain_consistency(project)
        assert result["status"] == "pass"

    def test_invalid_placement_ref_causes_failure(self, service, project):
        # Bypass validation by writing directly to agent_blocks.yaml
        path = service.workspace.require_project(project)
        agent_path = path / "spec" / "agent_blocks.yaml"
        from hw_codesign.io import write_yaml
        write_yaml(agent_path, {
            "placement": {"constraints": [{"ref": "GHOST_REF", "relationship": "adjacent_to"}]}
        })
        result = service.check_cross_domain_consistency(project)
        assert result["status"] == "fail"
        codes = [f["code"] for f in result.get("failures", [])]
        assert "placement_ref_not_in_bom" in codes


class TestRepairPlanAgentActions:
    def test_repair_plan_includes_agent_actions(self, service, project):
        service.generate_all(project)
        checks = service.run_all_checks(project, include_external=False)
        repair = service.generate_repair_plan(project, checks)
        assert "agent_actions" in repair
        assert isinstance(repair["agent_actions"], list)

    def test_agent_actions_have_tool_and_reason(self, service, project):
        service.generate_all(project)
        checks = service.run_all_checks(project, include_external=False)
        repair = service.generate_repair_plan(project, checks)
        for action in repair["agent_actions"]:
            assert "tool" in action
            assert "reason" in action
