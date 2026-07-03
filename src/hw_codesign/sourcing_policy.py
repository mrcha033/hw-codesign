from __future__ import annotations

from typing import Any

from .models import Failure, FailureCategory


def sourcing_waiver_failures(sourcing: dict[str, Any], *, path: str = "electronics.components") -> list[Failure]:
    if sourcing.get("status") != "waived":
        return []
    waiver = sourcing.get("waiver") or {}
    required_text = ["reason", "risk", "mitigation", "approved_by", "approved_at"]
    missing = [field for field in required_text if not str(waiver.get(field) or "").strip()]
    reviews = waiver.get("required_reviews")
    if not isinstance(reviews, list) or not all(isinstance(item, str) and item.strip() for item in reviews):
        missing.append("required_reviews")
    if not missing:
        return []
    return [
        Failure(
            FailureCategory.BOM_ERROR,
            "sourcing_waiver_unreviewed",
            "Sourcing waiver requires reason, risk, mitigation, approval, and required review evidence",
            path=path,
            details={"missing": sorted(set(missing)), "waiver": waiver},
        )
    ]
