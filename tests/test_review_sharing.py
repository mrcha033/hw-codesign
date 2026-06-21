from __future__ import annotations

import http.server
import json
import socket
import threading
from pathlib import Path

from hw_codesign.review_viewer import _merge_bundle, build_standalone_html

# ---------------------------------------------------------------------------
# Standalone HTML export
# ---------------------------------------------------------------------------

def _minimal_bundle(**overrides) -> dict:
    base = {
        "bundle_version": "1.0",
        "bundle_hash": "abc123def456",
        "generated_at": "2026-06-17T00:00:00+00:00",
        "project": {"name": "test_proj", "revision": "r1", "target_use": "test", "backend": "reference"},
        "gate_reports": [],
        "summary": {"total": 0, "pass": 0, "fail": 0, "blocked": 0, "other": 0},
        "placement": None, "requirements": None, "assumptions": None,
        "iterations": [], "candidates": [], "release": None, "artifacts": [], "comments": [],
    }
    return {**base, **overrides}


def test_build_standalone_html_embeds_data():
    bundle = _minimal_bundle()
    html = build_standalone_html(bundle)
    assert "<!DOCTYPE html>" in html
    assert "window.__BUNDLE_DATA=" in html
    assert "abc123def456" in html


def test_build_standalone_html_includes_comments():
    bundle = _minimal_bundle()
    comments = [{"id": "c1", "text": "looks good", "author": "alice", "timestamp": "2026-06-17T00:00:00+00:00"}]
    html = build_standalone_html(bundle, comments)
    assert "looks good" in html
    assert "alice" in html


def test_build_standalone_html_no_add_comment_link():
    bundle = _minimal_bundle()
    html = build_standalone_html(bundle)
    # The add-comment link is gated behind !window.__BUNDLE_DATA in JS.
    # Verify the guard is present so the link is never rendered in standalone mode.
    assert "window.__BUNDLE_DATA?" in html
    assert "window.__BUNDLE_DATA" in html


def test_build_standalone_html_no_polling():
    bundle = _minimal_bundle()
    html = build_standalone_html(bundle)
    # setInterval must only fire when NOT standalone (guarded by __BUNDLE_DATA check).
    assert "if(!window.__BUNDLE_DATA) setInterval" in html


def test_build_standalone_html_script_injection_safe():
    # Values containing </script> in the bundle must not break the page.
    bundle = _minimal_bundle()
    bundle["project"]["name"] = "evil</script><script>alert(1)</script>"
    html = build_standalone_html(bundle)
    # The raw </script> must not appear unescaped inside the data block.
    # Our escaping replaces </ with <\/
    assert "<\\/script>" in html or "evil</script><script>" not in html


def test_export_standalone_review_produces_file(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.export_standalone_review(project)
    assert result["status"] == "generated"
    assert result["bundle_hash"]
    path = Path(result["file"])
    assert path.is_file()
    html = path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html
    assert "window.__BUNDLE_DATA=" in html
    assert project in html


def test_export_standalone_review_embeds_comments(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    service.add_review_comment(project, "important note", author="alice")
    result = service.export_standalone_review(project)
    html = Path(result["file"]).read_text(encoding="utf-8")
    assert "important note" in html
    assert result["comment_count"] == 1


# ---------------------------------------------------------------------------
# Multi-project dashboard
# ---------------------------------------------------------------------------

def test_list_project_summaries_empty_workspace(service):
    result = service.list_project_summaries()
    assert result["status"] == "generated"
    assert result["projects"] == []


def test_list_project_summaries_no_bundle(service, project):
    result = service.list_project_summaries()
    assert len(result["projects"]) == 1
    entry = result["projects"][0]
    assert entry["name"] == project
    assert entry["has_bundle"] is False


def test_list_project_summaries_with_bundle(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    service.export_review(project)
    result = service.list_project_summaries()
    entry = result["projects"][0]
    assert entry["has_bundle"] is True
    assert entry["total"] > 0
    assert entry["bundle_hash"]
    assert entry["generated_at"]


def test_list_projects_workspace(service):
    service.create_project("alpha_board")
    service.create_project("beta_board")
    names = service.workspace.list_projects()
    assert "alpha_board" in names
    assert "beta_board" in names
    assert names == sorted(names)


# ---------------------------------------------------------------------------
# Review comments (collaboration)
# ---------------------------------------------------------------------------

def test_add_review_comment_creates_sidecar(service, project):
    result = service.add_review_comment(project, "looks good", author="alice")
    assert result["status"] == "generated"
    assert result["comment_id"]
    assert result["timestamp"]
    sidecar = (
        service.workspace.require_project(project)
        / "exports" / "working" / "review" / "comments.jsonl"
    )
    assert sidecar.is_file()
    entry = json.loads(sidecar.read_text().strip())
    assert entry["text"] == "looks good"
    assert entry["author"] == "alice"
    assert entry["target_type"] == "general"


def test_add_review_comment_gate_target(service, project):
    result = service.add_review_comment(
        project, "erc clean", target_type="gate_failure", target_id="erc"
    )
    assert result["status"] == "generated"
    sidecar = (
        service.workspace.require_project(project)
        / "exports" / "working" / "review" / "comments.jsonl"
    )
    entry = json.loads(sidecar.read_text().strip())
    assert entry["target_type"] == "gate_failure"
    assert entry["target_id"] == "erc"


def test_list_review_comments_empty(service, project):
    result = service.list_review_comments(project)
    assert result["status"] == "generated"
    assert result["comments"] == []
    assert result["count"] == 0


def test_list_review_comments_round_trip(service, project):
    service.add_review_comment(project, "first")
    service.add_review_comment(project, "second", author="bob")
    result = service.list_review_comments(project)
    assert result["count"] == 2
    texts = [c["text"] for c in result["comments"]]
    assert "first" in texts
    assert "second" in texts


def test_comments_appear_in_merged_bundle(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    export = service.export_review(project)
    service.add_review_comment(project, "review note")
    bundle_path = Path(export["file"])
    comments_path = bundle_path.parent / "comments.jsonl"
    merged = _merge_bundle(bundle_path, comments_path)
    assert len(merged["comments"]) == 1
    assert merged["comments"][0]["text"] == "review note"
    # bundle.json must not be modified
    original = json.loads(bundle_path.read_bytes())
    assert original["comments"] == []


# ---------------------------------------------------------------------------
# Hosted upload
# ---------------------------------------------------------------------------

def _find_free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _CaptureHandler(http.server.BaseHTTPRequestHandler):
    received: list[bytes] = []

    def log_message(self, *_): pass

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        self.__class__.received.append(self.rfile.read(length))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")


def _start_capture_server(port: int) -> http.server.HTTPServer:
    server = http.server.HTTPServer(("127.0.0.1", port), _CaptureHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def test_upload_review_posts_bundle(service, project):
    _CaptureHandler.received = []
    port = _find_free_port()
    server = _start_capture_server(port)
    try:
        service.generate_all(project)
        service.run_all_checks(project, include_external=False)
        result = service.upload_review(project, destination=f"http://127.0.0.1:{port}/api/upload")
        assert result["status"] == "generated"
        assert result["http_status"] == 200
        assert result["bundle_hash"]
        assert len(_CaptureHandler.received) == 1
        posted = json.loads(_CaptureHandler.received[0])
        assert posted["bundle_hash"] == result["bundle_hash"]
        assert posted["project"]["name"] == project
    finally:
        server.shutdown()


def test_upload_review_returns_fail_on_connection_error(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    result = service.upload_review(project, destination="http://127.0.0.1:1/api/upload")
    assert result["status"] == "fail"
    assert result["code"] == "upload_failed"


def test_upload_review_blocked_without_destination(service, project):
    result = service.upload_review(project)
    assert result["status"] == "blocked"
    assert result["code"] == "destination_required"
