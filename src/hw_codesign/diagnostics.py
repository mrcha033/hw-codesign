from __future__ import annotations

import re
from typing import Any

GATE_DEPENDENCIES: dict[str, list[str]] = {
    "requirements_lowering": ["spec_schema"],
    "semantic_electrical": ["spec_schema", "requirements_lowering"],
    "component_resolution": ["spec_schema"],
    "semantic_schematic_roundtrip": ["semantic_electrical", "component_resolution"],
    "datasheet_evidence": ["component_resolution"],
    "supplier_availability": ["component_resolution"],
    "bom": ["component_resolution"],
    "sourcing": ["component_resolution"],
    "sourcing_resilience": ["component_resolution", "sourcing", "component_provenance"],
    "component_provenance": ["component_resolution", "datasheet_evidence"],
    "pin_symbol_footprint": ["component_resolution", "component_provenance"],
    "power_tree_integrity": ["pin_symbol_footprint", "component_provenance"],
    "power_integrity_estimate": ["power_tree_integrity", "pin_symbol_footprint"],
    "interface_integrity": ["pin_symbol_footprint", "power_tree_integrity"],
    "firmware_pinmap": ["pin_symbol_footprint", "semantic_schematic_roundtrip"],
    "firmware_modules": ["firmware_pinmap", "hw_sw_parity"],
    "support_circuit_completeness": ["component_resolution", "semantic_electrical", "semantic_schematic_roundtrip", "power_tree_integrity", "interface_integrity"],
    "hw_sw_parity": ["firmware_pinmap", "pin_symbol_footprint", "semantic_schematic_roundtrip", "interface_integrity"],
    "firmware_interface_contract": ["firmware_pinmap", "hw_sw_parity", "interface_integrity"],
    "reference_firmware_build": ["firmware_pinmap", "firmware_modules", "firmware_interface_contract"],
    "placement_constraints": ["pin_symbol_footprint", "semantic_schematic_roundtrip"],
    "layout_thermal_integrity": ["placement_constraints", "power_tree_integrity", "interface_integrity"],
    "layout_signal_integrity": ["placement_constraints", "interface_integrity"],
    "ir_pcb_sanity": ["pin_symbol_footprint", "placement_constraints", "layout_thermal_integrity", "layout_signal_integrity", "semantic_schematic_roundtrip"],
    "reference_fabrication": ["ir_pcb_sanity", "placement_constraints", "layout_thermal_integrity", "layout_signal_integrity"],
    "compiled_electronics_backend": ["pin_symbol_footprint", "semantic_schematic_roundtrip"],
    "autoroute": ["ir_pcb_sanity"],
    "native_erc": ["pin_symbol_footprint"],
    "native_drc": ["ir_pcb_sanity"],
    "kicad_library_crosscheck": ["native_erc", "native_drc"],
    "mechanical_connector_cutouts": ["mechanical_fit", "placement_constraints"],
    "mechanical_mounting_integrity": ["mechanical_fit", "placement_constraints"],
    "native_mechanical_validation": ["mechanical_fit", "mechanical_connector_retention", "mechanical_connector_cutouts", "mechanical_mounting_integrity", "reference_fabrication"],
    "native_zephyr_build": ["firmware_pinmap", "firmware_modules", "firmware_interface_contract", "reference_firmware_build"],
    "physical_qualification": ["reference_fabrication", "reference_firmware_build", "firmware_modules", "firmware_interface_contract", "mechanical_fit", "mechanical_connector_retention", "mechanical_connector_cutouts", "mechanical_mounting_integrity", "layout_thermal_integrity", "layout_signal_integrity"],
    "release": ["compiled_electronics_backend", "reference_fabrication", "reference_firmware_build", "physical_qualification"],
}

_AGGREGATE_GATES = frozenset({"release", "design_dependency_graph", "candidate_critic", "artifact_integrity"})
_DERIVED_CODES = frozenset({"compile_prerequisite_failed", "gate_not_run", "failed_gate", "missing_export", "dependency_prerequisite_not_passed", "compiled_electronics_backend_required"})


def analyze_root_causes(reports: list[dict[str, Any]]) -> dict[str, Any]:
    by_gate = {str(report.get("gate")): report for report in reports if report.get("gate") and report.get("status") in {"fail", "blocked"}}
    unpassed = set(by_gate)
    parents = {gate: set(GATE_DEPENDENCIES.get(gate, [])) & unpassed for gate in unpassed}
    for gate, report in by_gate.items():
        parents[gate].update(_failure_prerequisites(report) & unpassed)
    roots = [gate for gate in unpassed if gate not in _AGGREGATE_GATES and not parents[gate]]
    if not roots:
        roots = [gate for gate, report in by_gate.items() if gate not in _AGGREGATE_GATES and not _is_purely_derived(report)]
    if not roots:
        roots = sorted(unpassed - _AGGREGATE_GATES)

    reverse: dict[str, set[str]] = {gate: set() for gate in unpassed}
    for gate, gate_parents in parents.items():
        for parent in gate_parents:
            reverse.setdefault(parent, set()).add(gate)
    entries = []
    for gate in roots:
        report = by_gate[gate]
        affected = sorted(_descendants(gate, reverse) - {gate})
        failures = report.get("failures", [])
        codes = sorted({str(failure.get("code", "unknown")) for failure in failures})
        summary = str(failures[0].get("message")) if failures else f"{gate} did not pass"
        entries.append({
            "id": f"{gate}:{'+'.join(codes) if codes else 'unpassed'}",
            "gate": gate,
            "status": report.get("status"),
            "failure_codes": codes,
            "summary": summary,
            "affected_gates": affected,
            "impact_count": len(affected),
            "failures": failures,
        })
    entries.sort(key=lambda item: (0 if item["status"] == "fail" else 1, -item["impact_count"], item["gate"]))
    for index, item in enumerate(entries, 1):
        item["repair_order"] = index
    return {
        "status": "generated",
        "root_causes": entries,
        "top_root_causes": entries[:3],
        "affected_gates": sorted({gate for item in entries for gate in item["affected_gates"]}),
        "repair_order": [item["gate"] for item in entries],
        "unpassed_gate_count": len(unpassed),
        "root_cause_count": len(entries),
        "folded_gate_count": max(0, len(unpassed) - len(entries)),
    }


def _failure_prerequisites(report: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for failure in report.get("failures", []):
        details = failure.get("details", {})
        for key in ("prerequisite", "required_gate", "gate"):
            value = details.get(key)
            if isinstance(value, str):
                found.add(value)
        message = str(failure.get("message", ""))
        match = re.search(r"(?:Required gate did not pass|prerequisite)[: ]+([a-z0-9_]+)", message, re.IGNORECASE)
        if match:
            found.add(match.group(1))
    return found


def _is_purely_derived(report: dict[str, Any]) -> bool:
    codes = {str(failure.get("code", "")) for failure in report.get("failures", [])}
    return bool(codes) and codes <= _DERIVED_CODES


def _descendants(root: str, reverse: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    pending = [root]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(reverse.get(current, ()))
    return seen
