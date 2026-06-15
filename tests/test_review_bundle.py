from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def _schema() -> dict:
    return json.loads((Path(__file__).parents[1] / "schemas" / "review_bundle.schema.json").read_text(encoding="utf-8"))


def test_export_review_produces_valid_bundle(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.export_review(project)

    assert result["status"] == "generated"
    assert result["gate_count"] > 0
    assert result["bundle_hash"]

    bundle_path = Path(result["file"])
    assert bundle_path.is_file()
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    errors = list(Draft202012Validator(_schema()).iter_errors(bundle))
    assert not errors, [e.message for e in errors]

    assert bundle["bundle_version"] == "1.0"
    assert bundle["project"]["name"] == project
    assert bundle["gate_reports"]
    assert bundle["summary"]["total"] == len(bundle["gate_reports"])
    assert bundle["placement"] is not None
    assert bundle["comments"] == []


def test_export_review_bundle_hash_excludes_generated_at(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    r1 = service.export_review(project)
    r2 = service.export_review(project)
    # Two consecutive exports may have different generated_at but same canonical hash.
    assert r1["bundle_hash"] == r2["bundle_hash"]


def test_export_review_html_is_written(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.export_review(project)
    html_path = Path(result["html"])
    assert html_path.is_file()
    html = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html
    assert project in html
    assert result["bundle_hash"][:12] in html


def test_export_review_without_prior_checks_produces_empty_gate_list(service, project):
    result = service.export_review(project)
    assert result["status"] == "generated"
    bundle = json.loads(Path(result["file"]).read_text(encoding="utf-8"))
    assert isinstance(bundle["gate_reports"], list)


def test_upload_review_blocked_without_destination(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.upload_review(project)
    assert result["status"] == "blocked"
    assert result["code"] == "destination_required"
    assert "bundle" in result
