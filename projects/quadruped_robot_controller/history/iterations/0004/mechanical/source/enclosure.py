"""Parametric enclosure source generated from the project spec."""
BOARD = (160.0, 100.0, 1.6)
INTERNAL = (166.0, 106.0, 28.0)
WALL = 2.4

def build():
    try:
        from build123d import Box
    except ImportError as exc:
        raise RuntimeError("build123d is required to export enclosure geometry") from exc
    return Box(INTERNAL[0] + 2 * WALL, INTERNAL[1] + 2 * WALL, INTERNAL[2] + WALL)
