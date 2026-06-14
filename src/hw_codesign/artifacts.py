from __future__ import annotations

import hashlib
import json
import math
import struct
import zipfile
from pathlib import Path
from typing import Iterable

from .io import atomic_write_text, write_json


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deterministic_zip(output: Path, files: Iterable[tuple[Path, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, archive_name in sorted(files, key=lambda item: item[1]):
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())


def write_manifest(root: Path, output: Path) -> str:
    entries = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path != output:
            entries.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    write_json(output, {"algorithm": "sha256", "artifacts": entries})
    return str(output)


def simple_pdf(title: str, lines: list[str], output: Path) -> None:
    escaped = [line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") for line in [title, *lines]]
    commands = ["BT", "/F1 16 Tf", "50 790 Td", f"({escaped[0]}) Tj", "/F1 10 Tf"]
    for line in escaped[1:]:
        commands.extend(("0 -16 Td", f"({line}) Tj"))
    commands.append("ET")
    stream = "\n".join(commands).encode("ascii", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    content = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(content)); content.extend(f"{index} 0 obj\n".encode()); content.extend(obj); content.extend(b"\nendobj\n")
    xref = len(content); content.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]: content.extend(f"{offset:010d} 00000 n \n".encode())
    content.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(content)


def box_stl(width: float, depth: float, height: float, wall: float, output: Path) -> None:
    """Write a watertight open-top enclosure shell as deterministic ASCII STL."""
    outer = _box_triangles(0, 0, 0, width, depth, height)
    inner = _box_triangles(wall, wall, wall, width - wall, depth - wall, height + wall)
    triangles = outer + [(c, b, a) for a, b, c in inner]
    lines = ["solid enclosure"]
    for a, b, c in triangles:
        normal = _normal(a, b, c)
        lines.append(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}")
        lines.append("    outer loop")
        lines.extend(f"      vertex {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}" for p in (a, b, c))
        lines.extend(("    endloop", "  endfacet"))
    lines.append("endsolid enclosure")
    atomic_write_text(output, "\n".join(lines) + "\n")


def _box_triangles(x0: float, y0: float, z0: float, x1: float, y1: float, z1: float):
    p = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return [(p[a], p[b], p[c]) for a, b, c in faces]


def _normal(a, b, c):
    u = tuple(b[i] - a[i] for i in range(3))
    v = tuple(c[i] - a[i] for i in range(3))
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    length = math.sqrt(sum(value * value for value in n)) or 1.0
    return tuple(value / length for value in n)


def step_box(name: str, width: float, depth: float, height: float, output: Path) -> None:
    """Write a compact AP214 faceted BREP box accepted by standard STEP readers."""
    points = [(0, 0, 0), (width, 0, 0), (width, depth, 0), (0, depth, 0), (0, 0, height), (width, 0, height), (width, depth, height), (0, depth, height)]
    faces = [(1, 4, 3, 2), (5, 6, 7, 8), (1, 2, 6, 5), (2, 3, 7, 6), (3, 4, 8, 7), (4, 1, 5, 8)]
    data = ["ISO-10303-21;", "HEADER;", "FILE_DESCRIPTION(('HW co-design deterministic faceted model'),'2;1');", f"FILE_NAME('{name}.step','1980-01-01T00:00:00',('hw-codesign'),('hw-codesign'),'hw-codesign','hw-codesign','');", "FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));", "ENDSEC;", "DATA;"]
    index = 1
    point_ids = []
    for x, y, z in points:
        data.append(f"#{index}=CARTESIAN_POINT('',({x:.6f},{y:.6f},{z:.6f}));")
        point_ids.append(index)
        index += 1
    face_ids = []
    for face in faces:
        loop_points = ",".join(f"#{point_ids[item - 1]}" for item in (*face, face[0]))
        data.append(f"#{index}=POLY_LOOP('',({loop_points}));")
        loop_id = index; index += 1
        data.append(f"#{index}=FACE_OUTER_BOUND('',#{loop_id},.T.);")
        bound_id = index; index += 1
        data.append(f"#{index}=FACE('',(#{bound_id}));")
        face_ids.append(index); index += 1
    data.append(f"#{index}=CLOSED_SHELL('',({','.join(f'#{item}' for item in face_ids)}));")
    shell_id = index; index += 1
    data.append(f"#{index}=FACETED_BREP('{name}',#{shell_id});")
    data.extend(("ENDSEC;", "END-ISO-10303-21;"))
    atomic_write_text(output, "\n".join(data) + "\n")
