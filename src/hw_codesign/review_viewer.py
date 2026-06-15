"""Local web viewer for the review bundle (stdlib only, no npm)."""
from __future__ import annotations

import http.server
import json
import threading
import urllib.parse
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .service import HardwareService


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
  return `<section><h2>Unresolved Requirements (${req.active_unresolved_count})</h2><table><thead><tr><th>ID</th><th>Source</th><th>Category</th><th>Flags</th></tr></thead><tbody>${rows}</tbody></table></section>`;
}

function renderAssumptions(asm){
  if(!asm||!asm.unresolved_critical) return '';
  const items=(asm.unresolved_critical_names||[]).map(n=>`<div class="unresolved">&#9888; Critical assumption unresolved: <strong>${esc(n)}</strong></div>`).join('');
  return `<section><h2>Critical Assumptions (${asm.unresolved_critical} unresolved)</h2>${items}</section>`;
}

function renderPlacement(pl){
  if(!pl) return '';
  const unenforced=(pl.unenforced_constraint_kinds||[]).map(esc).join(', ')||'none';
  const sources=Object.entries(pl.source_counts||{}).sort().map(([k,v])=>`${esc(k)}: ${v}`).join(', ');
  return `<section><h2>Placement Proposal</h2><table><tbody>
    <tr><th>Board</th><td>${esc(String(pl.board_width_mm))} &times; ${esc(String(pl.board_height_mm))} mm</td></tr>
    <tr><th>Placements</th><td>${pl.placement_count}</td></tr>
    <tr><th>Constraints</th><td>${pl.constraint_count}</td></tr>
    <tr><th>Unenforced</th><td class="warn">${unenforced}</td></tr>
    <tr><th>Sources</th><td>${sources}</td></tr>
  </tbody></table></section>`;
}

function renderComments(comments,hash){
  if(!comments||!comments.length) return '';
  let t=`<section><h2>Comments (${comments.length}) — <a href="/comment" style="color:#60a5fa;font-size:.8rem">Add comment</a></h2>`;
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
    <span class="chip ok">${sm.pass||0} pass</span>
    <span class="chip warn">${sm.blocked||0} blocked</span>
    <span class="chip" style="color:#ef4444">${sm.fail||0} fail</span>
    <span class="chip">${sm.total||0} total</span>
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
    const r=await fetch('/api/bundle');
    if(!r.ok){document.getElementById('status').textContent='Error: '+r.status;return;}
    const b=await r.json();
    document.getElementById('status').textContent='';
    document.getElementById('app').innerHTML=render(b);
  }catch(e){document.getElementById('status').textContent='Failed to load bundle: '+String(e);}
}
load();
setInterval(load,30000);
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

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        pass  # suppress access log

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/bundle":
            merged = _merge_bundle(self.bundle_path, self.comments_path)
            data = json.dumps(merged, sort_keys=True, indent=2).encode()
            self._respond(200, "application/json", data)
        elif parsed.path == "/comment":
            self._respond(200, "text/html", _COMMENTS_HTML.encode())
        else:
            self._respond(200, "text/html", _VIEWER_HTML.encode())

    def do_POST(self) -> None:  # noqa: N802
        if urllib.parse.urlparse(self.path).path != "/api/comment":
            self._respond(404, "text/plain", b"not found")
            return
        length = int(self.headers.get("Content-Length", 0))
        body = urllib.parse.parse_qs(self.rfile.read(length).decode())
        text = (body.get("text") or [""])[0].strip()
        target_type = (body.get("target_type") or ["general"])[0].strip() or "general"
        target_id = (body.get("target_id") or [""])[0].strip() or None
        author = (body.get("author") or [""])[0].strip() or None
        if not text:
            self._respond(400, "text/plain", b"text required")
            return
        from datetime import UTC, datetime
        import uuid
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
        with self.comments_path.open("a", encoding="utf-8") as fh:
            fh.write(entry + "\n")
        # bundle.json is intentionally NOT rewritten; _merge_bundle() merges at read time.
        self._respond(303, "text/plain", b"", headers={"Location": "/"})

    def _respond(self, code: int, ctype: str, body: bytes, headers: dict[str, str] | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
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

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
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
