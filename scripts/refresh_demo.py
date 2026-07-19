#!/usr/bin/env python3
"""Refresh the checked-in golden-board demo from one persisted evidence snapshot.

This script deliberately does not generate a board or run validation.  It only
accepts an already-exported review bundle when that bundle is an exact portable
copy of the current gate-report set.  That fail-closed boundary prevents stale
or selectively copied results from becoming product-demo claims.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT = "golden_rp2040_usb_hid"
EXPECTED_SUMMARY = {"total": 48, "pass": 44, "fail": 1, "blocked": 3, "other": 0}
EXPECTED_FAILS = frozenset({"sourcing"})
EXPECTED_BLOCKED = frozenset({"supplier_availability", "native_zephyr_build", "physical_qualification"})

ROOT_EVIDENCE_START = "<!-- golden-demo-evidence:start -->"
ROOT_EVIDENCE_END = "<!-- golden-demo-evidence:end -->"


class RefreshError(RuntimeError):
    """Raised when a persisted snapshot cannot safely support the demo claims."""


@dataclass(frozen=True)
class Snapshot:
    bundle: dict[str, Any]
    bundle_hash: str
    bundle_file_sha256: str
    generated_at: str
    reports: dict[str, dict[str, Any]]
    board_sha256: str
    routing: dict[str, Any]


@dataclass(frozen=True)
class Toolchain:
    rsvg_convert: str
    rsvg_version: str
    ffmpeg: str
    ffmpeg_version: str
    ffprobe: str


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RefreshError(f"Cannot read JSON evidence {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RefreshError(f"Expected a JSON object in {path}")
    return value


def _portable_string(value: str, repo_root: Path) -> str:
    root_text = repo_root.resolve().as_posix()
    normalized = value.replace("\\", "/")
    if normalized == root_text:
        return "."
    if normalized.startswith(f"{root_text}/"):
        return normalized[len(root_text) + 1 :]
    if root_text in normalized:
        return normalized.replace(root_text, ".")
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return f"<host-path>/{normalized.split('/')[-1]}"
    if re.match(r"^/(?:[^/\s]+/)*[^/\s]*$", value):
        return f"<host-path>/{Path(value).name}"
    return value


def _portable_value(value: Any, repo_root: Path) -> Any:
    if isinstance(value, dict):
        return {key: _portable_value(item, repo_root) for key, item in value.items()}
    if isinstance(value, list):
        return [_portable_value(item, repo_root) for item in value]
    if isinstance(value, str):
        return _portable_string(value, repo_root)
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise RefreshError(f"{label}: expected {expected!r}, found {actual!r}")


def _validate_bundle_claims(bundle: dict[str, Any], standalone_text: str, *, label: str) -> str:
    """Validate the release-facing claims encoded in a portable review bundle."""

    _require_equal(bundle.get("summary"), EXPECTED_SUMMARY, f"{label} summary")
    bundle_reports = bundle.get("gate_reports")
    if not isinstance(bundle_reports, list):
        raise RefreshError(f"{label} has no gate_reports list")

    reports: dict[str, dict[str, Any]] = {}
    for report in bundle_reports:
        if not isinstance(report, dict):
            raise RefreshError(f"{label} contains a non-object gate report")
        gate = report.get("gate")
        if not isinstance(gate, str) or not gate:
            raise RefreshError(f"{label} contains a gate report without a name")
        if gate in reports:
            raise RefreshError(f"{label} contains duplicate gate report {gate!r}")
        reports[gate] = report

    statuses = {gate: report.get("status") for gate, report in reports.items()}
    summary = {
        "total": len(reports),
        "pass": sum(status == "pass" for status in statuses.values()),
        "fail": sum(status == "fail" for status in statuses.values()),
        "blocked": sum(status == "blocked" for status in statuses.values()),
        "other": sum(status not in {"pass", "fail", "blocked"} for status in statuses.values()),
    }
    _require_equal(summary, EXPECTED_SUMMARY, f"{label} gate-report summary")
    _require_equal(
        frozenset(gate for gate, status in statuses.items() if status == "fail"),
        EXPECTED_FAILS,
        f"{label} failed gate set",
    )
    _require_equal(
        frozenset(gate for gate, status in statuses.items() if status == "blocked"),
        EXPECTED_BLOCKED,
        f"{label} blocked gate set",
    )

    canonical_bundle = {key: value for key, value in bundle.items() if key not in {"bundle_hash", "generated_at"}}
    expected_bundle_hash = _sha256_bytes(_canonical_json(canonical_bundle))
    _require_equal(bundle.get("bundle_hash"), expected_bundle_hash, f"{label} canonical hash")
    if expected_bundle_hash not in standalone_text:
        raise RefreshError(f"{label} standalone review does not embed its canonical bundle hash")

    for gate in ("autoroute", "native_erc", "native_drc", "native_zephyr_build", "physical_qualification"):
        if gate not in reports:
            raise RefreshError(f"{label} is missing required gate report {gate!r}")
    autoroute_metrics = reports["autoroute"].get("metrics", {})
    _require_equal(autoroute_metrics.get("freerouting_unrouted"), 0, f"{label} raw unrouted count")
    _require_equal(autoroute_metrics.get("unrouted"), 0, f"{label} post-fill unconnected count")
    _require_equal(reports["native_erc"].get("metrics", {}).get("violations"), 0, f"{label} native ERC violations")
    _require_equal(reports["native_drc"].get("metrics", {}).get("violations"), 0, f"{label} native DRC violations")
    zephyr_report = reports["native_zephyr_build"]
    zephyr_stdout = zephyr_report.get("backend", {}).get("stdout", "")
    if zephyr_report.get("status") == "pass":
        if "[170/170]" not in zephyr_stdout:
            raise RefreshError(f"{label} native Zephyr report does not contain the persisted 170/170 completion")
    elif zephyr_report.get("status") == "blocked":
        failure_codes = {
            failure.get("code")
            for failure in zephyr_report.get("failures", [])
            if isinstance(failure, dict)
        }
        if "arm_newlib_unavailable" not in failure_codes:
            raise RefreshError(f"{label} blocked native Zephyr report lacks arm_newlib_unavailable evidence")
    else:
        raise RefreshError(f"{label} native Zephyr report has unsupported status {zephyr_report.get('status')!r}")
    physical_report = reports["physical_qualification"]
    physical_metrics = physical_report.get("metrics", {})
    _require_equal(physical_metrics.get("required_tests"), 9, f"{label} physical required test count")
    _require_equal(physical_metrics.get("missing_or_unapproved"), 9, f"{label} physical missing or unapproved count")
    via_failures = [
        failure
        for failure in physical_report.get("failures", [])
        if isinstance(failure, dict) and "via_in_pad_process_qualification" in json.dumps(failure, sort_keys=True)
    ]
    if len(via_failures) != 1:
        raise RefreshError(f"{label} must contain one via-in-pad process qualification blocker")
    return expected_bundle_hash


def _embedded_bundle(standalone_text: str, *, label: str) -> dict[str, Any]:
    match = re.search(r"<script>window\.__BUNDLE_DATA=(.*?);</script>", standalone_text, flags=re.DOTALL)
    if not match:
        raise RefreshError(f"{label} does not contain embedded review bundle data")
    try:
        embedded = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise RefreshError(f"{label} contains invalid embedded review bundle JSON: {exc}") from exc
    if not isinstance(embedded, dict):
        raise RefreshError(f"{label} embedded review bundle is not an object")
    return embedded


def _validate_standalone_3d(bundle: dict[str, Any], standalone_text: str, *, label: str) -> None:
    preview = bundle.get("three_d_preview")
    if not isinstance(preview, dict):
        raise RefreshError(f"{label} has no three_d_preview object")
    _require_equal(preview.get("status"), "available", f"{label} 3D preview status")
    _require_equal(preview.get("interactive"), True, f"{label} interactive 3D preview")
    _require_equal(preview.get("model_count"), 31, f"{label} declared 3D model count")
    _require_equal(preview.get("available_model_count"), 31, f"{label} available 3D model count")
    for marker in (
        "3D Assembly Preview",
        'id="hw-review-3d"',
        'id="hw-review-vrml"',
        "31 of 31 referenced models available",
        "data:image/png;base64,",
        "window.HWReview3D.mount",
    ):
        if marker not in standalone_text:
            raise RefreshError(f"{label} is missing self-contained 3D marker: {marker}")
    if '<script src="assets/three_d/' in standalone_text:
        raise RefreshError(f"{label} depends on an external 3D viewer script")


def _verify_release_evidence(repo_root: Path) -> tuple[str, str]:
    """Verify only checked-in evidence, without native tools or demo renderers."""

    demo_dir = repo_root / "docs" / "demo"
    bundle_path = demo_dir / "bundle.json"
    standalone_path = demo_dir / "index.html"
    readme_path = demo_dir / "README.md"
    required = (bundle_path, standalone_path, readme_path)
    missing = [str(path.relative_to(repo_root)) for path in required if not path.is_file()]
    if missing:
        raise RefreshError("Missing checked-in release evidence: " + ", ".join(missing))

    bundle = _read_json(bundle_path)
    standalone_text = standalone_path.read_text(encoding="utf-8")
    bundle_hash = _validate_bundle_claims(bundle, standalone_text, label="checked-in full-toolchain bundle")
    embedded = _embedded_bundle(standalone_text, label="checked-in standalone review")
    if _canonical_json(embedded) != _canonical_json(bundle):
        raise RefreshError("Checked-in standalone review does not embed docs/demo/bundle.json exactly")
    _validate_standalone_3d(bundle, standalone_text, label="checked-in standalone review")

    bundle_file_sha256 = _sha256_file(bundle_path)
    readme_text = readme_path.read_text(encoding="utf-8")
    if f"{bundle_file_sha256}  bundle.json" not in readme_text:
        raise RefreshError("Demo README does not record the checked-in bundle.json SHA-256")

    source_bundle = repo_root / "projects" / PROJECT / "exports" / "working" / "review" / "bundle.json"
    if source_bundle.is_file() and source_bundle.read_bytes() != bundle_path.read_bytes():
        raise RefreshError("Checked-in release bundle differs from the locally audited full-toolchain bundle")
    return bundle_hash, bundle_file_sha256


def _load_snapshot(repo_root: Path) -> Snapshot:
    project = repo_root / "projects" / PROJECT
    reports_dir = project / "validation" / "reports"
    review_dir = project / "exports" / "working" / "review"
    bundle_path = review_dir / "bundle.json"
    standalone_path = review_dir / "review_standalone.html"
    board_path = project / "electronics" / "generated" / "kicad" / f"{PROJECT}.kicad_pcb"
    routing_path = project / "electronics" / "generated" / "kicad" / "routing.json"
    physical_plan_path = project / "validation" / "physical" / "qualification_plan.md"
    physical_plan_json_path = project / "validation" / "physical" / "qualification_plan.json"

    required = (
        bundle_path,
        standalone_path,
        board_path,
        routing_path,
        physical_plan_path,
        physical_plan_json_path,
    )
    missing = [str(path.relative_to(repo_root)) for path in required if not path.is_file()]
    if missing:
        raise RefreshError("Missing persisted demo inputs: " + ", ".join(missing))

    reports: dict[str, dict[str, Any]] = {}
    for path in sorted(reports_dir.glob("*.json")):
        report = _read_json(path)
        if "gate" not in report or "status" not in report:
            continue
        gate = report["gate"]
        if not isinstance(gate, str) or not gate:
            raise RefreshError(f"Invalid gate name in {path}")
        if gate in reports:
            raise RefreshError(f"Duplicate persisted gate report: {gate}")
        reports[gate] = report

    statuses = {gate: report.get("status") for gate, report in reports.items()}
    summary = {
        "total": len(reports),
        "pass": sum(status == "pass" for status in statuses.values()),
        "fail": sum(status == "fail" for status in statuses.values()),
        "blocked": sum(status == "blocked" for status in statuses.values()),
        "other": sum(status not in {"pass", "fail", "blocked"} for status in statuses.values()),
    }
    _require_equal(summary, EXPECTED_SUMMARY, "persisted report summary")
    _require_equal(
        frozenset(gate for gate, status in statuses.items() if status == "fail"),
        EXPECTED_FAILS,
        "failed gate set",
    )
    _require_equal(
        frozenset(gate for gate, status in statuses.items() if status == "blocked"),
        EXPECTED_BLOCKED,
        "blocked gate set",
    )

    bundle = _read_json(bundle_path)
    _require_equal(bundle.get("summary"), EXPECTED_SUMMARY, "review bundle summary")
    bundle_reports = bundle.get("gate_reports")
    if not isinstance(bundle_reports, list):
        raise RefreshError("Review bundle has no gate_reports list")
    expected_reports = [_portable_value(reports[gate], repo_root) for gate in sorted(reports)]
    if _canonical_json(bundle_reports) != _canonical_json(expected_reports):
        raise RefreshError(
            "Review bundle gate reports do not exactly match validation/reports. "
            f"Run `hw --root . export-standalone-review {PROJECT}` first."
        )

    standalone_text = standalone_path.read_text(encoding="utf-8")
    expected_bundle_hash = _validate_bundle_claims(bundle, standalone_text, label="audited full-toolchain bundle")
    if _canonical_json(_embedded_bundle(standalone_text, label="audited standalone review")) != _canonical_json(bundle):
        raise RefreshError("Standalone review does not embed the audited full-toolchain bundle exactly")
    _validate_standalone_3d(bundle, standalone_text, label="audited standalone review")
    for artifact in bundle.get("artifacts", []):
        if not isinstance(artifact, dict) or not artifact.get("exists"):
            continue
        relative = artifact.get("path")
        if not isinstance(relative, str):
            raise RefreshError("Review bundle contains an existing artifact without a path")
        artifact_path = (repo_root / relative).resolve()
        if not artifact_path.is_relative_to(repo_root) or not artifact_path.is_file():
            raise RefreshError(f"Review bundle artifact is missing or outside the repository: {relative}")
        _require_equal(artifact.get("bytes"), artifact_path.stat().st_size, f"artifact size for {relative}")
        _require_equal(artifact.get("sha256"), _sha256_file(artifact_path), f"artifact SHA-256 for {relative}")

    routing = _read_json(routing_path)
    for key, expected in {
        "status": "pass",
        "signal_routing": "complete",
        "zone_fill": "persisted",
        "freerouting_unrouted": 0,
        "post_import_unconnected": 0,
        "violations": 0,
    }.items():
        _require_equal(routing.get(key), expected, f"routing.{key}")

    board_sha256 = _sha256_file(board_path)
    _require_equal(routing.get("board_sha256"), board_sha256, "routing board SHA-256")
    _require_equal(reports["native_erc"].get("metrics", {}).get("violations"), 0, "native ERC violations")
    _require_equal(reports["native_drc"].get("metrics", {}).get("violations"), 0, "native DRC violations")
    zephyr_report = reports["native_zephyr_build"]
    zephyr_stdout = zephyr_report.get("backend", {}).get("stdout", "")
    if zephyr_report.get("status") == "pass":
        if "[170/170]" not in zephyr_stdout:
            raise RefreshError("Native Zephyr report does not contain the persisted 170/170 build completion")
    elif zephyr_report.get("status") == "blocked":
        failure_codes = {
            failure.get("code")
            for failure in zephyr_report.get("failures", [])
            if isinstance(failure, dict)
        }
        if "arm_newlib_unavailable" not in failure_codes:
            raise RefreshError("Blocked native Zephyr report lacks arm_newlib_unavailable evidence")
    else:
        raise RefreshError(f"Native Zephyr report has unsupported status {zephyr_report.get('status')!r}")
    physical_metrics = reports["physical_qualification"].get("metrics", {})
    _require_equal(physical_metrics.get("required_tests"), 9, "physical required test count")
    _require_equal(physical_metrics.get("missing_or_unapproved"), 9, "physical missing or unapproved count")

    physical_text = physical_plan_path.read_text(encoding="utf-8").lower()
    if "via-in-pad" not in physical_text:
        raise RefreshError("Physical qualification plan must explicitly name the via-in-pad process")
    physical_plan = _read_json(physical_plan_json_path)
    process_tests = [
        test for test in physical_plan.get("tests", []) if isinstance(test, dict) and test.get("id") == "via_in_pad_process_qualification"
    ]
    if len(process_tests) != 1:
        raise RefreshError("Physical qualification plan must contain one via_in_pad_process_qualification test")
    conditions = process_tests[0].get("conditions", {})
    _require_equal(conditions.get("qualification_status"), "unqualified", "via-in-pad qualification status")
    declared_locations = conditions.get("declared_locations", [])
    if not any(
        isinstance(location, dict) and location.get("reference") == "U2" and str(location.get("pad")) == "57"
        for location in declared_locations
    ):
        raise RefreshError("Via-in-pad qualification plan must explicitly declare U2.57")

    generated_at = bundle.get("generated_at")
    if not isinstance(generated_at, str) or len(generated_at) < 10:
        raise RefreshError("Review bundle has no usable generated_at timestamp")
    return Snapshot(
        bundle=bundle,
        bundle_hash=expected_bundle_hash,
        bundle_file_sha256=_sha256_file(bundle_path),
        generated_at=generated_at,
        reports=reports,
        board_sha256=board_sha256,
        routing=routing,
    )


def _first_line(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    output = (result.stdout or result.stderr).splitlines()
    if not output:
        raise RefreshError(f"Tool returned no version string: {' '.join(command)}")
    return output[0].strip()


def _resolve_tools() -> Toolchain:
    rsvg_convert = shutil.which(os.environ.get("RSVG_CONVERT", "rsvg-convert"))
    ffmpeg = shutil.which(os.environ.get("FFMPEG", "ffmpeg"))
    ffprobe = shutil.which(os.environ.get("FFPROBE", "ffprobe"))
    missing = [name for name, path in (("rsvg-convert", rsvg_convert), ("ffmpeg", ffmpeg), ("ffprobe", ffprobe)) if not path]
    if missing:
        raise RefreshError("Missing demo renderer prerequisites: " + ", ".join(missing))
    encoders = subprocess.run([ffmpeg, "-hide_banner", "-encoders"], check=True, capture_output=True, text=True).stdout
    if "libx264" not in encoders:
        raise RefreshError("ffmpeg must include the libx264 encoder for the checked-in MP4")
    return Toolchain(
        rsvg_convert=rsvg_convert,
        rsvg_version=_first_line([rsvg_convert, "--version"]),
        ffmpeg=ffmpeg,
        ffmpeg_version=_first_line([ffmpeg, "-version"]),
        ffprobe=ffprobe,
    )


def _frame_one() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <rect width="1200" height="675" fill="#0b0f14"/>
  <text x="64" y="72" fill="#35e08b" font-family="DejaVu Sans Mono, monospace" font-size="28" font-weight="700">hw-codesign</text>
  <text x="1136" y="72" text-anchor="end" fill="#768394" font-family="DejaVu Sans Mono, monospace" font-size="18">PROMPT → CANDIDATE → BLOCKERS</text>
  <rect x="64" y="116" width="1072" height="452" rx="18" fill="#111822" stroke="#293545" stroke-width="2"/>
  <circle cx="96" cy="148" r="7" fill="#ff6b6b"/><circle cx="120" cy="148" r="7" fill="#ffd166"/><circle cx="144" cy="148" r="7" fill="#35e08b"/>
  <text x="96" y="205" fill="#35e08b" font-family="DejaVu Sans Mono, monospace" font-size="20">$ hw --root . design-candidate golden_rp2040_usb_hid --brief \\</text>
  <text x="96" y="249" fill="#dce7f3" font-family="DejaVu Sans Mono, monospace" font-size="20">&quot;Design a 2-layer RP2040 USB HID and CDC board powered</text>
  <text x="96" y="283" fill="#dce7f3" font-family="DejaVu Sans Mono, monospace" font-size="20"> from USB-C, with 2 MB QSPI flash, a 12 MHz crystal,</text>
  <text x="96" y="317" fill="#dce7f3" font-family="DejaVu Sans Mono, monospace" font-size="20"> USB ESD protection, SWD debug, 1 ms HID reports, and</text>
  <text x="96" y="351" fill="#dce7f3" font-family="DejaVu Sans Mono, monospace" font-size="20"> enumeration within 500 ms. Use Zephyr and keep the board</text>
  <text x="96" y="385" fill="#dce7f3" font-family="DejaVu Sans Mono, monospace" font-size="20"> within 65 mm by 30 mm.&quot;</text>
  <text x="96" y="437" fill="#768394" font-family="DejaVu Sans Mono, monospace" font-size="19">lowering requirements… resolving parts… generating source… running gates…</text>
  <rect x="96" y="476" width="314" height="48" rx="24" fill="#153829" stroke="#35e08b"/>
  <text x="253" y="507" text-anchor="middle" fill="#8ff0bd" font-family="DejaVu Sans, sans-serif" font-size="19" font-weight="700">SUPPORTED FAMILY: RP2040</text>
  <text x="64" y="625" fill="#768394" font-family="DejaVu Sans, sans-serif" font-size="18">Repository evidence snapshot · no fabricated-board claim</text>
</svg>
"""


def _frame_two(snapshot: Snapshot) -> str:
    short_hash = html.escape(snapshot.bundle_hash[:12])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="675" viewBox="0 0 1200 675">
  <rect width="1200" height="675" fill="#0b0f14"/>
  <text x="64" y="72" fill="#35e08b" font-family="DejaVu Sans Mono, monospace" font-size="28" font-weight="700">hw-codesign</text>
  <text x="1136" y="72" text-anchor="end" fill="#768394" font-family="DejaVu Sans Mono, monospace" font-size="18">REVIEWABLE CANDIDATE</text>
  <rect x="64" y="116" width="432" height="466" rx="18" fill="#111822" stroke="#293545" stroke-width="2"/>
  <text x="96" y="171" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="30" font-weight="700">Candidate generated</text>
  <text x="96" y="214" fill="#8ff0bd" font-family="DejaVu Sans Mono, monospace" font-size="17">golden_rp2040_usb_hid</text>
  <line x1="96" y1="244" x2="464" y2="244" stroke="#293545"/>
  <text x="96" y="286" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="20">31 resolved components</text>
  <text x="96" y="326" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="20">Freerouting raw 0 · post-fill 0</text>
  <text x="96" y="366" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="20">Native ERC 0 · DRC 0</text>
  <text x="96" y="406" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="20">Zephyr build BLOCKED · ARM newlib</text>
  <text x="96" y="446" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="20">Bundle {short_hash}</text>
  <rect x="96" y="495" width="238" height="48" rx="24" fill="#153829" stroke="#35e08b"/>
  <text x="215" y="526" text-anchor="middle" fill="#8ff0bd" font-family="DejaVu Sans, sans-serif" font-size="19" font-weight="700">CANDIDATE ONLY</text>
  <rect x="528" y="116" width="608" height="466" rx="18" fill="#f6f7f9" stroke="#293545" stroke-width="2"/>
  <image x="548" y="138" width="568" height="420" preserveAspectRatio="xMidYMid meet" xlink:href="golden-rp2040-assembly.png"/>
  <text x="64" y="625" fill="#768394" font-family="DejaVu Sans, sans-serif" font-size="18">CAD and compiler gates pass; this assembly drawing is generated evidence, not a fabricated board.</text>
</svg>
"""


def _frame_three(snapshot: Snapshot) -> str:
    short_hash = html.escape(snapshot.bundle_hash[:12])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <rect width="1200" height="675" fill="#0b0f14"/>
  <text x="64" y="72" fill="#35e08b" font-family="DejaVu Sans Mono, monospace" font-size="28" font-weight="700">hw-codesign</text>
  <text x="1136" y="72" text-anchor="end" fill="#ffcf70" font-family="DejaVu Sans Mono, monospace" font-size="18">FABRICATION BLOCKER REPORT</text>
  <text x="64" y="136" fill="#dce7f3" font-family="DejaVu Sans, sans-serif" font-size="34" font-weight="700">It stops before pretending the board is ready.</text>
  <g font-family="DejaVu Sans, sans-serif">
    <rect x="64" y="178" width="520" height="136" rx="16" fill="#13231d" stroke="#2b7655"/>
    <text x="92" y="220" fill="#8ff0bd" font-size="20" font-weight="700">CAD + FIRMWARE STATUS</text>
    <text x="92" y="258" fill="#dce7f3" font-size="19">Route 0 raw / 0 post-fill · ERC 0 · DRC 0</text>
    <text x="92" y="286" fill="#8b98a8" font-size="17">Zephyr build is blocked: ARM newlib unavailable.</text>
    <rect x="616" y="178" width="520" height="136" rx="16" fill="#151a22" stroke="#4a3c27"/>
    <text x="644" y="220" fill="#ffcf70" font-size="20" font-weight="700">SOURCING EVIDENCE</text>
    <text x="644" y="258" fill="#dce7f3" font-size="19">Current availability and resilient alternates</text>
    <text x="644" y="286" fill="#8b98a8" font-size="17">remain failed or blocked for the selected BOM.</text>
    <rect x="64" y="338" width="520" height="136" rx="16" fill="#151a22" stroke="#4a3c27"/>
    <text x="92" y="380" fill="#ffcf70" font-size="20" font-weight="700">FABRICATION PROCESS OPEN</text>
    <text x="92" y="418" fill="#dce7f3" font-size="19">U2.57 uses via-in-pad; fill/cap/tent</text>
    <text x="92" y="446" fill="#8b98a8" font-size="17">requirements and fabricator capability are unqualified.</text>
    <rect x="616" y="338" width="520" height="136" rx="16" fill="#151a22" stroke="#4a3c27"/>
    <text x="644" y="380" fill="#ffcf70" font-size="20" font-weight="700">PHYSICAL QUALIFICATION</text>
    <text x="644" y="418" fill="#dce7f3" font-size="19">Not fabricated: assembly, bring-up, thermal,</text>
    <text x="644" y="446" fill="#8b98a8" font-size="17">SI/PI, EMI, retention and ESD evidence are absent.</text>
  </g>
  <rect x="64" y="518" width="1072" height="70" rx="16" fill="#2b1919" stroke="#ff7a7a"/>
  <text x="600" y="562" text-anchor="middle" fill="#ffaaaa" font-family="DejaVu Sans Mono, monospace" font-size="20" font-weight="700">44 PASS · 1 FAIL · 3 BLOCKED · CANDIDATE ≠ FABRICATION-QUALIFIED</text>
  <text x="64" y="625" fill="#768394" font-family="DejaVu Sans, sans-serif" font-size="18">Bundle {short_hash} · open the read-only review for gate-level evidence and artifact hashes.</text>
</svg>
"""


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise RefreshError(f"Command failed ({' '.join(command)}): {stderr}") from exc


def _render_png(toolchain: Toolchain, source: Path, output: Path, width: int, height: int) -> None:
    _run(
        [
            toolchain.rsvg_convert,
            "--width",
            str(width),
            "--height",
            str(height),
            "--background-color",
            "#ffffff" if "assembly" in source.name else "#0b0f14",
            "--output",
            str(output),
            str(source),
        ]
    )


def _video_inputs(toolchain: Toolchain, assets: Path) -> list[str]:
    result: list[str] = [toolchain.ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    for frame, duration in (("demo-frame-1.png", 6), ("demo-frame-2.png", 7), ("demo-frame-3.png", 7)):
        result.extend(["-loop", "1", "-framerate", "10", "-t", str(duration), "-i", str(assets / frame)])
    return result


def _render_video(toolchain: Toolchain, assets: Path, demo_dir: Path) -> None:
    frame_concat = (
        "[0:v]fps=10,setpts=PTS-STARTPTS[v0];"
        "[1:v]fps=10,setpts=PTS-STARTPTS[v1];"
        "[2:v]fps=10,setpts=PTS-STARTPTS[v2];"
        "[v0][v1][v2]concat=n=3:v=1:a=0"
    )
    mp4_filter = frame_concat + ",pad=1200:676:0:0:color=#0b0f14,format=yuv420p[out]"
    _run(
        _video_inputs(toolchain, assets)
        + [
            "-filter_complex",
            mp4_filter,
            "-map",
            "[out]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "20",
            "-threads",
            "1",
            "-map_metadata",
            "-1",
            "-fflags",
            "+bitexact",
            "-flags:v",
            "+bitexact",
            "-movflags",
            "+faststart",
            str(demo_dir / "prompt-to-board-20s.mp4"),
        ]
    )

    gif_filter = (
        frame_concat + ",scale=960:540:flags=lanczos,split[gif_a][gif_b];"
        "[gif_a]palettegen=max_colors=128:stats_mode=diff[palette];"
        "[gif_b][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[out]"
    )
    _run(
        _video_inputs(toolchain, assets)
        + [
            "-filter_complex",
            gif_filter,
            "-map",
            "[out]",
            "-an",
            "-gifflags",
            "-offsetting",
            str(demo_dir / "prompt-to-board-20s.gif"),
        ]
    )


def _probe_media(toolchain: Toolchain, path: Path, *, width: int, height: int, codec: str) -> None:
    result = subprocess.run(
        [
            toolchain.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_name,width,height,avg_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    if len(streams) != 1:
        raise RefreshError(f"Expected one video stream in {path}")
    stream = streams[0]
    _require_equal(stream.get("codec_name"), codec, f"{path.name} codec")
    _require_equal(stream.get("width"), width, f"{path.name} width")
    _require_equal(stream.get("height"), height, f"{path.name} height")
    duration = float(payload.get("format", {}).get("duration", 0))
    if abs(duration - 20.0) > 0.05:
        raise RefreshError(f"{path.name} duration must be 20 seconds, found {duration}")


def _replace_marked_block(text: str, block: str) -> str:
    marked = f"{ROOT_EVIDENCE_START}\n{block.rstrip()}\n{ROOT_EVIDENCE_END}"
    if ROOT_EVIDENCE_START in text or ROOT_EVIDENCE_END in text:
        pattern = re.compile(
            re.escape(ROOT_EVIDENCE_START) + r".*?" + re.escape(ROOT_EVIDENCE_END),
            flags=re.DOTALL,
        )
        if len(pattern.findall(text)) != 1:
            raise RefreshError("Root README demo evidence markers are malformed")
        return pattern.sub(marked, text)
    anchor = "[read the validation contract](docs/validation-contract.md)"
    heading = "## The 20-second product loop"
    if anchor not in text or heading not in text:
        raise RefreshError("Cannot locate root README demo evidence section")
    prefix, remainder = text.split(anchor, 1)
    _, suffix = remainder.split(heading, 1)
    return f"{prefix}{anchor}\n\n{marked}\n\n{heading}{suffix}"


def _replace_markdown_section(text: str, heading: str, next_heading: str, body: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\n.*?(?=^{re.escape(next_heading)}\n)",
        flags=re.DOTALL | re.MULTILINE,
    )
    if len(pattern.findall(text)) != 1:
        raise RefreshError(f"Cannot uniquely replace Markdown section {heading!r}")
    return pattern.sub(f"{heading}\n\n{body.rstrip()}\n\n", text)


def _root_evidence(snapshot: Snapshot) -> str:
    return f"""The demo is a dated full-toolchain repository run against the RP2040 USB-device
family. It produced a candidate, not a fabrication-qualified board: 44 of 48
recorded gates passed, 1 failed, and 3 were blocked. Freerouting reports zero
raw unrouted connections and KiCad reports zero post-fill unconnected items;
native ERC and DRC each report zero violations. The native Zephyr build is
blocked because the selected ARM toolchain lacks newlib runtime files.

The remaining evidence is material: sourcing fails, current supplier
availability is blocked, the native Zephyr build is blocked on ARM newlib, and
physical qualification is blocked. The
board has not been fabricated, and the U2.57 via-in-pad fill/cap/tent process is
unqualified. Bundle `{snapshot.bundle_hash}` records those boundaries."""


def _project_current_evidence(snapshot: Snapshot) -> str:
    return f"""- The current spec schema passes with zero errors.
- The resolved graph contains 31 manufacturer-identified components and 24
  named nets.
- A real KiCad schematic is generated with 36 intentional no-connect markers;
  native KiCad ERC passes with zero violations.
- The tscircuit layout places all 31 components with parity, emits 91 traces,
  and reports zero PCB validation errors.
- Freerouting records zero raw unrouted connections; the persisted zone fill has
  zero post-import unconnected items, and native KiCad DRC has zero violations.
- The native RP2040 Zephyr build is blocked because ARM newlib runtime files
  (`nosys.specs`, `libc.a`, `libnosys.a`) are unavailable; no firmware build
  completion is claimed.
- Electronics, mechanical, firmware, BOM, candidate fabrication, and review
  artifacts were generated.
- The dated full-toolchain review records 48 gates: 44 pass, 1 fail, 3 blocked.
- Review bundle hash:
  `{snapshot.bundle_hash}`.

Open the repository demo and review in [`docs/demo`](../../docs/demo/README.md)."""


def _project_blockers() -> str:
    return """- Current supplier availability and critical-role resilience need fresh,
  timestamped evidence; `sourcing` fails, while `sourcing_resilience` passes and
  `supplier_availability` remains blocked. The native Zephyr build is also
  blocked because ARM newlib runtime files are unavailable.
- U2 exposed pad U2.57 uses a via-in-pad connection. Native DRC acceptance does
  not qualify its tented, plugged, filled, or capped fabrication process; the
  required stack-up/fabricator capability and acceptance evidence are open.
- The candidate has not been fabricated or ordered. Assembly inspection,
  current-limited power-up, rail measurements, firmware interface bring-up,
  thermal, SI/PI, EMI, vibration/retention, and ESD/ingress evidence are absent.

The qualification checklist is in
[`validation/physical/qualification_plan.md`](validation/physical/qualification_plan.md).
Physical evidence must be captured with artifact hashes and approval status via
`hw record-physical-evidence`; prose in this README cannot close a gate."""


def _demo_readme(snapshot: Snapshot, toolchain: Toolchain, hashes: dict[str, str]) -> str:
    date = snapshot.generated_at[:10]
    hash_lines = "\n".join(f"{digest}  {path}" for path, digest in hashes.items())
    return f"""# Prompt-to-board demo evidence

This directory is a date-stamped, reproducible product demo for the
`golden_rp2040_usb_hid` candidate. It demonstrates candidate generation and an
explicit blocker report; it does **not** claim that the board has been fabricated
or qualified.

## 20-second flow

The prompt shown in the demo is the prompt supplied to the requirements compiler:

> Design a 2-layer RP2040 USB HID and CDC board powered from USB-C, with 2 MB
> QSPI flash, a 12 MHz crystal, USB ESD protection, SWD debug, 1 ms HID reports,
> and enumeration within 500 ms. Use Zephyr and keep the board within 65 mm by
> 30 mm.

The three frames show:

1. The brief and supported board family.
2. The generated candidate and its persisted CAD/compiler evidence.
3. The unresolved blockers: sourcing, current supplier availability, an ARM
   newlib toolchain gap, the unqualified U2.57 via-in-pad fabrication process,
   and physical qualification.

The animation is available as [GIF](prompt-to-board-20s.gif) and
[MP4](prompt-to-board-20s.mp4). The [read-only review](index.html) is a
self-contained HTML file suitable for static hosting.

## Reproduction

First produce a full-toolchain report snapshot and export the supported
self-contained review. Then let the repository-owned script verify exact
report/bundle agreement and refresh every checked-in demo claim from that one
snapshot:

```bash
hw --root . check golden_rp2040_usb_hid
hw --root . export-standalone-review golden_rp2040_usb_hid
python scripts/refresh_demo.py
python scripts/refresh_demo.py --check
python scripts/refresh_demo.py --verify-release-evidence
```

`refresh_demo.py` never generates or validates the board. It fails before
writing if the 48 gate reports, bundle contents, canonical bundle hash, routed
board hash, native CAD metrics, Zephyr status, or physical-process wording
disagree. The full refresh and byte-for-byte `--check` require `rsvg-convert`,
`ffmpeg` with `libx264`, and `ffprobe`. The cross-platform
`--verify-release-evidence` path needs only Python; it verifies that the
checked-in bundle, standalone review, hash receipt, gate counts, native-tool
claims, and fabrication blockers agree without regenerating evidence.

The demo snapshot was exported on {date}. It records 48 gates: 44 pass, 1 fail,
and 3 blocked. Freerouting records zero raw unrouted connections and KiCad has
zero post-fill unconnected items. Native ERC and DRC each report zero
violations. The native Zephyr build is blocked because ARM newlib runtime files
are unavailable. The canonical bundle
hash is `{snapshot.bundle_hash}`.

The failed gate is `sourcing`; the blocked gates are `supplier_availability`,
`native_zephyr_build`, and `physical_qualification`. The board has
not been fabricated. In particular, U2.57 uses via-in-pad, but the required
tented/plugged/filled/capped process and fabricator capability are unqualified.

## Renderer receipt

- `{toolchain.rsvg_version}`
- `{toolchain.ffmpeg_version}`

## Artifact hashes

```text
{hash_lines}
```

The assembly render is a CAD preview, not physical evidence. Model declarations,
software gates, and clean native DRC do not establish fit, solderability,
bring-up, thermal, SI/PI, EMI, retention, ESD, or manufacturing-process
qualification.
"""


def _build_expected(repo_root: Path, snapshot: Snapshot, toolchain: Toolchain, output_root: Path) -> dict[Path, Path]:
    demo_dir = output_root / "docs" / "demo"
    assets = demo_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    project = repo_root / "projects" / PROJECT

    source_review = project / "exports" / "working" / "review" / "review_standalone.html"
    source_bundle = project / "exports" / "working" / "review" / "bundle.json"
    source_assembly = project / "exports" / "candidates" / "reference-fabrication" / "fabrication" / "assembly_drawing.svg"
    if not source_assembly.is_file():
        raise RefreshError(f"Missing generated assembly drawing: {source_assembly}")
    shutil.copyfile(source_review, demo_dir / "index.html")
    shutil.copyfile(source_bundle, demo_dir / "bundle.json")
    shutil.copyfile(source_assembly, assets / "golden-rp2040-assembly.svg")

    (assets / "demo-frame-1.svg").write_text(_frame_one(), encoding="utf-8")
    (assets / "demo-frame-2.svg").write_text(_frame_two(snapshot), encoding="utf-8")
    (assets / "demo-frame-3.svg").write_text(_frame_three(snapshot), encoding="utf-8")
    _render_png(toolchain, assets / "golden-rp2040-assembly.svg", assets / "golden-rp2040-assembly.png", 1600, 900)
    for number in (1, 2, 3):
        _render_png(toolchain, assets / f"demo-frame-{number}.svg", assets / f"demo-frame-{number}.png", 1200, 675)
    _render_video(toolchain, assets, demo_dir)
    _probe_media(toolchain, demo_dir / "prompt-to-board-20s.mp4", width=1200, height=676, codec="h264")
    _probe_media(toolchain, demo_dir / "prompt-to-board-20s.gif", width=960, height=540, codec="gif")

    root_readme = (repo_root / "README.md").read_text(encoding="utf-8")
    root_readme = _replace_marked_block(root_readme, _root_evidence(snapshot))
    (output_root / "README.md").parent.mkdir(parents=True, exist_ok=True)
    (output_root / "README.md").write_text(root_readme, encoding="utf-8")

    project_readme_path = project / "README.md"
    project_readme = project_readme_path.read_text(encoding="utf-8")
    project_readme = _replace_markdown_section(
        project_readme,
        "## Current evidence",
        "## Release blockers",
        _project_current_evidence(snapshot),
    )
    # The release-blocker section is the final section today, so replace to EOF.
    release_pattern = re.compile(r"^## Release blockers\n.*\Z", flags=re.DOTALL | re.MULTILINE)
    if len(release_pattern.findall(project_readme)) != 1:
        raise RefreshError("Cannot uniquely replace project README release blockers")
    project_readme = release_pattern.sub(f"## Release blockers\n\n{_project_blockers().rstrip()}\n", project_readme)
    destination_project_readme = output_root / project_readme_path.relative_to(repo_root)
    destination_project_readme.parent.mkdir(parents=True, exist_ok=True)
    destination_project_readme.write_text(project_readme, encoding="utf-8")

    hash_targets = [
        "bundle.json",
        "index.html",
        "prompt-to-board-20s.gif",
        "prompt-to-board-20s.mp4",
        "assets/golden-rp2040-assembly.svg",
        "assets/golden-rp2040-assembly.png",
        "assets/demo-frame-1.svg",
        "assets/demo-frame-1.png",
        "assets/demo-frame-2.svg",
        "assets/demo-frame-2.png",
        "assets/demo-frame-3.svg",
        "assets/demo-frame-3.png",
    ]
    hashes = {relative: _sha256_file(demo_dir / relative) for relative in hash_targets}
    hashes[f"../../projects/{PROJECT}/electronics/generated/kicad/{PROJECT}.kicad_pcb"] = snapshot.board_sha256
    (demo_dir / "README.md").write_text(_demo_readme(snapshot, toolchain, hashes), encoding="utf-8")

    generated = [demo_dir / "README.md", output_root / "README.md", destination_project_readme]
    generated.extend(demo_dir / relative for relative in hash_targets)
    return {path.relative_to(output_root): path for path in generated}


def _write_or_check(repo_root: Path, expected: dict[Path, Path], check: bool) -> list[str]:
    changed: list[str] = []
    for relative, source in sorted(expected.items(), key=lambda item: str(item[0])):
        destination = repo_root / relative
        current = destination.read_bytes() if destination.is_file() else None
        wanted = source.read_bytes()
        if current == wanted:
            continue
        changed.append(relative.as_posix())
        if check:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.refresh-demo.tmp")
        temporary.write_bytes(wanted)
        os.replace(temporary, destination)
    if check and changed:
        raise RefreshError("Demo is stale; refresh these files: " + ", ".join(changed))
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate byte-for-byte freshness without writing")
    mode.add_argument(
        "--verify-release-evidence",
        action="store_true",
        help="verify checked-in bundle/review evidence without renderer or native-tool dependencies",
    )
    args = parser.parse_args(argv)
    repo_root = args.root.resolve()
    try:
        if args.verify_release_evidence:
            bundle_hash, bundle_file_sha256 = _verify_release_evidence(repo_root)
            print(
                json.dumps(
                    {
                        "status": "verified",
                        "bundle_hash": bundle_hash,
                        "bundle_file_sha256": bundle_file_sha256,
                        "summary": EXPECTED_SUMMARY,
                        "source": "docs/demo/bundle.json",
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        snapshot = _load_snapshot(repo_root)
        toolchain = _resolve_tools()
        with tempfile.TemporaryDirectory(prefix="hw-codesign-demo-") as temporary:
            expected = _build_expected(repo_root, snapshot, toolchain, Path(temporary))
            changed = _write_or_check(repo_root, expected, args.check)
    except (RefreshError, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"refresh_demo: error: {exc}", file=sys.stderr)
        return 1
    action = "verified" if args.check else ("refreshed" if changed else "already current")
    print(
        json.dumps(
            {
                "status": action,
                "bundle_hash": snapshot.bundle_hash,
                "summary": EXPECTED_SUMMARY,
                "changed": changed,
                "renderer": toolchain.rsvg_version,
                "video_encoder": toolchain.ffmpeg_version,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
