"""Parametric build123d enclosure source generated from the project spec."""
BOARD = (160.0, 100.0, 1.6)
INTERNAL = (166.0, 106.0, 28.0)
WALL = 2.4
TOP_HEIGHT = 18.0
BOTTOM_HEIGHT = 3.0
INSERTION_CLEARANCE = 2.0
MOUNTING_HOLES = ((6.0, 6.0), (BOARD[0] - 6.0, 6.0), (6.0, BOARD[1] - 6.0), (BOARD[0] - 6.0, BOARD[1] - 6.0))
CONNECTOR_CUTOUTS = ((0.0, 18.0, 12.0, 10.0), (INTERNAL[0], 50.0, 12.0, 16.0))

def build():
    try:
        from build123d import Box, Cylinder, Pos, export_step, export_stl
    except ImportError as exc:
        raise RuntimeError("build123d is required to export enclosure geometry") from exc
    outer = Box(INTERNAL[0] + 2 * WALL, INTERNAL[1] + 2 * WALL, INTERNAL[2] + WALL)
    cavity = Pos(WALL, WALL, WALL) * Box(INTERNAL[0], INTERNAL[1], INTERNAL[2] + WALL)
    base = outer - cavity
    bosses = None
    for x, y in MOUNTING_HOLES:
        boss = Pos(WALL + x, WALL + y, WALL) * (Cylinder(3.2, 4.0) - Cylinder(1.6, 4.0))
        bosses = boss if bosses is None else bosses + boss
    lid = Pos(0, 0, INTERNAL[2] + WALL + 0.5) * Box(INTERNAL[0] + 2 * WALL, INTERNAL[1] + 2 * WALL, WALL)
    return {"base": base + bosses, "lid": lid, "assembly": base + bosses + lid}
