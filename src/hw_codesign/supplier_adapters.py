from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NormalizedSupplierOffer:
    provider: str
    component_id: str
    sku: str | None
    availability: str
    stock: int | None
    observed_at: str | None
    source_record: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "component_id": self.component_id,
            "sku": self.sku,
            "availability": self.availability,
            "stock": self.stock,
            "observed_at": self.observed_at,
            "source_record": self.source_record,
        }


class SupplierAdapter:
    provider: str

    def normalize(self, record: dict[str, Any]) -> NormalizedSupplierOffer:
        raise NotImplementedError

    def _offer(
        self,
        record: dict[str, Any],
        *,
        sku: str | None,
        availability: str,
        stock: int | None,
        observed_at: str | None,
    ) -> NormalizedSupplierOffer:
        return NormalizedSupplierOffer(
            provider=self.provider,
            component_id=str(record["component_id"]),
            sku=sku,
            availability=availability,
            stock=stock,
            observed_at=observed_at,
            source_record=record,
        )


class CuratedSupplierAdapter(SupplierAdapter):
    provider = "curated"

    def normalize(self, record: dict[str, Any]) -> NormalizedSupplierOffer:
        return self._offer(
            record,
            sku=record.get("supplier_sku"),
            availability=record.get("availability", "unknown"),
            stock=record.get("stock"),
            observed_at=record.get("observed_at"),
        )


class LcscJlcpcbAdapter(SupplierAdapter):
    provider = "lcsc_jlcpcb"

    def normalize(self, record: dict[str, Any]) -> NormalizedSupplierOffer:
        return self._offer(
            record,
            sku=record.get("lcsc_part_number"),
            availability=record.get("availability", "unknown"),
            stock=record.get("jlcpcb_stock"),
            observed_at=record.get("observed_at"),
        )


class DistributorMetadataAdapter(SupplierAdapter):
    def __init__(self, provider: str):
        if provider not in {"digikey", "mouser", "octopart"}:
            raise ValueError(f"Unsupported distributor provider: {provider}")
        self.provider = provider

    def normalize(self, record: dict[str, Any]) -> NormalizedSupplierOffer:
        return self._offer(
            record,
            sku=record.get("sku"),
            availability=record.get("availability", "unknown"),
            stock=record.get("stock"),
            observed_at=record.get("observed_at"),
        )


def supplier_adapter(provider: str) -> SupplierAdapter:
    if provider == "curated":
        return CuratedSupplierAdapter()
    if provider == "lcsc_jlcpcb":
        return LcscJlcpcbAdapter()
    if provider in {"digikey", "mouser", "octopart"}:
        return DistributorMetadataAdapter(provider)
    raise ValueError(f"Unsupported supplier provider: {provider}")
