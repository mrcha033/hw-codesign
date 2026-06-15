from __future__ import annotations

from typing import Any

# Hand-tuned anchor coordinates for the robotics-controller reference design.
# These are the authoritative placement seed: they are tuned so the reference
# board routes and clears the enclosure. The structured placement-proposal layer
# in ``placement.py`` builds provenance, constraints, and checks on top of them
# but never moves them. Keeping the coordinates here unchanged guarantees the
# tuned routing and mechanical gates keep producing identical output.
_ANCHORS: dict[str, tuple[float, float]] = {
    "J1": (20.0, 5.0), "F1": (38.0, 5.0), "Q1": (56.0, 5.0), "D1": (74.0, 5.0),
    "U3": (92.0, 5.0), "U4": (112.0, 18.0), "U5": (132.0, 18.0),
    "J5": (120.0, 95.0), "D2": (42.0, 27.0), "R4": (60.0, 27.0), "U6": (90.0, 27.0),
    "J3": (80.0, 5.0), "R1": (136.0, 27.0), "U2": (22.0, 48.0), "R2": (42.0, 48.0),
    "R3": (58.0, 48.0), "J2": (140.0, 95.0), "Q2": (124.0, 48.0), "J4": (104.0, 69.0),
    "U1": (70.0, 37.0),
}


def _seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    """Provenance-tagged seed coordinates.

    Each entry maps a reference to ``((x_mm, y_mm), source)`` where ``source``
    records how the seed coordinate was derived: a hand-tuned anchor, a
    decoupling-capacitor row, or a connector pushed to a board edge.
    """
    table: dict[str, tuple[tuple[float, float], str]] = {
        ref: (xy, "curated_anchor") for ref, xy in _ANCHORS.items()
    }
    for index in range(10):
        table[f"C{index + 1}"] = ((24.0 + (index % 5) * 22.0, 76.0 + (index // 5) * 13.0), "decoupling_row_seed")
    for index in range(1, 13):
        side_index = (index - 1) % 6
        table[f"J{index + 10}"] = ((3.0 if index <= 6 else 157.0, 7.0 + side_index * 15.0), "connector_edge_seed")
    return table


def _grid_fallback(index: int) -> tuple[float, float]:
    return (10.0 + (index % 7) * 20.0, 10.0 + (index // 7) * 15.0)


def component_positions(graph: dict[str, Any]) -> dict[str, tuple[float, float]]:
    """Backward-compatible coordinate lookup (ref -> (x_mm, y_mm))."""
    table = _seed_table()
    return {
        item["ref"]: table[item["ref"]][0] if item["ref"] in table else _grid_fallback(index)
        for index, item in enumerate(graph.get("components", []))
    }


def placement_sources(graph: dict[str, Any]) -> dict[str, str]:
    """Provenance tag for each placed reference (mirrors ``component_positions``)."""
    table = _seed_table()
    return {
        item["ref"]: table[item["ref"]][1] if item["ref"] in table else "grid_fallback"
        for item in graph.get("components", [])
    }
