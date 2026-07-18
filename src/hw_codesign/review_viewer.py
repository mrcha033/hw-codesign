"""Local web viewer for the review bundle (stdlib only, no npm)."""
from __future__ import annotations

import hashlib
import hmac
import http.server
import json
import os
import re
import secrets
import socket
import stat
import tempfile
import threading
import urllib.parse
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .service import HardwareService


_REQUEST_TIMEOUT_SECONDS = 10.0
_MAX_COMMENT_BYTES = 64 * 1024
_MAX_COMMENT_TEXT_CHARS = 16 * 1024
_MAX_COMMENT_FIELD_CHARS = 256


class _HardenedHTTPServer(http.server.ThreadingHTTPServer):
    """Threaded local server with bounded idle/read time per connection."""

    daemon_threads = True
    block_on_close = False

    def get_request(self) -> tuple[socket.socket, object]:
        request, client_address = super().get_request()
        request.settimeout(_REQUEST_TIMEOUT_SECONDS)
        return request, client_address


def _send_response_headers(
    handler: http.server.BaseHTTPRequestHandler,
    code: int,
    ctype: str,
    length: int,
    headers: dict[str, str] | None = None,
) -> None:
    handler.send_response(code)
    handler.send_header("Content-Type", ctype)
    handler.send_header("Content-Length", str(length))
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("Referrer-Policy", "no-referrer")
    handler.send_header("X-Frame-Options", "DENY")
    handler.send_header(
        "Content-Security-Policy",
        "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
        "connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
    )
    for key, value in (headers or {}).items():
        handler.send_header(key, value)
    handler.end_headers()


def _merge_bundle(bundle_path: Path, comments_path: Path) -> dict:
    """Return bundle with sidecar comments merged in. Never writes to bundle_path."""
    bundle = json.loads(bundle_path.read_bytes())
    comments = []
    if comments_path.is_file():
        for line in comments_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                comments.append(json.loads(line))
    return {**bundle, "comments": comments}


_VIEWER_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>hw-codesign Review Viewer</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;padding:1.5rem 2rem;background:#0f172a;color:#e2e8f0;}
h1{margin:0 0 .25rem;font-size:1.5rem;}
.meta{color:#94a3b8;font-size:.85rem;margin-bottom:1.5rem;}
.summary{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem;}
.chip{padding:.3rem .75rem;border-radius:999px;font-size:.8rem;font-weight:600;background:#1e293b;}
section{margin-bottom:1.75rem;}
h2{font-size:1rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em;margin:0 0 .6rem;}
table{border-collapse:collapse;width:100%;font-size:.85rem;}
th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid #1e293b;}
th{color:#94a3b8;font-weight:500;}
.badge{display:inline-block;padding:.1rem .5rem;border-radius:4px;font-size:.75rem;font-weight:700;color:#fff;}
details{background:#1e293b;border-radius:.4rem;margin-bottom:.4rem;}
summary{padding:.5rem .75rem;cursor:pointer;font-size:.85rem;}
pre{margin:0;padding:.5rem .75rem;font-size:.75rem;white-space:pre-wrap;color:#94a3b8;}
.warn{color:#fbbf24;} .ok{color:#4ade80;}
.unresolved{background:#7f1d1d;border-radius:.4rem;padding:.5rem .75rem;margin-bottom:.4rem;font-size:.85rem;}
#status{color:#94a3b8;font-size:.85rem;}
</style>
</head>
<body>
<h1>hw-codesign Review Viewer</h1>
<div id="status">Loading bundle from /api/bundle …</div>
<div id="app"></div>
<!--BUNDLE_DATA_INJECTION-->
<script>
const STATUS_COLOR={pass:"#22c55e",fail:"#ef4444",blocked:"#f97316",candidate:"#a855f7",released:"#3b82f6"};

function esc(s){
  return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function badge(s){return`<span class="badge" style="background:${STATUS_COLOR[esc(s)]||'#64748b'}">${esc(s)}</span>`;}

function renderGates(gr){
  let t=`<section><h2>Gate Reports</h2><table><thead><tr><th>Gate</th><th>Status</th><th>Findings</th></tr></thead><tbody>`;
  for(const r of gr){
    t+=`<tr><td>${esc(r.gate)}</td><td>${badge(r.status)}</td><td>${(r.failures||[]).length}</td></tr>`;
  }
  t+=`</tbody></table></section>`;
  const failing=gr.filter(r=>(r.failures||[]).length>0);
  if(failing.length){
    t+=`<section><h2>Findings</h2>`;
    for(const r of failing){
      const inner=(r.failures||[]).map(f=>`<pre>[${esc(f.severity||'error')}] ${esc(f.code)} — ${esc(f.message)}${f.path?`\\n  path: ${esc(f.path)}`:''}</pre>`).join('');
      t+=`<details><summary>${badge(r.status)} ${esc(r.gate)} (${(r.failures||[]).length})</summary>${inner}</details>`;
    }
    t+=`</section>`;
  }
  return t;
}

function renderRequirements(req){
  if(!req||!req.active_unresolved_count) return '';
  const rows=(req.active_unresolved||[]).map(r=>`<tr><td>${esc(r.id)}</td><td>${esc(r.source)}</td><td>${esc(r.category)}</td><td>${r.release_blocking?'&#9888; release-blocking':''}</td></tr>`).join('');
  return `<section><h2>Unresolved Requirements (${esc(req.active_unresolved_count)})</h2><table><thead><tr><th>ID</th><th>Source</th><th>Category</th><th>Flags</th></tr></thead><tbody>${rows}</tbody></table></section>`;
}

function renderAssumptions(asm){
  if(!asm||!asm.unresolved_critical) return '';
  const items=(asm.unresolved_critical_names||[]).map(n=>`<div class="unresolved">&#9888; Critical assumption unresolved: <strong>${esc(n)}</strong></div>`).join('');
  return `<section><h2>Critical Assumptions (${esc(asm.unresolved_critical)} unresolved)</h2>${items}</section>`;
}

function renderPlacement(pl){
  if(!pl) return '';
  const unenforced=(pl.unenforced_constraint_kinds||[]).map(esc).join(', ')||'none';
  const sources=Object.entries(pl.source_counts||{}).sort().map(([k,v])=>`${esc(k)}: ${esc(v)}`).join(', ');
  return `<section><h2>Placement Proposal</h2><table><tbody>
    <tr><th>Board</th><td>${esc(String(pl.board_width_mm))} &times; ${esc(String(pl.board_height_mm))} mm</td></tr>
    <tr><th>Placements</th><td>${esc(pl.placement_count)}</td></tr>
    <tr><th>Constraints</th><td>${esc(pl.constraint_count)}</td></tr>
    <tr><th>Unenforced</th><td class="warn">${unenforced}</td></tr>
    <tr><th>Sources</th><td>${sources}</td></tr>
  </tbody></table></section>`;
}

function renderComments(comments,hash){
  if(!comments||!comments.length) return '';
  const commentLink=window.__BUNDLE_DATA?'':' — <a href="/comment" style="color:#60a5fa;font-size:.8rem">Add comment</a>';
  let t=`<section><h2>Comments (${comments.length})${commentLink}</h2>`;
  for(const c of comments){
    const target=c.target_id?` [${esc(c.target_type||'general')}:${esc(c.target_id)}]`:(c.gate?` [gate:${esc(c.gate)}]`:'');
    t+=`<details open><summary>${esc(c.timestamp)}${target}${c.author?' — '+esc(c.author):''}</summary><pre>${esc(c.text)}</pre></details>`;
  }
  t+=`</section>`;
  return t;
}

function render(b){
  const p=b.project||{},sm=b.summary||{},gr=b.gate_reports||[];
  let html=`<h1>Review: ${esc(p.name)}</h1>`;
  html+=`<div class="meta">Rev ${esc(p.revision)} &bull; ${esc(p.backend)} &bull; ${esc(p.target_use)} &bull; ${esc(b.generated_at)} &bull; ${esc((b.bundle_hash||'').slice(0,12))}</div>`;
  html+=`<div class="summary">
    <span class="chip ok">${esc(sm.pass||0)} pass</span>
    <span class="chip warn">${esc(sm.blocked||0)} blocked</span>
    <span class="chip" style="color:#ef4444">${esc(sm.fail||0)} fail</span>
    <span class="chip">${esc(sm.total||0)} total</span>
  </div>`;
  html+=renderAssumptions(b.assumptions);
  html+=renderRequirements(b.requirements);
  html+=renderPlacement(b.placement);
  html+=renderGates(gr);
  html+=renderComments(b.comments,b.bundle_hash);
  return html;
}

async function load(){
  try{
    let b;
    if(window.__BUNDLE_DATA){b=window.__BUNDLE_DATA;}
    else{
      const r=await fetch('/api/bundle');
      if(!r.ok){document.getElementById('status').textContent='Error: '+r.status;return;}
      b=await r.json();
    }
    document.getElementById('status').textContent='';
    document.getElementById('app').innerHTML=render(b);
  }catch(e){document.getElementById('status').textContent='Failed to load bundle: '+String(e);}
}
load();
if(!window.__BUNDLE_DATA) setInterval(load,30000);
</script>
</body>
</html>
"""

_COMMENTS_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Add Comment</title>
<style>body{font-family:system-ui,sans-serif;margin:2rem;background:#0f172a;color:#e2e8f0;}
label{display:block;margin-bottom:.75rem;}
textarea{width:100%;height:8rem;background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:.4rem;padding:.5rem;font-family:inherit;}
input,select{background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:.4rem;padding:.4rem .6rem;width:100%;margin-top:.25rem;display:block;}
button{background:#3b82f6;color:#fff;border:none;padding:.5rem 1rem;border-radius:.4rem;cursor:pointer;margin-top:.5rem;}
</style></head>
<body>
<h2>Add Comment / Decision</h2>
<form method="post" action="/api/comment">
<input type="hidden" name="csrf_token" value="@@CSRF_TOKEN@@">
<label>Target type
  <select name="target_type">
    <option value="general">General</option>
    <option value="gate_failure">Gate failure</option>
    <option value="requirement">Requirement</option>
    <option value="component">Component</option>
  </select>
</label>
<label>Target ID (optional — e.g. gate:footprint_check or req_001)
  <input name="target_id" placeholder="leave blank for general">
</label>
<label>Author<input name="author" placeholder="optional"></label>
<label>Comment<textarea name="text" required></textarea></label>
<button type="submit">Add</button>
</form>
</body></html>
"""


class _Handler(http.server.BaseHTTPRequestHandler):
    bundle_path: Path
    comments_path: Path
    csrf_token: str
    comment_lock: threading.Lock
    port: int

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        pass  # suppress access log

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/bundle":
            merged = _merge_bundle(self.bundle_path, self.comments_path)
            data = json.dumps(merged, sort_keys=True, indent=2).encode()
            self._respond(200, "application/json", data)
        elif parsed.path == "/comment":
            html = _COMMENTS_HTML.replace("@@CSRF_TOKEN@@", self.csrf_token)
            self._respond(200, "text/html", html.encode())
        else:
            self._respond(200, "text/html", _VIEWER_HTML.encode())

    def do_POST(self) -> None:  # noqa: N802
        if urllib.parse.urlparse(self.path).path != "/api/comment":
            self._respond(404, "text/plain", b"not found")
            return
        transfer_encoding = self.headers.get("Transfer-Encoding")
        content_lengths = self.headers.get_all("Content-Length", failobj=[])
        if transfer_encoding or len(content_lengths) != 1:
            self._respond(411 if not transfer_encoding and not content_lengths else 400, "text/plain", b"one Content-Length header required")
            return
        try:
            length = int(content_lengths[0])
        except (TypeError, ValueError):
            self._respond(400, "text/plain", b"invalid Content-Length")
            return
        if length <= 0:
            self._respond(400, "text/plain", b"empty comment")
            return
        if length > _MAX_COMMENT_BYTES:
            self._respond(413, "text/plain", b"comment form too large")
            return
        media_type = self.headers.get("Content-Type", "").partition(";")[0].strip().lower()
        if media_type != "application/x-www-form-urlencoded":
            self._respond(415, "text/plain", b"Content-Type must be application/x-www-form-urlencoded")
            return
        try:
            raw_body = self.rfile.read(length)
        except (TimeoutError, OSError):
            self._respond(408, "text/plain", b"comment body timed out")
            return
        if len(raw_body) != length:
            self._respond(400, "text/plain", b"incomplete comment body")
            return
        try:
            body = urllib.parse.parse_qs(
                raw_body.decode("utf-8", errors="strict"),
                keep_blank_values=True,
                max_num_fields=16,
            )
        except (UnicodeDecodeError, ValueError):
            self._respond(400, "text/plain", b"invalid comment form")
            return
        supplied_token = (body.get("csrf_token") or [""])[0]
        if not isinstance(supplied_token, str) or not hmac.compare_digest(supplied_token, self.csrf_token):
            self._respond(403, "text/plain", b"invalid CSRF token")
            return
        text = (body.get("text") or [""])[0].strip()
        target_type = (body.get("target_type") or ["general"])[0].strip() or "general"
        target_id = (body.get("target_id") or [""])[0].strip() or None
        author = (body.get("author") or [""])[0].strip() or None
        if not text:
            self._respond(400, "text/plain", b"text required")
            return
        if target_type not in {"general", "gate_failure", "requirement", "component"}:
            self._respond(400, "text/plain", b"invalid target type")
            return
        if (
            len(text) > _MAX_COMMENT_TEXT_CHARS
            or (target_id is not None and len(target_id) > _MAX_COMMENT_FIELD_CHARS)
            or (author is not None and len(author) > _MAX_COMMENT_FIELD_CHARS)
        ):
            self._respond(413, "text/plain", b"comment field too large")
            return
        import uuid
        from datetime import UTC, datetime
        # Stamp with the bundle_hash so this comment is anchored to a specific evidence snapshot.
        bundle_hash = json.loads(self.bundle_path.read_bytes()).get("bundle_hash", "")
        entry = json.dumps({
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "target_type": target_type,
            "target_id": target_id,
            "author": author,
            "text": text,
            "bundle_hash": bundle_hash,
        }, sort_keys=True)
        with self.comment_lock:
            with self.comments_path.open("a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
        # bundle.json is intentionally NOT rewritten; _merge_bundle() merges at read time.
        self._respond(303, "text/plain", b"", headers={"Location": "/"})

    def _respond(self, code: int, ctype: str, body: bytes, headers: dict[str, str] | None = None) -> None:
        _send_response_headers(self, code, ctype, len(body), headers)
        if body:
            self.wfile.write(body)


def serve_review(service: "HardwareService", project: str, port: int = 7474, open_browser: bool = True) -> None:
    export_result = service.export_review(project)
    bundle_path = Path(export_result["file"])
    comments_path = bundle_path.parent / "comments.jsonl"
    comments_path.touch(exist_ok=True)

    class Handler(_Handler):
        pass

    Handler.bundle_path = bundle_path
    Handler.comments_path = comments_path
    Handler.csrf_token = secrets.token_urlsafe(32)
    Handler.comment_lock = threading.Lock()
    Handler.port = port

    server = _HardenedHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Review viewer: {url}")
    print(f"Bundle: {bundle_path}")
    print(f"Comments: {comments_path}")
    print("Press Ctrl-C to stop.")
    if open_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


# ---------------------------------------------------------------------------
# Standalone HTML export (no server required — data embedded in the file)
# ---------------------------------------------------------------------------

def build_standalone_html(bundle: dict, comments: list | None = None) -> str:
    """Return a self-contained HTML string with bundle data embedded as JS."""
    merged = {**bundle, "comments": comments or bundle.get("comments", [])}
    # Replace </ with <\/ to prevent the JSON from breaking the <script> tag.
    data_json = json.dumps(merged, separators=(",", ":")).replace("</", "<\\/")
    injection = f"<script>window.__BUNDLE_DATA={data_json};</script>"
    return _VIEWER_HTML.replace("<!--BUNDLE_DATA_INJECTION-->", injection)


# ---------------------------------------------------------------------------
# Multi-project dashboard server
# ---------------------------------------------------------------------------

_DASHBOARD_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>hw-codesign Dashboard</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;padding:1.5rem 2rem;background:#0f172a;color:#e2e8f0;}
h1{margin:0 0 .25rem;font-size:1.5rem;}
.meta{color:#94a3b8;font-size:.85rem;margin-bottom:1.5rem;}
table{border-collapse:collapse;width:100%;font-size:.85rem;}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid #1e293b;}
th{color:#94a3b8;font-weight:500;}
.chip{display:inline-block;padding:.15rem .5rem;border-radius:999px;font-size:.75rem;font-weight:600;background:#1e293b;margin-right:.25rem;}
a{color:#60a5fa;text-decoration:none;}a:hover{text-decoration:underline;}
.muted{color:#64748b;}
</style>
</head>
<body>
<h1>hw-codesign Dashboard</h1>
<div id="status" class="meta">Loading projects…</div>
<table id="tbl" style="display:none">
<thead><tr><th>Project</th><th>Gate status</th><th>Last export</th><th></th></tr></thead>
<tbody id="tbody"></tbody>
</table>
<script>
const SC={pass:"#22c55e",fail:"#ef4444",blocked:"#f97316"};
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function chip(s,n){return n?`<span class="chip" style="color:${SC[s]||'#94a3b8'}">${esc(n)} ${esc(s)}</span>`:''}
function row(p){
  const chips=chip('pass',p.pass)+chip('fail',p.fail)+chip('blocked',p.blocked);
  const when=p.generated_at?(new Date(p.generated_at)).toLocaleString():'—';
  const link=p.has_bundle?`<a href="/project/${encodeURIComponent(p.name)}">View</a>`:'<span class="muted">no bundle</span>';
  return `<tr><td><strong>${esc(p.name)}</strong></td><td>${chips||'<span class="muted">—</span>'}</td><td class="muted">${esc(when)}</td><td>${link}</td></tr>`;
}
async function load(){
  try{
    const r=await fetch('/api/projects');
    if(!r.ok){document.getElementById('status').textContent='Error: '+r.status;return;}
    const d=await r.json();
    const projects=d.projects||[];
    document.getElementById('status').textContent=`${projects.length} project${projects.length===1?'':'s'}`;
    document.getElementById('tbody').innerHTML=projects.map(row).join('');
    document.getElementById('tbl').style.display='';
  }catch(e){document.getElementById('status').textContent='Failed: '+String(e);}
}
load();
setInterval(load,30000);
</script>
</body>
</html>
"""

_RECEIVER_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>hw-codesign Review Receiver</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;padding:1.5rem 2rem;background:#0f172a;color:#e2e8f0;}
h1{margin:0 0 .25rem;font-size:1.5rem;}
.meta{color:#94a3b8;font-size:.85rem;margin-bottom:1.5rem;}
table{border-collapse:collapse;width:100%;font-size:.85rem;}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid #1e293b;}
th{color:#94a3b8;font-weight:500;}
a{color:#60a5fa;text-decoration:none;}a:hover{text-decoration:underline;}
.muted{color:#64748b;}
code{background:#1e293b;padding:.1rem .35rem;border-radius:.25rem;font-size:.8rem;}
</style>
</head>
<body>
<h1>hw-codesign Review Receiver</h1>
<div class="meta">Upload: <code>hw upload-review &lt;project&gt; --destination http://&lt;host&gt;:{PORT}/api/upload</code></div>
<div id="status" class="meta">Loading…</div>
<table id="tbl" style="display:none">
<thead><tr><th>Project</th><th>Hash</th><th>Received</th><th></th></tr></thead>
<tbody id="tbody"></tbody>
</table>
<script>
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function row(b){
  const when=(new Date(b.received_at)).toLocaleString();
  return `<tr><td><strong>${esc(b.project_name||'unknown')}</strong></td><td class="muted">${esc((b.bundle_hash||'').slice(0,12))}</td><td class="muted">${esc(when)}</td><td><a href="/bundle/${encodeURIComponent(b.bundle_hash)}">View</a></td></tr>`;
}
async function load(){
  try{
    const r=await fetch('/api/bundles');
    if(!r.ok){document.getElementById('status').textContent='Error: '+r.status;return;}
    const d=await r.json();
    const bundles=d.bundles||[];
    document.getElementById('status').textContent=`${bundles.length} bundle${bundles.length===1?'':'s'} received`;
    document.getElementById('tbody').innerHTML=bundles.map(row).join('');
    document.getElementById('tbl').style.display='';
  }catch(e){document.getElementById('status').textContent='Failed: '+String(e);}
}
load();
setInterval(load,10000);
</script>
</body>
</html>
"""


class _DashboardHandler(http.server.BaseHTTPRequestHandler):
    service: "HardwareService"

    def log_message(self, fmt: str, *args: object) -> None:
        pass

    def do_GET(self) -> None:  # noqa: N802
        parts = [p for p in urllib.parse.urlparse(self.path).path.split("/") if p]

        if not parts:
            self._respond(200, "text/html", _DASHBOARD_HTML.encode())
        elif parts == ["api", "projects"]:
            data = json.dumps(self.service.list_project_summaries(), sort_keys=True, indent=2).encode()
            self._respond(200, "application/json", data)
        elif len(parts) >= 2 and parts[0] == "project":
            name = parts[1]
            if len(parts) >= 4 and parts[2:4] == ["api", "bundle"]:
                # Serve the raw bundle JSON for this project
                try:
                    result = self.service.export_review(name)
                    bundle_path = Path(result["file"])
                    comments_path = bundle_path.parent / "comments.jsonl"
                    merged = _merge_bundle(bundle_path, comments_path)
                    data = json.dumps(merged, sort_keys=True, indent=2).encode()
                    self._respond(200, "application/json", data)
                except Exception as exc:
                    self._respond(404, "application/json", json.dumps({"error": str(exc)}).encode())
            else:
                # Serve the viewer with embedded bundle data
                try:
                    result = self.service.export_review(name)
                    bundle_path = Path(result["file"])
                    comments_path = bundle_path.parent / "comments.jsonl"
                    merged = _merge_bundle(bundle_path, comments_path)
                    html = build_standalone_html(merged)
                    self._respond(200, "text/html", html.encode())
                except Exception as exc:
                    self._respond(404, "text/plain", str(exc).encode())
        else:
            self._respond(404, "text/plain", b"not found")

    def _respond(self, code: int, ctype: str, body: bytes) -> None:
        _send_response_headers(self, code, ctype, len(body))
        if body:
            self.wfile.write(body)


def serve_dashboard(service: "HardwareService", port: int = 7475, open_browser: bool = True) -> None:
    class Handler(_DashboardHandler):
        pass

    Handler.service = service

    server = _HardenedHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Dashboard: {url}")
    print("Press Ctrl-C to stop.")
    if open_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


# ---------------------------------------------------------------------------
# Bundle receiver server (accepts uploaded bundles via HTTP POST)
# ---------------------------------------------------------------------------

_BUNDLE_HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
_MAX_BUNDLE_BYTES = 50 * 1024 * 1024
_MAX_META_BYTES = 256 * 1024
_MAX_SUMMARY_BYTES = 64 * 1024
_MAX_PROJECT_NAME_CHARS = 256


def _is_bundle_hash(value: object) -> bool:
    return isinstance(value, str) and _BUNDLE_HASH_RE.fullmatch(value) is not None


def _receiver_path_parts(target: str) -> tuple[str, ...]:
    """Decode a request path without accepting ambiguous or encoded separators."""
    try:
        raw_path = urllib.parse.urlsplit(target).path
    except ValueError as exc:
        raise ValueError("malformed request path") from exc
    if raw_path == "/":
        return ()
    if not raw_path.startswith("/") or raw_path.endswith("/"):
        raise ValueError("malformed request path")

    raw_parts = raw_path[1:].split("/")
    if any(not part for part in raw_parts):
        raise ValueError("malformed request path")

    parts: list[str] = []
    for raw_part in raw_parts:
        if re.search(r"%(?![0-9A-Fa-f]{2})", raw_part):
            raise ValueError("malformed percent escape")
        try:
            part = urllib.parse.unquote(raw_part, encoding="utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ValueError("request path is not valid UTF-8") from exc
        if (
            part in {".", ".."}
            or "/" in part
            or "\\" in part
            or any(ord(char) < 0x20 or ord(char) == 0x7F for char in part)
        ):
            raise ValueError("malformed request path segment")
        parts.append(part)
    return tuple(parts)


def _inbox_root(inbox_dir: Path) -> Path:
    root = Path(inbox_dir).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("receiver inbox is not a directory")
    return root


def _safe_inbox_member(inbox_dir: Path, filename: str) -> Path:
    """Resolve one direct inbox member and reject symlink/path escapes."""
    if not filename or Path(filename).name != filename or "/" in filename or "\\" in filename:
        raise ValueError("invalid inbox filename")
    root = _inbox_root(inbox_dir)
    target = root / filename
    if target.is_symlink():
        raise ValueError("inbox member cannot be a symlink")
    return target


def _read_inbox_member(inbox_dir: Path, filename: str, *, max_bytes: int) -> bytes:
    root = _inbox_root(inbox_dir)
    _safe_inbox_member(root, filename)
    fd: int | None = None
    if os.open in os.supports_dir_fd and hasattr(os, "O_NOFOLLOW"):
        root_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        root_fd = os.open(root, root_flags)
        try:
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=root_fd)
        finally:
            os.close(root_fd)
    else:
        path = _safe_inbox_member(root, filename)
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0))
        if path.is_symlink():
            os.close(fd)
            raise ValueError("inbox member cannot be a symlink")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("inbox member is not a regular file")
        with os.fdopen(fd, "rb") as fh:
            fd = None
            data = fh.read(max_bytes + 1)
    finally:
        if fd is not None:
            os.close(fd)
    if len(data) > max_bytes:
        raise ValueError("stored receiver file exceeds size limit")
    return data


def _atomic_write_inbox_member(inbox_dir: Path, filename: str, data: bytes) -> None:
    root = _inbox_root(inbox_dir)
    # Validate the currently resolved destination as well as the lexical filename.
    # os.replace then replaces a racing symlink rather than following it.
    _safe_inbox_member(root, filename)
    target = root / filename
    fd, temporary_name = tempfile.mkstemp(prefix=".review-upload-", suffix=".tmp", dir=root)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(temporary_name, target)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def _strict_json_loads(data: bytes) -> object:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number: {value}")

    return json.loads(data, object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant)


def _canonical_bundle_hash(bundle: dict[str, object]) -> str:
    canonical = {key: value for key, value in bundle.items() if key not in {"bundle_hash", "generated_at"}}
    canonical_bytes = json.dumps(canonical, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(canonical_bytes).hexdigest()


class _ReceiverHandler(http.server.BaseHTTPRequestHandler):
    inbox_dir: Path
    port: int

    def log_message(self, fmt: str, *args: object) -> None:
        pass

    def do_GET(self) -> None:  # noqa: N802
        try:
            parts = _receiver_path_parts(self.path)
        except ValueError:
            self._respond(400, "text/plain", b"malformed request path")
            return

        if not parts:
            html = _RECEIVER_HTML.replace("{PORT}", str(self.port))
            self._respond(200, "text/html", html.encode())
        elif parts == ("api", "bundles"):
            records: list[tuple[float, dict[str, object]]] = []
            for candidate in self.inbox_dir.glob("*.json"):
                if candidate.name.endswith(".meta.json"):
                    continue
                bundle_hash = candidate.name.removesuffix(".json")
                if not _is_bundle_hash(bundle_hash):
                    continue
                try:
                    bundle_path = _safe_inbox_member(self.inbox_dir, candidate.name)
                    meta_data = _read_inbox_member(
                        self.inbox_dir,
                        f"{bundle_hash}.meta.json",
                        max_bytes=_MAX_META_BYTES,
                    )
                    meta = _strict_json_loads(meta_data)
                    if not isinstance(meta, dict) or meta.get("bundle_hash") != bundle_hash:
                        continue
                    records.append((bundle_path.stat().st_mtime, meta))
                except Exception:
                    pass
            bundles = [meta for _, meta in sorted(records, key=lambda record: record[0], reverse=True)]
            self._respond(200, "application/json", json.dumps({"bundles": bundles}, sort_keys=True, indent=2).encode())
        elif len(parts) == 3 and parts[:2] == ("api", "bundle"):
            bundle_hash = parts[2]
            if not _is_bundle_hash(bundle_hash):
                self._respond(400, "text/plain", b"invalid bundle hash")
                return
            try:
                data = _read_inbox_member(self.inbox_dir, f"{bundle_hash}.json", max_bytes=_MAX_BUNDLE_BYTES)
            except (FileNotFoundError, IsADirectoryError):
                self._respond(404, "text/plain", b"bundle not found")
            except ValueError:
                self._respond(400, "text/plain", b"invalid bundle path")
            except OSError:
                self._respond(500, "text/plain", b"unable to read bundle")
            else:
                self._respond(200, "application/json", data)
        elif len(parts) == 2 and parts[0] == "bundle":
            bundle_hash = parts[1]
            if not _is_bundle_hash(bundle_hash):
                self._respond(400, "text/plain", b"invalid bundle hash")
                return
            try:
                bundle_data = _read_inbox_member(self.inbox_dir, f"{bundle_hash}.json", max_bytes=_MAX_BUNDLE_BYTES)
                bundle = _strict_json_loads(bundle_data)
                if not isinstance(bundle, dict):
                    raise ValueError("stored bundle is not a JSON object")
                html = build_standalone_html(bundle)
            except (FileNotFoundError, IsADirectoryError):
                self._respond(404, "text/plain", b"bundle not found")
            except ValueError:
                self._respond(400, "text/plain", b"invalid bundle path or content")
            except OSError:
                self._respond(500, "text/plain", b"unable to read bundle")
            else:
                self._respond(200, "text/html", html.encode())
        else:
            self._respond(404, "text/plain", b"not found")

    def do_POST(self) -> None:  # noqa: N802
        try:
            parts = _receiver_path_parts(self.path)
        except ValueError:
            self._respond(400, "text/plain", b"malformed request path")
            return
        if parts != ("api", "upload"):
            self._respond(404, "text/plain", b"not found")
            return

        transfer_encoding = self.headers.get("Transfer-Encoding")
        content_lengths = self.headers.get_all("Content-Length", failobj=[])
        if transfer_encoding or len(content_lengths) != 1:
            self._respond(411 if not transfer_encoding and not content_lengths else 400, "text/plain", b"one Content-Length header required")
            return
        try:
            length = int(content_lengths[0])
        except (TypeError, ValueError):
            self._respond(400, "text/plain", b"invalid Content-Length")
            return
        if length <= 0:
            self._respond(400, "text/plain", b"empty bundle")
            return
        if length > _MAX_BUNDLE_BYTES:
            self._respond(413, "text/plain", b"bundle too large (>50 MB)")
            return

        media_type = self.headers.get("Content-Type", "").partition(";")[0].strip().lower()
        if media_type != "application/json" and not (media_type.startswith("application/") and media_type.endswith("+json")):
            self._respond(415, "text/plain", b"Content-Type must be application/json")
            return

        try:
            body = self.rfile.read(length)
        except (TimeoutError, OSError):
            self._respond(408, "text/plain", b"bundle body timed out")
            return
        if len(body) != length:
            self._respond(400, "text/plain", b"incomplete request body")
            return
        try:
            bundle = _strict_json_loads(body)
            if not isinstance(bundle, dict):
                raise ValueError("bundle must be a JSON object")
            bundle_hash = bundle.get("bundle_hash", "")
            if not _is_bundle_hash(bundle_hash):
                raise ValueError("bundle_hash must be a lowercase SHA-256 digest")
            expected_hash = _canonical_bundle_hash(bundle)
            if not hmac.compare_digest(bundle_hash, expected_hash):
                self._respond(422, "text/plain", b"bundle_hash does not match bundle content")
                return

            header_hash = self.headers.get("X-Bundle-Hash")
            if header_hash is not None and (
                not _is_bundle_hash(header_hash) or not hmac.compare_digest(header_hash, bundle_hash)
            ):
                self._respond(400, "text/plain", b"X-Bundle-Hash does not match bundle_hash")
                return

            project = bundle.get("project", {})
            summary = bundle.get("summary", {})
            if not isinstance(project, dict) or not isinstance(summary, dict):
                raise ValueError("project and summary must be JSON objects")
            project_name = project.get("name", "unknown")
            if (
                not isinstance(project_name, str)
                or len(project_name) > _MAX_PROJECT_NAME_CHARS
                or any(ord(char) < 0x20 or ord(char) == 0x7F for char in project_name)
            ):
                raise ValueError("invalid project name")
            summary_bytes = json.dumps(summary, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
            if len(summary_bytes) > _MAX_SUMMARY_BYTES:
                raise ValueError("summary exceeds size limit")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError):
            self._respond(400, "text/plain", b"invalid JSON")
            return

        from datetime import UTC, datetime
        meta = {
            "bundle_hash": bundle_hash,
            "project_name": project_name,
            "received_at": datetime.now(UTC).isoformat(),
            "summary": summary,
        }
        meta_bytes = json.dumps(meta, sort_keys=True, separators=(",", ":")).encode()
        try:
            _atomic_write_inbox_member(self.inbox_dir, f"{bundle_hash}.json", body)
            _atomic_write_inbox_member(self.inbox_dir, f"{bundle_hash}.meta.json", meta_bytes)
        except ValueError:
            self._respond(400, "text/plain", b"invalid bundle destination")
            return
        except OSError:
            self._respond(500, "text/plain", b"unable to store bundle")
            return
        print(f"Received bundle {bundle_hash[:12]} for project {meta['project_name']!r}")
        self._respond(200, "application/json", json.dumps({"status": "received", "bundle_hash": bundle_hash}).encode())

    def _respond(self, code: int, ctype: str, body: bytes) -> None:
        _send_response_headers(self, code, ctype, len(body))
        if body:
            self.wfile.write(body)


def serve_receiver(inbox_dir: Path, port: int = 7476, open_browser: bool = True) -> None:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    inbox_dir = inbox_dir.resolve(strict=True)
    class Handler(_ReceiverHandler):
        pass

    Handler.inbox_dir = inbox_dir
    Handler.port = port

    server = _HardenedHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Receiver: {url}")
    print(f"Listening: 127.0.0.1:{port} (loopback only)")
    print(f"Inbox: {inbox_dir}")
    print(f"Upload: hw upload-review <project> --destination http://<host>:{port}/api/upload")
    print("Press Ctrl-C to stop.")
    if open_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
