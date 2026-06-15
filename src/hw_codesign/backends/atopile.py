from __future__ import annotations

from pathlib import Path
from typing import Any

from ..io import atomic_write_text, write_json
from ..provenance import artifact_provenance
from .electronics import ElectronicsBackendAdapter


class AtopileBackend(ElectronicsBackendAdapter):
    name = "atopile"

    def __init__(self, platform_root: Path):
        self.platform_root = platform_root

    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        target = project / "electronics" / "source" / self.name
        target.mkdir(parents=True, exist_ok=True)
        intent = target / "design.ato.intent.md"
        atomic_write_text(intent, "---\nartifact_type: design_intent\ncompiled: false\nrelease_eligible: false\nsource_of_truth: false\nbackend: atopile\n---\n\nAtopile source generation is not implemented. This file is not compiler input.\n")
        manifest = target / "source_manifest.json"
        write_json(manifest, {
            "backend": self.name,
            "backend_release_capable": False,
            "source_release_eligible": False,
            "sources": self.source_entries(target, [intent]),
            "contract_gates": list(self.gate_names),
            "release_blocking_gates": list(self.gate_names),
            "provenance": artifact_provenance(spec, self.platform_root / "parts", self.name, command=[], release_eligible=False),
        })
        return [str(intent), str(manifest)]

    def evaluate(self, project: Path, graph: dict[str, Any]):
        return self.blocked_contract("backend_not_implemented", "Atopile adapter exists, but compiler source generation and parity extraction are not implemented")
