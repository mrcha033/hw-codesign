from __future__ import annotations

from typing import Any


CONNECTOR_CATEGORIES = {"power_input", "can_connector", "usb", "estop", "motor_io"}


def build_mechanical_contract(spec: dict[str, Any], graph: dict[str, Any]) -> dict[str, Any]:
    mechanical = spec["mechanical"]
    envelope = mechanical["envelope"]
    board_origin = list(map(float, mechanical.get("board_origin_mm", [0.0, 0.0, 0.0])))
    components = {item["ref"]: item for item in graph.get("components", [])}
    default_height = float(mechanical.get("default_component_height_mm", 4.0))
    overrides = mechanical.get("component_heights_mm", {})
    height_map = [
        {
            "ref": item["ref"],
            "x_mm": float(item.get("pcb_position_mm", [0.0, 0.0])[0]),
            "y_mm": float(item.get("pcb_position_mm", [0.0, 0.0])[1]),
            "height_mm": float(overrides.get(item["ref"], default_height)),
            "category": item.get("category"),
        }
        for item in graph.get("components", [])
    ]
    cutouts = []
    for interface in mechanical.get("connector_interfaces", []):
        component = components.get(interface["ref"])
        position = component.get("pcb_position_mm") if component else None
        cutouts.append({
            **interface,
            "component_present": component is not None,
            "electrical_category": component.get("category") if component else None,
            "pcb_position_mm": position,
            "enclosure_position_mm": [board_origin[0] + position[0], board_origin[1] + position[1]] if position else None,
        })
    return {
        "contract_version": 1,
        "provenance": {
            key: graph.get("provenance", {}).get(key)
            for key in ("source_spec_hash", "component_db_hash", "role_set_hash")
        },
        "selected_variant": mechanical["selected_variant"],
        "variants": mechanical["variants"],
        "board": {
            "width_mm": float(envelope["board_width_mm"]),
            "height_mm": float(envelope["board_height_mm"]),
            "thickness_mm": float(envelope["board_thickness_mm"]),
            "max_component_height_top_mm": float(envelope["max_component_height_top_mm"]),
            "max_component_height_bottom_mm": float(envelope["max_component_height_bottom_mm"]),
            "origin_mm": board_origin,
            "component_height_map": height_map,
        },
        "enclosure": {
            "internal_mm": list(map(float, mechanical["enclosure_internal_mm"])),
            "wall_thickness_mm": float(mechanical["wall_thickness_mm"]),
        },
        "clearances": {
            "insertion_mm": float(mechanical["insertion_clearance_mm"]),
            "assembly_mm": float(mechanical["assembly_clearance_mm"]),
            "tolerance_mm": float(mechanical["tolerance_mm"]),
            "max_connector_edge_distance_mm": float(mechanical.get("max_connector_edge_distance_mm", 6.0)),
        },
        "mounting_holes": mechanical["mounting_holes"],
        "fixtures": mechanical.get("fixtures", {}),
        "connector_cutouts": cutouts,
        "connector_component_refs": sorted(item["ref"] for item in graph.get("components", []) if item.get("category") in CONNECTOR_CATEGORIES),
    }
