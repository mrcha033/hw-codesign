from __future__ import annotations

import heapq
import math
from collections import defaultdict
from typing import Any

GRID_MM = 0.25
LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")


def route_board(
    nets: list[dict[str, Any]],
    pad_positions: dict[str, list[tuple[float, float]]],
    width_mm: float,
    height_mm: float,
    route_signals: bool = True,
    layers: tuple[str, ...] = LAYERS,
    plane_layer_by_net: dict[str, str] | None = None,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    occupied: dict[tuple[int, int, int], str] = {}
    segments: list[str] = []
    vias: list[str] = []
    failures: list[dict[str, Any]] = []
    max_x, max_y = int(width_mm / GRID_MM), int(height_mm / GRID_MM)
    pad_cells = {name: [_cell(point) for point in points] for name, points in pad_positions.items()}
    all_pads: dict[tuple[int, int], set[str]] = defaultdict(set)
    for name, cells in pad_cells.items():
        for cell in cells:
            all_pads[cell].add(name)

    plane_layer_names = plane_layer_by_net or {"GND": "In1.Cu", "V5": "In2.Cu", "V3V3": "B.Cu"}
    plane_layers = {net: layers.index(layer) for net, layer in plane_layer_names.items() if layer in layers}
    def routing_priority(item):
        cells = pad_cells[item["name"]]
        span = (max((x for x, _ in cells), default=0) - min((x for x, _ in cells), default=0)) + (max((y for _, y in cells), default=0) - min((y for _, y in cells), default=0))
        return (0 if item["name"] in plane_layers else 1, -item["required_track_width_mm"], -span, -len(cells), item["name"])

    ordered = sorted(
        (item for item in nets if route_signals or item["name"] in plane_layers),
        key=routing_priority,
    )
    for net_index, net in enumerate(ordered):
        name = net["name"]
        endpoints = list(dict.fromkeys(pad_cells[name]))
        if len(endpoints) < 2:
            continue
        clearance_cells = max(1, math.ceil((net["required_track_width_mm"] / 2 + 0.15) / GRID_MM))
        pad_clearance_cells = max(1, math.ceil((net["required_track_width_mm"] / 2 + 0.375 + 0.2) / GRID_MM))
        net_paths = None
        failed_endpoints = []
        layer_order = [plane_layers[name]] if name in plane_layers else [(net_index + offset) % len(layers) for offset in range(len(layers))]
        for layer in layer_order:
            trial_occupied = dict(occupied)
            tree = {(endpoints[0][0], endpoints[0][1], layer)}
            trial_paths: list[list[tuple[int, int, int]]] = []
            trial_failures = []
            remaining = set(endpoints[1:])
            while remaining:
                endpoint = min(
                    remaining,
                    key=lambda point: min(abs(point[0] - x) + abs(point[1] - y) for x, y, _ in tree),
                )
                path = _astar([(endpoint[0], endpoint[1], layer)], tree, trial_occupied, all_pads, name, max_x, max_y, clearance_cells, pad_clearance_cells, layer_count=len(layers), allowed_layers={layer}, nearest_goal=True)
                if path is None:
                    trial_failures.append(endpoint)
                    break
                trial_paths.append(path); tree.update(path)
                _reserve(path, trial_occupied, name, clearance_cells, max_x, max_y)
                remaining.remove(endpoint)
            if not trial_failures:
                occupied = trial_occupied; net_paths = trial_paths
                break
            failed_endpoints = trial_failures
        if net_paths is None and name not in plane_layers:
            trial_occupied = dict(occupied)
            tree = {(endpoints[0][0], endpoints[0][1], layer) for layer in range(len(layers))}
            trial_paths = []
            remaining = set(endpoints[1:])
            while remaining:
                endpoint = min(
                    remaining,
                    key=lambda point: min(abs(point[0] - x) + abs(point[1] - y) for x, y, _ in tree),
                )
                starts = [(endpoint[0], endpoint[1], layer) for layer in layer_order]
                path = _astar(starts, tree, trial_occupied, all_pads, name, max_x, max_y, clearance_cells, pad_clearance_cells, layer_count=len(layers), nearest_goal=True)
                if path is None:
                    failed_endpoints = [endpoint]
                    break
                trial_paths.append(path); tree.update(path)
                _reserve(path, trial_occupied, name, clearance_cells, max_x, max_y)
                remaining.remove(endpoint)
            else:
                occupied = trial_occupied; net_paths = trial_paths
        if net_paths is None:
            for endpoint in failed_endpoints or endpoints[1:2]:
                failures.append({"net": name, "endpoint_mm": [endpoint[0] * GRID_MM, endpoint[1] * GRID_MM], "reason": "no_clear_single_layer_path"})
            continue
        for path in net_paths:
            path_segments, path_vias = _emit(path, net["required_track_width_mm"], net["id"], layers)
            segments.extend(path_segments)
            vias.extend(path_vias)
    return segments, vias, failures


def _astar(starts, goals, occupied, all_pads, net, max_x, max_y, clearance, pad_clearance, layer_count=len(LAYERS), allowed_layers=None, nearest_goal=False):
    queue: list[tuple[float, int, tuple[int, int, int]]] = []
    distance: dict[tuple[int, int, int], float] = {}
    previous: dict[tuple[int, int, int], tuple[int, int, int] | None] = {}
    serial = 0
    goal_states = set(goals)
    goal_points = {(x, y) for x, y, _ in goal_states}
    if nearest_goal:
        start_x, start_y, _ = starts[0]
        nearest = min(goal_points, key=lambda point: abs(point[0] - start_x) + abs(point[1] - start_y))
        goal_points = {nearest}
    goals = {
        state for state in goal_states
        if (state[0], state[1]) in goal_points and (allowed_layers is None or state[2] in allowed_layers)
    }
    goal_bounds = (
        min(x for x, _ in goal_points),
        max(x for x, _ in goal_points),
        min(y for _, y in goal_points),
        max(y for _, y in goal_points),
    )
    expansions = 0
    for state in starts:
        distance[state] = 0.0; previous[state] = None
        heapq.heappush(queue, (_heuristic(state, goal_bounds), serial, state)); serial += 1
    while queue:
        expansions += 1
        if expansions > 50_000:
            return None
        _, _, state = heapq.heappop(queue)
        if state in goals:
            path = []
            while state is not None:
                path.append(state); state = previous[state]
            return list(reversed(path))
        x, y, layer = state
        neighbors = [(x + 1, y, layer, 1.0), (x - 1, y, layer, 1.0), (x, y + 1, layer, 1.0), (x, y - 1, layer, 1.0)]
        if allowed_layers is None:
            neighbors.extend((x, y, other, 6.0) for other in range(layer_count) if other != layer)
        for nx, ny, nl, cost in neighbors:
            candidate = (nx, ny, nl)
            if nx < 2 or ny < 2 or nx > max_x - 2 or ny > max_y - 2:
                continue
            via_move = nl != layer
            if not _available(candidate, occupied, all_pads, net, clearance, pad_clearance, all_layers=via_move):
                continue
            new_distance = distance[state] + cost
            if new_distance >= distance.get(candidate, float("inf")):
                continue
            distance[candidate] = new_distance; previous[candidate] = state
            heapq.heappush(queue, (new_distance + _heuristic(candidate, goal_bounds), serial, candidate)); serial += 1
    return None


def _available(state, occupied, all_pads, net, clearance, pad_clearance, all_layers=False):
    x, y, layer = state
    checked_layers = range(len(LAYERS)) if all_layers else (layer,)
    for checked_layer in checked_layers:
        for dx in range(-clearance, clearance + 1):
            for dy in range(-clearance, clearance + 1):
                owner = occupied.get((x + dx, y + dy, checked_layer))
                if owner is not None and owner != net:
                    return False
    for dx in range(-pad_clearance, pad_clearance + 1):
        for dy in range(-pad_clearance, pad_clearance + 1):
            pad_owners = all_pads.get((x + dx, y + dy), set())
            if pad_owners and net not in pad_owners:
                return False
    return True


def _reserve(path, occupied, net, clearance, max_x, max_y):
    for index, (x, y, layer) in enumerate(path):
        is_via = (index > 0 and path[index - 1][2] != layer) or (index + 1 < len(path) and path[index + 1][2] != layer)
        layers = range(len(LAYERS)) if is_via else (layer,)
        for dx in range(-clearance, clearance + 1):
            for dy in range(-clearance, clearance + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx <= max_x and 0 <= ny <= max_y:
                    for checked_layer in layers:
                        occupied.setdefault((nx, ny, checked_layer), net)


def _emit(path, width, net_id, layers):
    if len(path) < 2:
        return [], []
    segments: list[str] = []
    vias: list[str] = []
    run_start = path[0]
    previous = path[0]
    previous_direction = None
    for current in path[1:]:
        if current[2] != previous[2]:
            if run_start != previous:
                segments.append(_segment(run_start, previous, width, net_id, layers))
            vias.append(f'  (via (at {current[0] * GRID_MM:.3f} {current[1] * GRID_MM:.3f}) (size 0.8) (drill 0.4) (layers "{layers[0]}" "{layers[-1]}") (net {net_id}))')
            run_start = current; previous_direction = None
        else:
            direction = (current[0] - previous[0], current[1] - previous[1])
            if previous_direction is not None and direction != previous_direction:
                segments.append(_segment(run_start, previous, width, net_id, layers)); run_start = previous
            previous_direction = direction
        previous = current
    if run_start != previous:
        segments.append(_segment(run_start, previous, width, net_id, layers))
    return segments, list(dict.fromkeys(vias))


def _segment(start, end, width, net_id, layers):
    layer = layers[start[2]]
    return f'  (segment (start {start[0] * GRID_MM:.3f} {start[1] * GRID_MM:.3f}) (end {end[0] * GRID_MM:.3f} {end[1] * GRID_MM:.3f}) (width {width:.3f}) (layer "{layer}") (net {net_id}))'


def _heuristic(state, bounds):
    x, y, _ = state
    min_x, max_x, min_y, max_y = bounds
    dx = min_x - x if x < min_x else (x - max_x if x > max_x else 0)
    dy = min_y - y if y < min_y else (y - max_y if y > max_y else 0)
    return dx + dy


def _cell(point):
    return round(point[0] / GRID_MM), round(point[1] / GRID_MM)
