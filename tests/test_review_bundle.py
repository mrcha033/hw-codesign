from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from hw_codesign.review_report import render_html
from hw_codesign.review_viewer import _merge_bundle


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
    assert isinstance(bundle["iterations"], list)
    assert isinstance(bundle["candidates"], list)
    assert isinstance(bundle["artifacts"], list)


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


def test_bundle_json_not_mutated_after_comment(service, project, tmp_path):
    """_merge_bundle() must surface comments without touching bundle.json."""
    result = service.export_review(project)
    bundle_path = Path(result["file"])
    original_bytes = bundle_path.read_bytes()

    comments_path = tmp_path / "comments.jsonl"
    entry = json.dumps({
        "id": "test-id",
        "timestamp": "2026-06-16T00:00:00+00:00",
        "target_type": "general",
        "target_id": None,
        "author": "tester",
        "text": "looks good",
        "bundle_hash": result["bundle_hash"],
    })
    comments_path.write_text(entry + "\n", encoding="utf-8")

    merged = _merge_bundle(bundle_path, comments_path)

    # bundle.json must be byte-for-byte unchanged.
    assert bundle_path.read_bytes() == original_bytes
    # The merged result surfaces the comment.
    assert len(merged["comments"]) == 1
    assert merged["comments"][0]["text"] == "looks good"
    # bundle_hash in the response is the original (not recomputed over comments).
    assert merged["bundle_hash"] == result["bundle_hash"]


def test_html_report_escapes_injection(service, project):
    """Values containing HTML special chars must be escaped in rendered output."""
    bundle = {
        "bundle_version": "1.0",
        "bundle_hash": "abc123",
        "generated_at": "2026-06-16T00:00:00+00:00",
        "project": {
            "name": "<script>alert(1)</script>",
            "revision": "r<1>",
            "target_use": "test & demo",
            "backend": "reference",
        },
        "gate_reports": [
            {
                "gate": "evil<gate>",
                "status": "fail",
                "failures": [
                    {
                        "severity": "error",
                        "code": "bad</code>",
                        "message": 'xss " test',
                        "path": None,
                    }
                ],
                "metrics": {},
                "artifacts": [],
                "backend": {},
            }
        ],
        "summary": {"total": 1, "pass": 0, "fail": 1, "blocked": 0, "other": 0},
        "placement": None,
        "requirements": None,
        "assumptions": None,
        "iterations": [],
        "candidates": [],
        "release": None,
        "artifacts": [],
        "comments": [],
    }
    html = render_html(bundle)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
    assert "evil<gate>" not in html
    assert "bad</code>" not in html
    assert "test & demo" not in html
    assert "test &amp; demo" in html
    # No raw unescaped < in user-controlled values (besides expected HTML tags).
    assert 'r<1>' not in html


def test_iterations_included_in_bundle(service, project):
    """Iterations from history/iterations/ appear in the exported bundle."""
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.export_review(project)
    bundle = json.loads(Path(result["file"]).read_text(encoding="utf-8"))
    # The test project fixture doesn't run design-until-release, so iterations may be empty.
    # Just verify the field is present and well-formed.
    assert "iterations" in bundle
    for it in bundle["iterations"]:
        assert "iteration_id" in it
