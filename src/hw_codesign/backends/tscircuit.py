from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

from sexpdata import Symbol, loads

from ..footprint_library import canonical_footprint_geometry
from ..io import atomic_write_text, write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..provenance import artifact_provenance
from .electronics import ElectronicsBackendAdapter


class TSCircuitBackend(ElectronicsBackendAdapter):
    name = "tscircuit"
    VERSION = "0.1.1491"
    DEFAULT_TIMEOUT_SECONDS = 600

    def __init__(self, platform_root: Path, parts_root: Path | None = None):
        self.platform_root = platform_root
        self.parts_root = parts_root or platform_root / "parts"

    @staticmethod
    def _source_position(
        component: dict[str, Any],
        index: int,
        board_width: float,
        board_height: float,
    ) -> tuple[float, float, bool]:
        position = component.get("pcb_position_mm")
        has_solver_position = (
            isinstance(position, list)
            and len(position) == 2
            and all(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) for value in position)
        )
        if has_solver_position:
            board_x, board_y = float(position[0]), float(position[1])
        else:
            board_x = 8 + (index % 7) * max(8, (board_width - 16) / 6)
            board_y = 8 + (index // 7) * max(8, (board_height - 16) / 6)
        return board_x - board_width / 2, board_y - board_height / 2, has_solver_position

    @staticmethod
    def _sexp_head(form: Any, name: str) -> bool:
        return (
            isinstance(form, list)
            and bool(form)
            and isinstance(form[0], Symbol)
            and form[0].value() == name
        )

    @classmethod
    def _sexp_direct(cls, form: list[Any], name: str) -> list[list[Any]]:
        return [item for item in form[2:] if cls._sexp_head(item, name)]

    @staticmethod
    def _sexp_atom(value: Any) -> str:
        return value.value() if isinstance(value, Symbol) else str(value)

    @classmethod
    def _pin_number_maps(
        cls,
        component: dict[str, Any],
        footprint_id: str,
    ) -> tuple[dict[str, str], dict[str, str]]:
        """Map arbitrary graph pad identifiers onto tscircuit's numeric pins.

        tscircuit requires ``pinLabels`` keys to be numeric (``pin1`` etc.),
        while real KiCad footprints may use identifiers such as A1/B12/SH.
        Numeric graph pins retain their number; non-numeric pins receive stable
        positive integers in graph order.  The reverse map restores the exact
        graph identifiers during netlist and footprint parity checks.
        """
        ordered: list[str] = []
        for pin in component.get("pins", []):
            number = str(pin.get("number", ""))
            if number and number not in ordered:
                ordered.append(number)
        geometry = canonical_footprint_geometry(footprint_id)
        if geometry is not None:
            ordered.extend(number for number in geometry.numbered_pads if number not in ordered)

        graph_to_backend: dict[str, str] = {}
        used: set[int] = set()
        for number in ordered:
            if number.isdigit() and int(number) > 0 and int(number) not in used:
                graph_to_backend[number] = number
                used.add(int(number))
        candidate = 1
        for number in ordered:
            if number in graph_to_backend:
                continue
            while candidate in used:
                candidate += 1
            graph_to_backend[number] = str(candidate)
            used.add(candidate)
            candidate += 1
        return graph_to_backend, {backend: graph for graph, backend in graph_to_backend.items()}

    @classmethod
    def _canonical_footprint_elements(
        cls,
        footprint_id: str,
        graph_to_backend: dict[str, str],
    ) -> tuple[list[tuple[str, dict[str, Any]]], str] | None:
        """Translate a hash-verified vendored KiCad footprint into JSX pads.

        This keeps compilation offline and makes tscircuit consume the same pad
        geometry used by the KiCad reference renderer.  Only physical pad and
        tooling-hole primitives are needed for connectivity/layout parity.
        """
        geometry = canonical_footprint_geometry(footprint_id)
        if geometry is None or ":" not in footprint_id:
            return None
        asset = Path(__file__).parents[1] / "footprints" / f"{footprint_id.split(':', 1)[1]}.kicad_mod"
        if not asset.is_file() or sha256(asset.read_bytes()).hexdigest() != geometry.sha256:
            return None
        ast = loads(asset.read_text(encoding="utf-8"))
        if not isinstance(ast, list) or not cls._sexp_head(ast, "footprint"):
            return None

        elements: list[tuple[str, dict[str, Any]]] = []
        for pad in cls._sexp_direct(ast, "pad"):
            if len(pad) < 4:
                continue
            number = cls._sexp_atom(pad[1])
            pad_type = cls._sexp_atom(pad[2])
            pad_shape = cls._sexp_atom(pad[3])
            at = cls._sexp_direct(pad, "at")
            size = cls._sexp_direct(pad, "size")
            layers = cls._sexp_direct(pad, "layers")
            if not at or len(at[0]) < 3 or not size or len(size[0]) < 3:
                continue
            x_mm, y_mm = float(at[0][1]), -float(at[0][2])
            rotation_deg = -float(at[0][3]) if len(at[0]) > 3 else 0.0
            width_mm, height_mm = float(size[0][1]), float(size[0][2])
            layer_names = {cls._sexp_atom(item) for item in layers[0][1:]} if layers else set()
            copper = any(layer == "*.Cu" or layer.endswith(".Cu") for layer in layer_names)

            if pad_type == "np_thru_hole":
                if pad_shape == "circle":
                    elements.append(("hole", {"pcbX": x_mm, "pcbY": y_mm, "diameter": width_mm}))
                elif pad_shape == "oval":
                    elements.append(("hole", {
                        "pcbX": x_mm,
                        "pcbY": y_mm,
                        "shape": "pill",
                        "width": width_mm,
                        "height": height_mm,
                        "pcbRotation": rotation_deg,
                    }))
                continue
            if not copper:
                continue

            port_hints: list[str] = []
            if number:
                backend_number = graph_to_backend.get(number)
                if backend_number is None:
                    continue
                port_hints = [f"pin{backend_number}", cls._identifier(number) or f"PAD_{backend_number}"]

            common: dict[str, Any] = {"pcbX": x_mm, "pcbY": y_mm}
            if port_hints:
                common["portHints"] = port_hints
            if pad_type == "smd":
                if pad_shape == "circle":
                    props = {**common, "shape": "circle", "radius": width_mm / 2.0, "layer": "top"}
                elif pad_shape == "oval" and not rotation_deg:
                    props = {
                        **common,
                        "shape": "pill",
                        "width": width_mm,
                        "height": height_mm,
                        "radius": min(width_mm, height_mm) / 2.0,
                        "layer": "top",
                    }
                else:
                    shape = "rotated_rect" if rotation_deg else "rect"
                    props = {**common, "shape": shape, "width": width_mm, "height": height_mm, "layer": "top"}
                    ratio = cls._sexp_direct(pad, "roundrect_rratio")
                    if ratio and len(ratio[0]) > 1:
                        props["cornerRadius" if rotation_deg else "rectBorderRadius"] = (
                            float(ratio[0][1]) * min(width_mm, height_mm)
                        )
                    if rotation_deg:
                        props["ccwRotation"] = rotation_deg
                elements.append(("smtpad", props))
                continue

            if pad_type != "thru_hole":
                continue
            drill = cls._sexp_direct(pad, "drill")
            if not drill or len(drill[0]) < 2:
                continue
            if isinstance(drill[0][1], Symbol) and drill[0][1].value() == "oval":
                hole_width = float(drill[0][2])
                hole_height = float(drill[0][3])
                props = {
                    **common,
                    "shape": "oval",
                    "outerWidth": width_mm,
                    "outerHeight": height_mm,
                    "holeWidth": hole_width,
                    "holeHeight": hole_height,
                    "pcbRotation": rotation_deg,
                }
            else:
                hole_diameter = float(drill[0][1])
                if pad_shape == "circle":
                    props = {
                        **common,
                        "shape": "circle",
                        "holeDiameter": hole_diameter,
                        "outerDiameter": width_mm,
                    }
                else:
                    props = {
                        **common,
                        "shape": "circular_hole_with_rect_pad",
                        "holeDiameter": hole_diameter,
                        "rectPadWidth": width_mm,
                        "rectPadHeight": height_mm,
                    }
                    ratio = cls._sexp_direct(pad, "roundrect_rratio")
                    if ratio and len(ratio[0]) > 1:
                        props["rectBorderRadius"] = float(ratio[0][1]) * min(width_mm, height_mm)
            elements.append(("platedhole", props))
        return elements, geometry.sha256

    @staticmethod
    def _tsx_footprint(elements: list[tuple[str, dict[str, Any]]]) -> str:
        children = "".join(
            f"<{name} " + " ".join(f"{key}={{{json.dumps(value)}}}" for key, value in props.items()) + " />"
            for name, props in elements
        )
        return f"<footprint>{children}</footprint>"

    @staticmethod
    def _esm_footprint(elements: list[tuple[str, dict[str, Any]]]) -> str:
        children = ", ".join(
            f"React.createElement({json.dumps(name)}, {json.dumps(props, sort_keys=True)})"
            for name, props in elements
        )
        suffix = f", {children}" if children else ""
        return f"React.createElement(\"footprint\", null{suffix})"

    @staticmethod
    def _partition_circuit_errors(
        circuit_json: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Separate generation failures from downstream PCB validation errors.

        A successful tscircuit build may include ``pcb_*_error`` records for
        clearance, boundary, routing, or placement violations.  Those records
        must fail the layout gate, but they do not prevent extracting the
        compiled netlist or checking graph and footprint parity.  Source and
        schematic errors remain compile-fatal because they make those checks
        unreliable.
        """
        errors = [item for item in circuit_json if str(item.get("type", "")).endswith("_error")]
        pcb_errors = [item for item in errors if str(item.get("type", "")).startswith("pcb_")]
        compile_errors = [item for item in errors if not str(item.get("type", "")).startswith("pcb_")]
        return compile_errors, pcb_errors

    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        target = project / "electronics" / "source" / "tscircuit"
        target.mkdir(parents=True, exist_ok=True)
        components = []
        esm_components = []
        unsupported_footprints: list[dict[str, str]] = []
        missing_solver_placements: list[str] = []
        pin_number_aliases: dict[str, dict[str, dict[str, str]]] = {}
        canonical_footprints: list[dict[str, Any]] = []
        envelope = spec["mechanical"]["envelope"]
        board_width = envelope["board_width_mm"]
        board_height = envelope["board_height_mm"]
        board_name = re.sub(r"[^A-Za-z0-9_-]", "_", project.name) or "HardwareBoard"
        for index, item in enumerate(graph.get("components", [])):
            footprint_id = item.get("footprint_metadata", {}).get("library_id") or item.get("footprint") or ""
            graph_to_backend, backend_to_graph = self._pin_number_maps(item, footprint_id)
            pin_number_aliases[str(item["ref"])] = {
                "graph_to_backend": graph_to_backend,
                "backend_to_graph": backend_to_graph,
            }
            pin_by_number = {str(pin.get("number")): pin for pin in item.get("pins", [])}
            labels: dict[str, list[str]] = {}
            for graph_number, backend_number in graph_to_backend.items():
                pin = pin_by_number.get(graph_number, {})
                semantic = f"{self._identifier(str(pin.get('name') or 'PAD'))}_{self._identifier(graph_number) or backend_number}"
                physical = self._identifier(graph_number) or f"PAD_{backend_number}"
                labels[f"pin{backend_number}"] = list(dict.fromkeys((semantic, physical)))
            connections = {
                f"pin{graph_to_backend[str(pin['number'])]}": f"sel.net.{self._identifier(pin['net'])}"
                for pin in item.get("pins", [])
                if pin.get("net") and str(pin.get("number")) in graph_to_backend
            }

            canonical = self._canonical_footprint_elements(footprint_id, graph_to_backend)
            tscircuit_footprint = None
            if canonical is not None:
                elements, footprint_sha256 = canonical
                footprint_prop = f" footprint={{{self._tsx_footprint(elements)}}}"
                esm_extra = f", footprint: {self._esm_footprint(elements)}"
                canonical_footprints.append({
                    "ref": str(item["ref"]),
                    "library_id": footprint_id,
                    "sha256": footprint_sha256,
                    "physical_elements": len(elements),
                })
            else:
                tscircuit_footprint = (
                    item.get("footprint_metadata", {}).get("backend_footprints", {}).get("tscircuit")
                    or self._footprint(footprint_id)
                )
                footprint_prop = f" footprint={json.dumps(tscircuit_footprint)}" if tscircuit_footprint else ""
                esm_extra = f", footprint: {json.dumps(tscircuit_footprint)}" if tscircuit_footprint else ""
            if footprint_id and canonical is None and not tscircuit_footprint:
                unsupported_footprints.append({"ref": item["ref"], "footprint": footprint_id})
            labels_js = json.dumps(labels, sort_keys=True)
            conn_js = "{" + ", ".join(f"{json.dumps(key)}: {value}" for key, value in connections.items()) + "}"
            x, y, has_solver_position = self._source_position(item, index, board_width, board_height)
            rotation = float(item.get("pcb_rotation_deg", 0.0) or 0.0)
            if not has_solver_position:
                missing_solver_placements.append(str(item["ref"]))
            placement_prop = f" pcbX={{{x:.3f}}} pcbY={{{y:.3f}}} pcbRotation={{{rotation:.3f}}}"
            mpn_prop = " supplierPartNumbers={{lcsc: []}}"
            components.append(
                f'      <chip name={json.dumps(item["ref"])}{footprint_prop}{placement_prop}{mpn_prop} pinLabels={{{labels_js}}} connections={{{conn_js}}} />'
            )
            # connections must remain unquoted JS expressions (sel.net.*), not JSON strings
            esm_components.append(
                f"    React.createElement(\"chip\", {{ name: {json.dumps(item['ref'])}{esm_extra}, pcbX: {x:.3f}, pcbY: {y:.3f}, pcbRotation: {rotation:.3f}, pinLabels: {labels_js}, connections: {conn_js} }})"
            )
        source = (
            "import React from \"react\"\n"
            "import { sel } from \"tscircuit\"\n\n"
            "export default () => (\n"
            f'  <board name="{board_name}" width="{board_width}mm" height="{board_height}mm">\n'
            + "\n".join(components)
            + "\n  </board>\n)\n"
        )
        entry = target / "board.tsx"
        atomic_write_text(entry, source)
        compiler_entry = target / "board.compiler.mjs"
        esm = (
            "import React from \"react\"\n"
            "import { sel } from \"tscircuit\"\n\n"
            "export default () => React.createElement(\n"
            "  \"board\",\n"
            f"  {{ name: \"{board_name}\", width: \"{board_width}mm\", height: \"{board_height}mm\" }},\n"
            + ",\n".join(esm_components)
            + "\n)\n"
        )
        atomic_write_text(compiler_entry, esm)
        fabrication_release_eligible = not unsupported_footprints and not missing_solver_placements
        write_json(target / "source_manifest.json", {
            "backend": "tscircuit",
            "compiler_version": self.VERSION,
            "backend_release_capable": True,
            "release_tier": "fabrication",
            "source_release_eligible": fabrication_release_eligible,
            "netlist_release_eligible": False,
            "hdl_source_release_eligible": False,
            "fabrication_release_eligible": fabrication_release_eligible,
            "pcb_disabled": False,
            "routing_disabled": False,
            "unsupported_footprints": unsupported_footprints,
            "canonical_footprints": canonical_footprints,
            "pin_number_aliases": pin_number_aliases,
            "placement_contract": {
                "source": "electrical_graph.components[].pcb_position_mm + pcb_rotation_deg",
                "coordinate_transform": "board_origin_top_left_to_tscircuit_center",
                "solver_placements": len(graph.get("components", [])) - len(missing_solver_placements),
                "missing_solver_placements": missing_solver_placements,
            },
            "sources": self.source_entries(target, [entry, compiler_entry]),
            "contract_gates": list(self.gate_names),
            "release_blocking_gates": list(self.gate_names),
            "provenance": artifact_provenance(
                spec,
                self.parts_root,
                "tscircuit",
                compiler_version=self.VERSION,
                command=self.command(entry),
                release_eligible=fabrication_release_eligible,
                release_tier="fabrication",
            ),
        })
        return [str(entry), str(compiler_entry), str(target / "source_manifest.json")]

    def _tsx_bin(self) -> Path:
        name = "tsx.cmd" if sys.platform == "win32" else "tsx"
        return self.platform_root / "node_modules" / ".bin" / name

    def command(self, entry: Path) -> list[str]:
        compiler_entry = entry.with_name("board.compiler.mjs")
        try:
            entry_arg = compiler_entry.relative_to(self.platform_root).as_posix()
        except ValueError:
            entry_arg = compiler_entry.as_posix()
        return [
            str(self._tsx_bin()),
            str(self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js"),
            "build", entry_arg, "--ignore-config",
            "--disable-parts-engine",
        ]

    def _patch_windows_esm_imports(self) -> None:
        """Patch importFromUserLand in tscircuit bundles to use file:// URLs on Windows.

        tsx 4.22.4 does not convert Windows absolute paths to file:// URLs in its
        ESM load hook, causing ERR_UNSUPPORTED_ESM_URL_SCHEME on Node.js v22.
        This applies the same pathToFileURL fix that the rest of the bundle already uses.
        """
        targets = [
            self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "build" / "build.worker.js",
            self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js",
        ]
        fix_user = (
            'const _fixedUserPath = /^[A-Za-z]:[/\\\\]/.test(resolvedUserPath)'
            ' ? "file:///" + resolvedUserPath.replace(/\\\\/g, "/") : resolvedUserPath;\n'
            '      return await import(_fixedUserPath);'
        )
        fix_cli = (
            'const _fixedCliPath = /^[A-Za-z]:[/\\\\]/.test(resolvedCliPath)'
            ' ? "file:///" + resolvedCliPath.replace(/\\\\/g, "/") : resolvedCliPath;\n'
            '      return await import(_fixedCliPath);'
        )
        for target in targets:
            if not target.is_file():
                continue
            text = target.read_text(encoding="utf-8")
            changed = False
            if "return await import(resolvedUserPath);" in text:
                text = text.replace("return await import(resolvedUserPath);", fix_user)
                changed = True
            if "return await import(resolvedCliPath);" in text:
                text = text.replace("return await import(resolvedCliPath);", fix_cli)
                changed = True
            if changed:
                target.write_text(text, encoding="utf-8")

    def evaluate(self, project: Path, graph: dict[str, Any]) -> list[GateReport]:
        return self.complete_contract(self.compile(project, graph))

    def compile(self, project: Path, graph: dict[str, Any], timeout_seconds: int | None = None) -> list[GateReport]:
        timeout_seconds = _timeout_seconds(timeout_seconds, "HW_TSCIRCUIT_TIMEOUT_SECONDS", self.DEFAULT_TIMEOUT_SECONDS)
        entry = project / "electronics" / "source" / "tscircuit" / "board.tsx"
        cli = self.platform_root / "node_modules" / "@tscircuit" / "cli" / "dist" / "cli" / "main.js"
        if shutil.which("node") is None or not cli.is_file() or not self._tsx_bin().is_file():
            failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "Pinned Node.js tscircuit CLI is unavailable; run npm ci")
            return [
                GateReport(name, Status.BLOCKED, [failure], backend={"name": "tscircuit", "version": self.VERSION, "offline": True})
                for name in ("tscircuit_compile", "tscircuit_netlist_extract", "tscircuit_graph_parity",
                             "tscircuit_footprint_parity", "tscircuit_layout_completeness")
            ]
        if not entry.is_file():
            failure = Failure(FailureCategory.EDA_ERROR, "missing_design_source", "Generate tscircuit source before compilation")
            return [GateReport(name, Status.BLOCKED, [failure]) for name in (
                "tscircuit_compile", "tscircuit_netlist_extract", "tscircuit_graph_parity",
                "tscircuit_footprint_parity", "tscircuit_layout_completeness",
            )]
        shutil.rmtree(entry.parent / "dist", ignore_errors=True)
        if sys.platform == "win32":
            self._patch_windows_esm_imports()
        try:
            result = subprocess.run(self.command(entry), cwd=str(self.platform_root), capture_output=True, text=True, timeout=timeout_seconds)
        except OSError as exc:
            failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", f"tscircuit CLI could not be executed: {exc}")
            blocked = Failure(FailureCategory.TOOL_ERROR, "compile_prerequisite_failed", "Prerequisite compile gate did not pass")
            return [
                GateReport("tscircuit_compile", Status.BLOCKED, [failure], backend={"name": "tscircuit", "version": self.VERSION, "offline": True, "timeout_seconds": timeout_seconds}),
                GateReport("tscircuit_netlist_extract", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_graph_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_footprint_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_layout_completeness", Status.BLOCKED, [blocked]),
            ]
        except subprocess.TimeoutExpired as exc:
            failure = Failure(FailureCategory.TOOL_ERROR, "tool_timeout", f"tscircuit CLI did not complete within {timeout_seconds} s", details={"timeout_seconds": timeout_seconds, "stdout": (exc.stdout or "")[-4000:], "stderr": (exc.stderr or "")[-4000:]})
            blocked = Failure(FailureCategory.TOOL_ERROR, "compile_prerequisite_failed", "Prerequisite compile gate did not pass")
            return [
                GateReport("tscircuit_compile", Status.BLOCKED, [failure], backend={"name": "tscircuit", "version": self.VERSION, "offline": True, "timeout_seconds": timeout_seconds}),
                GateReport("tscircuit_netlist_extract", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_graph_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_footprint_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_layout_completeness", Status.BLOCKED, [blocked]),
            ]
        backend = {
            "name": "tscircuit", "version": self.VERSION, "offline": True,
            "timeout_seconds": timeout_seconds,
            "command": self.command(entry), "returncode": result.returncode,
            "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:],
        }
        if result.returncode != 0:
            failure = Failure(FailureCategory.EDA_ERROR, "tscircuit_compile_failed", "Pinned tscircuit compiler returned nonzero", details={"returncode": result.returncode, "stderr": result.stderr[-2000:]})
            blocked = Failure(FailureCategory.EDA_ERROR, "compile_prerequisite_failed", "Prerequisite compile gate did not pass")
            return [
                GateReport("tscircuit_compile", Status.FAIL, [failure], backend=backend),
                GateReport("tscircuit_netlist_extract", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_graph_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_footprint_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_layout_completeness", Status.BLOCKED, [blocked]),
            ]
        candidates = sorted(
            [*entry.parent.rglob("*.circuit.json"), *entry.parent.rglob("circuit.json")],
            key=lambda p: p.stat().st_mtime, reverse=True,
        )
        candidates.extend(
            sorted((self.platform_root / "dist").rglob("circuit.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            if (self.platform_root / "dist").is_dir() else []
        )
        if not candidates:
            failure = Failure(FailureCategory.EDA_ERROR, "compiled_netlist_missing", "tscircuit completed without a Circuit JSON output")
            blocked = Failure(FailureCategory.EDA_ERROR, "netlist_prerequisite_failed", "Prerequisite netlist gate did not pass")
            return [
                GateReport("tscircuit_compile", Status.PASS, backend=backend),
                GateReport("tscircuit_netlist_extract", Status.FAIL, [failure]),
                GateReport("tscircuit_graph_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_footprint_parity", Status.BLOCKED, [blocked]),
                GateReport("tscircuit_layout_completeness", Status.BLOCKED, [blocked]),
            ]
        compiled_path = candidates[0]
        compiled: list[dict[str, Any]] = json.loads(compiled_path.read_text(encoding="utf-8"))
        compiler_errors, pcb_errors = self._partition_circuit_errors(compiled)
        if compiler_errors:
            failure = Failure(FailureCategory.EDA_ERROR, "compiled_circuit_contains_errors", "tscircuit emitted Circuit JSON error elements", details={"count": len(compiler_errors), "types": sorted({item.get("type") for item in compiler_errors})})
            prerequisite = Failure(FailureCategory.EDA_ERROR, "compile_prerequisite_failed", "Prerequisite compile gate did not pass")
            return [
                GateReport("tscircuit_compile", Status.FAIL, [failure], artifacts=[str(compiled_path)], backend=backend),
                *[GateReport(name, Status.BLOCKED, [prerequisite], backend=backend) for name in self.gate_names[1:]],
            ]
        backend_pin_aliases = {
            str(component["ref"]): self._pin_number_maps(
                component,
                component.get("footprint_metadata", {}).get("library_id") or component.get("footprint") or "",
            )[1]
            for component in graph.get("components", [])
        }
        netlist = self.extract_netlist(compiled, backend_pin_aliases)
        netlist_path = project / "electronics" / "generated" / "tscircuit_netlist.json"
        write_json(netlist_path, netlist)
        expected = self.graph_netlist(graph)
        parity_failures = [] if netlist == expected else [
            Failure(FailureCategory.EDA_ERROR, "graph_parity_mismatch",
                    "Python resolved graph differs from compiled tscircuit netlist",
                    details={"expected": expected, "compiled": netlist})
        ]
        compile_gate = GateReport(
            "tscircuit_compile",
            Status.PASS,
            metrics={"circuit_elements": len(compiled), "pcb_validation_errors": len(pcb_errors)},
            artifacts=[str(compiled_path)],
            backend=backend,
        )
        netlist_gate = GateReport("tscircuit_netlist_extract", Status.PASS, metrics={"nets": len(netlist)}, artifacts=[str(netlist_path)], backend=backend)
        parity_gate = GateReport("tscircuit_graph_parity", Status.FAIL if parity_failures else Status.PASS, parity_failures, metrics={"expected_nets": len(expected), "compiled_nets": len(netlist)}, backend=backend)

        # PCB gates — require pcb_component and pcb_trace elements in circuit.json
        pcb_components = [item for item in compiled if item.get("type") == "pcb_component"]
        pcb_traces = [item for item in compiled if item.get("type") == "pcb_trace"]
        pcb_validation_failures = [
            Failure(
                FailureCategory.EDA_ERROR,
                "tscircuit_pcb_validation_error",
                str(item.get("message") or "tscircuit reported a PCB validation error"),
                details={
                    "type": str(item.get("type", "pcb_error")),
                    "pcb_component_id": item.get("pcb_component_id"),
                    "pcb_trace_id": item.get("pcb_trace_id"),
                },
            )
            for item in pcb_errors
        ]
        all_component_refs = {item["ref"] for item in graph.get("components", [])}
        source_components = {item.get("source_component_id"): item for item in compiled if item.get("type") == "source_component"}
        placed_refs = {source_components.get(item.get("source_component_id"), {}).get("name") for item in pcb_components}

        if not pcb_components:
            pcb_blocked = Failure(FailureCategory.EDA_ERROR, "pcb_layout_absent",
                                  "tscircuit produced no pcb_component entries; PCB layout was not generated")
            footprint_gate = GateReport("tscircuit_footprint_parity", Status.BLOCKED, [pcb_blocked], backend=backend)
            layout_gate = GateReport(
                "tscircuit_layout_completeness",
                Status.BLOCKED,
                [pcb_blocked, *pcb_validation_failures],
                backend=backend,
            )
        else:
            # Footprint parity checks compiled pad numbers against the curated footprint contract.
            pcb_by_source = {item.get("source_component_id"): item.get("pcb_component_id") for item in pcb_components}
            pads_by_pcb: dict[str, set[str]] = {}
            for pad in compiled:
                if pad.get("type") not in {"pcb_smtpad", "pcb_plated_hole"}:
                    continue
                pads_by_pcb.setdefault(pad.get("pcb_component_id"), set()).update(str(hint).removeprefix("pin") for hint in pad.get("port_hints", []) if str(hint).removeprefix("pin").isdigit())
            footprint_failures: list[Failure] = []
            for component in graph.get("components", []):
                expected = set(map(str, component.get("footprint_metadata", {}).get("expected_pads", []))) or {str(pin["number"]) for pin in component.get("pins", [])}
                source_id = next((key for key, value in source_components.items() if value.get("name") == component["ref"]), None)
                backend_pads = pads_by_pcb.get(pcb_by_source.get(source_id), set())
                pin_aliases = backend_pin_aliases.get(str(component["ref"]), {})
                compiled_pads = {pin_aliases.get(number, number) for number in backend_pads}
                if expected != compiled_pads:
                    footprint_failures.append(Failure(
                        FailureCategory.EDA_ERROR, "footprint_pad_parity_mismatch",
                        f"{component['ref']}: compiled pad contract differs from curated footprint metadata",
                        details={"ref": component["ref"], "expected_pads": sorted(expected), "compiled_pads": sorted(compiled_pads)},
                    ))
            footprint_gate = GateReport(
                "tscircuit_footprint_parity",
                Status.FAIL if footprint_failures else Status.PASS,
                footprint_failures,
                metrics={"components_checked": len(all_component_refs), "pcb_components": len(pcb_components)},
                backend=backend,
            )
            # Layout completeness: every component must have a placed pcb_component
            unplaced = sorted(all_component_refs - placed_refs)
            layout_failures = [
                Failure(FailureCategory.EDA_ERROR, "component_unplaced", f"{ref} has no PCB placement in circuit.json", details={"ref": ref})
                for ref in unplaced
            ]
            layout_failures.extend(pcb_validation_failures)
            placement_parity_failures, placement_parity_checked = self.placement_parity_failures(compiled, graph)
            layout_failures.extend(placement_parity_failures)
            layout_failures += [
                Failure(FailureCategory.EDA_ERROR, "pcb_traces_absent", "tscircuit produced no pcb_trace entries; routing may be deferred")
            ] if not pcb_traces else []
            layout_gate = GateReport(
                "tscircuit_layout_completeness",
                Status.FAIL if layout_failures else Status.PASS,
                layout_failures,
                metrics={
                    "placed": len(pcb_components),
                    "total": len(all_component_refs),
                    "traces": len(pcb_traces),
                    "placement_parity_checked": placement_parity_checked,
                    "placement_parity_failures": len(placement_parity_failures),
                    "placement_tolerance_mm": 0.05,
                    "placement_rotation_tolerance_deg": 0.05,
                    "pcb_validation_errors": len(pcb_errors),
                },
                backend=backend,
            )

        return [compile_gate, netlist_gate, parity_gate, footprint_gate, layout_gate]

    @staticmethod
    def _footprint(library_id: str) -> str | None:
        if not library_id or library_id.startswith("HW_Curated:"):
            return None
        if ":" in library_id:
            library, name = library_id.split(":", 1)
            return f"kicad:{library}/{name}"
        normalized = library_id.lower()
        if re.fullmatch(r"(?:0402|0603|0805|1206|1210|soic\d+|sot23(?:_5)?|qfn\d+|qfp\d+|pinrow\d+)", normalized):
            return normalized
        return None

    @staticmethod
    def _identifier(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9_]", "_", value)

    @staticmethod
    def _rotation_degrees(value: Any) -> float | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value) if math.isfinite(value) else None
        if not isinstance(value, str):
            return None
        match = re.fullmatch(
            r"\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*(deg|rad)?\s*",
            value,
            flags=re.IGNORECASE,
        )
        if match is None:
            return None
        parsed = float(match.group(1))
        if match.group(2) and match.group(2).lower() == "rad":
            parsed = math.degrees(parsed)
        return parsed if math.isfinite(parsed) else None

    @staticmethod
    def _rotation_error_degrees(actual: float, expected: float) -> float:
        return abs((actual - expected + 180.0) % 360.0 - 180.0)

    @classmethod
    def placement_parity_failures(
        cls,
        circuit_json: list[dict[str, Any]],
        graph: dict[str, Any],
        tolerance_mm: float = 0.05,
        rotation_tolerance_deg: float = 0.05,
    ) -> tuple[list[Failure], int]:
        placement = graph.get("placement", {})
        board_width = placement.get("board_width_mm")
        board_height = placement.get("board_height_mm")
        if not isinstance(board_width, (int, float)) or not isinstance(board_height, (int, float)):
            return [Failure(
                FailureCategory.EDA_ERROR,
                "solver_placement_contract_missing",
                "Electrical graph does not carry the board dimensions required for tscircuit placement parity",
            )], 0

        source_components = {
            item.get("source_component_id"): item.get("name")
            for item in circuit_json
            if item.get("type") == "source_component" and item.get("source_component_id") and item.get("name")
        }
        pcb_by_ref = {
            source_components.get(item.get("source_component_id")): item
            for item in circuit_json
            if item.get("type") == "pcb_component"
            and source_components.get(item.get("source_component_id"))
        }
        failures: list[Failure] = []
        checked = 0
        for index, component in enumerate(graph.get("components", [])):
            ref = str(component.get("ref", "?"))
            expected_x, expected_y, has_solver_position = cls._source_position(
                component,
                index,
                float(board_width),
                float(board_height),
            )
            if not has_solver_position:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "solver_component_placement_missing",
                    f"{ref} has no solver-derived pcb_position_mm for tscircuit placement",
                    details={"ref": ref},
                ))
                continue
            compiled = pcb_by_ref.get(ref)
            if compiled is None:
                continue
            center = compiled.get("center") or {}
            display_x = compiled.get("display_offset_x")
            display_y = compiled.get("display_offset_y")
            has_display_origin = (
                isinstance(display_x, (int, float))
                and isinstance(display_y, (int, float))
            )
            compiled_x = display_x if has_display_origin else center.get("x")
            compiled_y = display_y if has_display_origin else center.get("y")
            if not isinstance(compiled_x, (int, float)) or not isinstance(compiled_y, (int, float)):
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "compiled_component_position_missing",
                    f"{ref} pcb_component has no numeric placement origin in Circuit JSON",
                    details={
                        "ref": ref,
                        "display_offset_x": display_x,
                        "display_offset_y": display_y,
                        "center": center,
                    },
                ))
                continue
            checked += 1
            error_mm = math.hypot(float(compiled_x) - expected_x, float(compiled_y) - expected_y)
            if error_mm > tolerance_mm:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "placement_coordinate_mismatch",
                    f"{ref} compiled tscircuit placement origin differs from the solver proposal by {error_mm:.3f} mm",
                    details={
                        "ref": ref,
                        "solver_board_position_mm": component.get("pcb_position_mm"),
                        "expected_tscircuit_origin_mm": [round(expected_x, 3), round(expected_y, 3)],
                        "compiled_tscircuit_origin_mm": [compiled_x, compiled_y],
                        "error_mm": round(error_mm, 6),
                        "tolerance_mm": tolerance_mm,
                        "placement_source": component.get("placement_source"),
                    },
                ))
            expected_rotation_value = component.get("pcb_rotation_deg", 0.0)
            expected_rotation = cls._rotation_degrees(expected_rotation_value)
            if expected_rotation is None:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "solver_component_rotation_invalid",
                    f"{ref} has a non-numeric pcb_rotation_deg in the electrical graph",
                    details={"ref": ref, "pcb_rotation_deg": expected_rotation_value},
                ))
                continue

            compiled_rotation_value = compiled.get("rotation")
            if compiled_rotation_value is None:
                if cls._rotation_error_degrees(expected_rotation, 0.0) <= rotation_tolerance_deg:
                    continue
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "compiled_component_rotation_missing",
                    f"{ref} pcb_component has no rotation in Circuit JSON",
                    details={
                        "ref": ref,
                        "expected_rotation_deg": expected_rotation,
                        "rotation_tolerance_deg": rotation_tolerance_deg,
                    },
                ))
                continue

            compiled_rotation = cls._rotation_degrees(compiled_rotation_value)
            if compiled_rotation is None:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "compiled_component_rotation_invalid",
                    f"{ref} pcb_component has a non-numeric rotation in Circuit JSON",
                    details={"ref": ref, "rotation": compiled_rotation_value},
                ))
                continue

            rotation_error_deg = cls._rotation_error_degrees(compiled_rotation, expected_rotation)
            if rotation_error_deg > rotation_tolerance_deg:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "placement_rotation_mismatch",
                    f"{ref} compiled tscircuit rotation differs from the solver proposal by {rotation_error_deg:.3f} degrees",
                    details={
                        "ref": ref,
                        "expected_rotation_deg": expected_rotation,
                        "compiled_rotation_deg": compiled_rotation,
                        "rotation_error_deg": round(rotation_error_deg, 6),
                        "rotation_tolerance_deg": rotation_tolerance_deg,
                        "placement_source": component.get("placement_source"),
                    },
                ))
        return failures, checked

    @staticmethod
    def extract_netlist(
        circuit_json: list[dict[str, Any]],
        pin_number_aliases: dict[str, dict[str, str]] | None = None,
    ) -> dict[str, list[str]]:
        pin_number_aliases = pin_number_aliases or {}
        source_components = {
            item.get("source_component_id"): item.get("name")
            for item in circuit_json
            if item.get("source_component_id") and item.get("name")
        }
        ports = {
            item.get("source_port_id"): (
                source_components.get(item.get("source_component_id")),
                str(item.get("pin_number") or item.get("name", "")).removeprefix("pin"),
            )
            for item in circuit_json
            if item.get("type") == "source_port"
        }
        net_objects = {item.get("source_net_id"): item.get("name") for item in circuit_json if item.get("type") == "source_net"}
        nets: dict[str, set[str]] = {}
        for item in circuit_json:
            if item.get("type") != "source_trace":
                continue
            net_ids = item.get("connected_source_net_ids") or []
            name = net_objects.get(net_ids[0]) if net_ids else None
            if not name:
                continue
            for port_id in item.get("connected_source_port_ids") or []:
                ref, number = ports.get(port_id, (None, None))
                if ref and number:
                    graph_number = pin_number_aliases.get(ref, {}).get(number, number)
                    nets.setdefault(name, set()).add(f"{ref}.{graph_number}")
        return {name: sorted(values) for name, values in sorted(nets.items())}


def _timeout_seconds(value: int | None, env_name: str, default: int) -> int:
    raw = value if value is not None else os.environ.get(env_name, default)
    try:
        parsed = int(raw)
    except (TypeError, ValueError):
        return default
    return max(1, parsed)
