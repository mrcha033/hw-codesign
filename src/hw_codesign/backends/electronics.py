from __future__ import annotations

from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path
from typing import Any

from ..models import Failure, FailureCategory, GateReport, Status


CONTRACT_STAGES = (
    "compile",
    "netlist_extract",
    "graph_parity",
    "footprint_parity",
    "layout_completeness",
    "manufacturing_export",
)


class ElectronicsBackendAdapter(ABC):
    name: str

    @property
    def gate_names(self) -> tuple[str, ...]:
        return tuple(f"{self.name}_{stage}" for stage in CONTRACT_STAGES)

    @abstractmethod
    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, project: Path, graph: dict[str, Any]) -> list[GateReport]:
        raise NotImplementedError

    def blocked_contract(self, code: str, message: str, *, category: FailureCategory = FailureCategory.TOOL_ERROR) -> list[GateReport]:
        failure = Failure(category, code, message)
        return [GateReport(gate, Status.BLOCKED, [failure], backend={"name": self.name}) for gate in self.gate_names]

    def complete_contract(self, reports: list[GateReport]) -> list[GateReport]:
        by_gate = {report.gate: report for report in reports}
        for gate in self.gate_names:
            if gate not in by_gate:
                by_gate[gate] = GateReport(
                    gate,
                    Status.BLOCKED,
                    [Failure(FailureCategory.EDA_ERROR, "gate_not_run", f"Backend contract gate was not run: {gate}")],
                    backend={"name": self.name},
                )
        return [by_gate[gate] for gate in self.gate_names]

    @staticmethod
    def source_entries(root: Path, paths: list[Path]) -> list[dict[str, str]]:
        return [
            {"path": path.relative_to(root).as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}
            for path in sorted(paths)
        ]

    @staticmethod
    def graph_netlist(graph: dict[str, Any]) -> dict[str, list[str]]:
        return {item["name"]: sorted(item.get("connected_pins", [])) for item in graph.get("nets", [])}
