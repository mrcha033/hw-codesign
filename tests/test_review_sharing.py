from __future__ import annotations

import hashlib
import http.server
import json
import socket
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from hw_codesign import review_viewer
from hw_codesign.review_viewer import (
    _DASHBOARD_HTML,
    _RECEIVER_HTML,
    _VIEWER_HTML,
    _Handler,
    _merge_bundle,
    _ReceiverHandler,
    build_standalone_html,
)

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
    assert html.index("window.__BUNDLE_DATA=") < html.index("const STATUS_COLOR")


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


# ---------------------------------------------------------------------------
# Review receiver security
# ---------------------------------------------------------------------------

def _receiver_bundle() -> dict:
    canonical = {
        "bundle_version": "1.0",
        "project": {"name": "receiver_test", "revision": "r1"},
        "summary": {"total": 1, "pass": 1, "fail": 0, "blocked": 0},
        "gate_reports": [],
    }
    digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        **canonical,
        "bundle_hash": digest,
        "generated_at": "2026-07-18T00:00:00+00:00",
    }


def _start_receiver_server(inbox_dir: Path) -> http.server.HTTPServer:
    inbox_dir.mkdir(parents=True, exist_ok=True)

    class Handler(_ReceiverHandler):
        pass

    Handler.inbox_dir = inbox_dir.resolve()
    Handler.port = 0
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    Handler.port = server.server_port
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _receiver_request(
    server: http.server.HTTPServer,
    path: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, bytes]:
    request = urllib.request.Request(
        f"http://127.0.0.1:{server.server_port}{path}",
        data=body,
        method=method,
        headers=headers or {},
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _raw_receiver_request(server: http.server.HTTPServer, request: bytes) -> bytes:
    with socket.create_connection(("127.0.0.1", server.server_port), timeout=3) as connection:
        connection.sendall(request)
        connection.shutdown(socket.SHUT_WR)
        chunks = []
        while chunk := connection.recv(65536):
            chunks.append(chunk)
    return b"".join(chunks)


def test_receiver_accepts_valid_bundle_and_serves_only_one_record(tmp_path):
    inbox = tmp_path / "inbox"
    server = _start_receiver_server(inbox)
    bundle = _receiver_bundle()
    bundle_hash = bundle["bundle_hash"]
    body = json.dumps(bundle).encode()
    try:
        status, response = _receiver_request(
            server,
            "/api/upload",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json", "X-Bundle-Hash": bundle_hash},
        )
        assert status == 200
        assert json.loads(response)["bundle_hash"] == bundle_hash
        assert (inbox / f"{bundle_hash}.json").read_bytes() == body
        assert (inbox / f"{bundle_hash}.meta.json").is_file()

        status, response = _receiver_request(server, f"/api/bundle/{bundle_hash}")
        assert status == 200
        assert json.loads(response)["project"]["name"] == "receiver_test"

        status, response = _receiver_request(server, "/api/bundles")
        assert status == 200
        records = json.loads(response)["bundles"]
        assert len(records) == 1
        assert records[0]["bundle_hash"] == bundle_hash
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("bundle_hash", ["../escape", "a" * 63, "A" * 64, "g" * 64])
def test_receiver_rejects_malformed_bundle_hash_without_writing_outside(tmp_path, bundle_hash):
    inbox = tmp_path / "inbox"
    server = _start_receiver_server(inbox)
    bundle = _receiver_bundle()
    bundle["bundle_hash"] = bundle_hash
    try:
        status, _ = _receiver_request(
            server,
            "/api/upload",
            method="POST",
            body=json.dumps(bundle).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert status == 400
        assert not (tmp_path / "escape.json").exists()
        assert not (tmp_path / "escape.meta.json").exists()
        assert list(inbox.iterdir()) == []
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("path", ["/api/bundle/%2e%2e%2fescape", "/bundle/%2e%2e%2fescape"])
def test_receiver_encoded_traversal_cannot_read_outside_inbox(tmp_path, path):
    inbox = tmp_path / "inbox"
    outside = tmp_path / "escape.json"
    outside.write_text('{"secret":"must-not-leak"}', encoding="utf-8")
    server = _start_receiver_server(inbox)
    try:
        status, response = _receiver_request(server, path)
        assert status == 400
        assert b"must-not-leak" not in response
    finally:
        server.shutdown()
        server.server_close()


def test_receiver_rejects_symlink_escape_for_reads_and_writes(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("do not overwrite", encoding="utf-8")
    bundle = _receiver_bundle()
    bundle_hash = bundle["bundle_hash"]
    (inbox / f"{bundle_hash}.json").symlink_to(outside)
    server = _start_receiver_server(inbox)
    try:
        status, response = _receiver_request(server, f"/api/bundle/{bundle_hash}")
        assert status == 400
        assert b"do not overwrite" not in response

        status, _ = _receiver_request(
            server,
            "/api/upload",
            method="POST",
            body=json.dumps(bundle).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert status == 400
        assert outside.read_text(encoding="utf-8") == "do not overwrite"
    finally:
        server.shutdown()
        server.server_close()


def test_receiver_rejects_wrong_digest_content_type_and_oversized_body(tmp_path):
    server = _start_receiver_server(tmp_path / "inbox")
    bundle = _receiver_bundle()
    try:
        mismatched = {**bundle, "project": {"name": "tampered"}}
        status, _ = _receiver_request(
            server,
            "/api/upload",
            method="POST",
            body=json.dumps(mismatched).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert status == 422

        status, _ = _receiver_request(
            server,
            "/api/upload",
            method="POST",
            body=json.dumps(bundle).encode(),
            headers={"Content-Type": "text/plain"},
        )
        assert status == 415

        response = _raw_receiver_request(
            server,
            b"POST /api/upload HTTP/1.1\r\n"
            b"Host: 127.0.0.1\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: 52428801\r\n"
            b"Connection: close\r\n\r\n",
        )
        assert response.startswith(b"HTTP/1.0 413")
    finally:
        server.shutdown()
        server.server_close()


def test_receiver_handles_malformed_content_length(tmp_path):
    server = _start_receiver_server(tmp_path / "inbox")
    try:
        response = _raw_receiver_request(
            server,
            b"POST /api/upload HTTP/1.1\r\n"
            b"Host: 127.0.0.1\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: nope\r\n"
            b"Connection: close\r\n\r\n",
        )
        assert response.startswith(b"HTTP/1.0 400")
    finally:
        server.shutdown()
        server.server_close()


def test_receiver_is_loopback_only(tmp_path, monkeypatch):
    addresses = []

    class FakeServer:
        def __init__(self, address, _handler):
            addresses.append(address)

        def serve_forever(self):
            raise KeyboardInterrupt

        def server_close(self):
            pass

    monkeypatch.setattr(review_viewer, "_HardenedHTTPServer", FakeServer)
    review_viewer.serve_receiver(tmp_path / "default", port=7476, open_browser=False)
    review_viewer.serve_receiver(tmp_path / "second", port=7477, open_browser=False)

    assert addresses == [("127.0.0.1", 7476), ("127.0.0.1", 7477)]


def test_receiver_cli_defaults_to_loopback():
    from hw_codesign.cli import build_parser

    args = build_parser().parse_args(["serve-receiver", "--no-open"])

    assert not hasattr(args, "host")


def test_viewer_templates_escape_untrusted_values_before_inner_html():
    assert "${esc(b.project_name||'unknown')}" in _RECEIVER_HTML
    assert "${b.project_name||'unknown'}" not in _RECEIVER_HTML
    assert "${esc(p.name)}" in _DASHBOARD_HTML
    assert "${p.name}" not in _DASHBOARD_HTML
    assert "${esc(sm.pass||0)} pass" in _VIEWER_HTML
    assert "${esc(req.active_unresolved_count)}" in _VIEWER_HTML
    assert "${esc(pl.placement_count)}" in _VIEWER_HTML


def _start_comment_server(tmp_path: Path) -> tuple[http.server.HTTPServer, Path]:
    bundle_path = tmp_path / "bundle.json"
    comments_path = tmp_path / "comments.jsonl"
    bundle_path.write_text(json.dumps(_receiver_bundle()), encoding="utf-8")
    comments_path.touch()

    class Handler(_Handler):
        pass

    Handler.bundle_path = bundle_path
    Handler.comments_path = comments_path
    Handler.csrf_token = "test-csrf-token"
    Handler.comment_lock = threading.Lock()
    Handler.port = 0
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    Handler.port = server.server_port
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, comments_path


def _comment_post(server: http.server.HTTPServer, body: bytes, *, declared_length: int | None = None) -> bytes:
    length = len(body) if declared_length is None else declared_length
    return _raw_receiver_request(
        server,
        b"POST /api/comment HTTP/1.1\r\n"
        b"Host: 127.0.0.1\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        + f"Content-Length: {length}\r\n".encode()
        + b"Connection: close\r\n\r\n"
        + body,
    )


def test_comment_endpoint_requires_csrf_and_bounds_body(tmp_path):
    server, comments_path = _start_comment_server(tmp_path)
    try:
        forged = _comment_post(server, b"text=forged")
        assert forged.startswith(b"HTTP/1.0 403")
        assert comments_path.read_text(encoding="utf-8") == ""

        oversized = _comment_post(server, b"", declared_length=64 * 1024 + 1)
        assert oversized.startswith(b"HTTP/1.0 413")

        accepted = _comment_post(server, b"csrf_token=test-csrf-token&text=reviewed")
        assert accepted.startswith(b"HTTP/1.0 303")
        entry = json.loads(comments_path.read_text(encoding="utf-8"))
        assert entry["text"] == "reviewed"
        assert entry["bundle_hash"] == _receiver_bundle()["bundle_hash"]
    finally:
        server.shutdown()
        server.server_close()


def test_comment_form_response_has_security_headers_and_token(tmp_path):
    server, _ = _start_comment_server(tmp_path)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/comment", timeout=3) as response:
            body = response.read()
            assert response.headers["X-Content-Type-Options"] == "nosniff"
            assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
            assert b'test-csrf-token' in body
    finally:
        server.shutdown()
        server.server_close()
