"""Generate a self-contained HTML review report from a review bundle."""

from __future__ import annotations

import base64
import json
from html import escape
from pathlib import Path
from typing import Any

_STATUS_LABEL = {
    "pass": "Passed",
    "fail": "Failed",
    "blocked": "Blocked",
    "candidate": "Candidate",
    "released": "Released",
}

_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Hardware review · @@PROJECT_NAME@@ @@REVISION@@</title>
<style>
:root {
  --ink: #05080a;
  --surface: #0a0e11;
  --surface-raised: #0f1519;
  --surface-soft: #131b20;
  --line: #263139;
  --line-strong: #3b4951;
  --text: #f1f5f6;
  --muted: #94a0a8;
  --quiet: #65727a;
  --signal: #38d9ed;
  --signal-soft: rgba(56, 217, 237, .11);
  --pass: #56d69a;
  --pass-soft: rgba(86, 214, 154, .11);
  --fail: #ff6b6b;
  --fail-soft: rgba(255, 107, 107, .12);
  --blocked: #f6b863;
  --blocked-soft: rgba(246, 184, 99, .12);
  --radius: 14px;
  --display: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  --body: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  overflow-x: hidden;
  color: var(--text);
  background:
    radial-gradient(circle at 76% -8%, rgba(56, 217, 237, .08), transparent 28rem),
    linear-gradient(180deg, #080b0d 0, var(--ink) 42rem);
  font-family: var(--body);
  font-size: 15px;
  line-height: 1.55;
}
button, input, textarea { font: inherit; }
button { color: inherit; }
a { color: var(--signal); }
.skip-link { position: fixed; left: 1rem; top: -4rem; z-index: 100; padding: .65rem 1rem; background: var(--text); color: var(--ink); }
.skip-link:focus { top: 1rem; }
.site-header {
  height: 64px;
  padding: 0 clamp(1rem, 4vw, 3rem);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(148, 160, 168, .18);
  background: rgba(5, 8, 10, .82);
  backdrop-filter: blur(18px);
  position: sticky;
  top: 0;
  z-index: 20;
}
.brand { display: inline-flex; align-items: center; gap: .75rem; font: 600 .9rem/1 var(--display); letter-spacing: .04em; }
.brand-mark { width: 28px; height: 32px; color: #c6cdd1; }
.brand-mark .signal { stroke: var(--signal); }
.header-meta { color: var(--muted); font: .72rem/1.3 var(--display); text-align: right; }
main { width: min(1180px, calc(100% - 2rem)); margin: 0 auto; padding-bottom: 7rem; }
.hero {
  min-height: 570px;
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(290px, .7fr);
  gap: clamp(3rem, 8vw, 7rem);
  align-items: center;
  padding: clamp(4rem, 9vw, 8rem) 0 5rem;
}
.eyebrow { margin: 0 0 1rem; color: var(--signal); font: 600 .72rem/1.2 var(--display); letter-spacing: .16em; text-transform: uppercase; }
h1 { max-width: 780px; margin: 0; font: 500 clamp(2.65rem, 7vw, 5.8rem)/.98 var(--display); letter-spacing: -.075em; }
.lede { max-width: 660px; margin: 1.65rem 0 0; color: #b5c0c6; font-size: clamp(1rem, 1.6vw, 1.2rem); }
.hero-actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 2rem; }
.button {
  min-height: 44px;
  padding: .72rem 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .55rem;
  border: 1px solid var(--line-strong);
  border-radius: 8px;
  background: transparent;
  color: var(--text);
  font-weight: 650;
  cursor: pointer;
  text-decoration: none;
  transition: border-color .18s ease, background .18s ease, transform .18s ease;
}
.button:hover { border-color: var(--muted); background: rgba(255,255,255,.035); transform: translateY(-1px); }
.button.primary { border-color: var(--signal); background: var(--signal); color: #021013; }
.button.primary:hover { background: #6ee6f4; }
.button.small { min-height: 38px; padding: .55rem .75rem; font-size: .84rem; }
.button:focus-visible, input:focus-visible, textarea:focus-visible, summary:focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; }
.signal-card {
  position: relative;
  min-height: 390px;
  padding: 2rem 1.8rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid var(--line-strong);
  background: linear-gradient(145deg, rgba(15,21,25,.95), rgba(8,12,14,.72));
  clip-path: polygon(16px 0, calc(100% - 16px) 0, 100% 16px, 100% calc(100% - 16px), calc(100% - 16px) 100%, 16px 100%, 0 calc(100% - 16px), 0 16px);
}
.signal-card::before { content: ""; position: absolute; top: 2rem; bottom: 2rem; left: 1.8rem; width: 2px; background: linear-gradient(var(--signal), rgba(56,217,237,.08)); box-shadow: 0 0 20px rgba(56,217,237,.38); }
.signal-card-head, .signal-counts { padding-left: 1.7rem; }
.state-label { display: block; color: var(--muted); font: .68rem/1.2 var(--display); letter-spacing: .13em; text-transform: uppercase; }
.state-value { display: block; margin-top: .55rem; font: 500 1.55rem/1.15 var(--display); }
.state-value.fail { color: var(--fail); }
.state-value.blocked { color: var(--blocked); }
.state-value.pass, .state-value.released { color: var(--pass); }
.signal-counts { display: grid; grid-template-columns: repeat(3, 1fr); gap: .65rem; }
.count { padding-top: .85rem; border-top: 1px solid var(--line); }
.count strong { display: block; font: 500 1.65rem/1 var(--display); }
.count span { display: block; margin-top: .4rem; color: var(--muted); font-size: .76rem; }
.count.fail strong { color: var(--fail); }
.count.blocked strong { color: var(--blocked); }
.count.pass strong { color: var(--pass); }
.context-strip { display: flex; flex-wrap: wrap; gap: .55rem; margin-top: 2rem; }
.context-chip { padding: .35rem .58rem; border: 1px solid var(--line); border-radius: 5px; color: var(--muted); font: .7rem/1.3 var(--display); }
.section { padding: 5.5rem 0; border-top: 1px solid rgba(148,160,168,.18); scroll-margin-top: 82px; }
.section-heading { display: grid; grid-template-columns: minmax(0, .7fr) minmax(300px, 1.3fr); gap: 2rem; align-items: end; margin-bottom: 2.2rem; }
.kicker { margin: 0 0 .6rem; color: var(--signal); font: 600 .68rem/1.2 var(--display); letter-spacing: .14em; text-transform: uppercase; }
h2 { margin: 0; font: 500 clamp(1.8rem, 4vw, 3.1rem)/1.04 var(--display); letter-spacing: -.055em; }
.section-intro { margin: 0; color: var(--muted); font-size: 1rem; }
.workflow-note { display: flex; gap: .9rem; margin-bottom: 1.25rem; padding: 1rem 1.1rem; border-left: 2px solid var(--signal); background: var(--signal-soft); color: #c7d5da; }
.workflow-note strong { color: var(--text); }
.toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: .7rem; margin: 1.3rem 0; }
.toolbar .selection-count { margin-right: auto; color: var(--muted); font: .75rem/1 var(--display); }
.filter-group { display: flex; gap: .35rem; flex-wrap: wrap; }
.filter {
  padding: .48rem .7rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font-size: .78rem;
}
.filter[aria-pressed="true"] { color: var(--ink); background: var(--text); border-color: var(--text); }
.action-list { display: grid; gap: .75rem; }
.action-card {
  position: relative;
  display: grid;
  grid-template-columns: 30px minmax(0, 1.15fr) minmax(260px, .85fr);
  gap: 1rem;
  align-items: start;
  padding: 1.2rem;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(15, 21, 25, .78);
}
.action-card[data-kind="decision"] { border-left: 2px solid var(--signal); }
.action-card[data-kind="design"] { border-left: 2px solid var(--fail); }
.action-card[data-kind="environment"], .action-card[data-kind="evidence"] { border-left: 2px solid var(--blocked); }
.action-card.hidden { display: none; }
.task-check { width: 18px; height: 18px; margin: .2rem 0 0; accent-color: var(--signal); cursor: pointer; }
.task-type { display: inline-flex; align-items: center; gap: .4rem; color: var(--muted); font: .66rem/1.2 var(--display); letter-spacing: .1em; text-transform: uppercase; }
.task-type::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.action-card[data-kind="design"] .task-type { color: var(--fail); }
.action-card[data-kind="environment"] .task-type, .action-card[data-kind="evidence"] .task-type { color: var(--blocked); }
.action-card[data-kind="decision"] .task-type { color: var(--signal); }
.task-title { margin: .35rem 0 .3rem; font: 600 1rem/1.35 var(--display); overflow-wrap: anywhere; }
.task-summary { margin: 0; color: #aeb9bf; font-size: .88rem; }
.task-next { margin: 0 0 .75rem; color: var(--text); font-size: .86rem; }
.task-next strong { color: var(--signal); }
.task-note { width: 100%; min-height: 66px; resize: vertical; padding: .65rem .75rem; border: 1px solid var(--line); border-radius: 7px; background: #090d0f; color: var(--text); font-size: .82rem; }
.task-note::placeholder { color: var(--quiet); }
.decision-guide { grid-column: 2 / -1; padding: 1rem; border: 1px solid rgba(56,217,237,.24); border-radius: 9px; background: rgba(56,217,237,.045); }
.decision-guide-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .85rem 1.2rem; }
.decision-guide-block > span { display: block; margin-bottom: .3rem; color: var(--quiet); font: 600 .64rem/1.2 var(--display); letter-spacing: .09em; text-transform: uppercase; }
.decision-guide-block strong, .decision-guide-block p { margin: 0; color: #c3cdd1; font-size: .84rem; }
.decision-guide-block strong { color: var(--text); }
.confidence { display: inline-flex; margin-left: .35rem; padding: .15rem .35rem; border: 1px solid var(--line-strong); border-radius: 4px; color: var(--muted); font: .62rem/1 var(--display); text-transform: uppercase; }
.decision-guide-block .decision-rationale { margin-top: .35rem; color: var(--muted); font-size: .78rem; }
.decision-options { display: grid; gap: .45rem; margin: 1rem 0 0; padding: 0; border: 0; }
.decision-options legend { margin-bottom: .45rem; color: var(--text); font: 600 .72rem/1.2 var(--display); }
.decision-option { display: flex; align-items: flex-start; gap: .65rem; padding: .65rem .7rem; border: 1px solid var(--line); border-radius: 7px; background: rgba(5,8,10,.56); color: #b5c0c6; font-size: .82rem; cursor: pointer; }
.decision-option:has(input:checked) { border-color: var(--signal); background: var(--signal-soft); color: var(--text); }
.decision-option input { margin-top: .18rem; accent-color: var(--signal); }
.recommended-tag { margin-left: auto; color: var(--signal); font: .6rem/1 var(--display); letter-spacing: .07em; text-transform: uppercase; }
.empty-actions { padding: 2rem; border: 1px solid rgba(86,214,154,.28); background: var(--pass-soft); border-radius: var(--radius); }
.empty-actions strong { display: block; color: var(--pass); font: 500 1.25rem/1.2 var(--display); }
.empty-actions p { margin-bottom: 0; color: #b6c4c0; }
.workflow-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; margin-top: 1.5rem; background: var(--line); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }
.workflow-step { min-height: 155px; padding: 1.25rem; background: var(--surface); }
.workflow-step span { color: var(--signal); font: .7rem/1 var(--display); }
.workflow-step strong { display: block; margin: .7rem 0 .35rem; font: 600 .92rem/1.3 var(--display); }
.workflow-step p { margin: 0; color: var(--muted); font-size: .83rem; }
.three-d-grid { display: grid; grid-template-columns: minmax(0,1.55fr) minmax(250px,.65fr); gap: 1rem; align-items: stretch; }
.assembly-viewer { min-height: 31rem; position: relative; overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius); background: #070a0c; }
.assembly-viewer canvas,.assembly-viewer img { display: block; width: 100%; height: 100%; min-height: 31rem; object-fit: contain; }
.assembly-viewer canvas { position: absolute; inset: 0; }
.evidence-card { padding: 1.25rem; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface-raised); font-size: .86rem; }
.evidence-card h3 { margin: .8rem 0 .45rem; font: 600 .95rem/1.3 var(--display); }
.evidence-card p { margin: .2rem 0 .8rem; color: var(--muted); }
.evidence-card ul { margin: .5rem 0; padding-left: 1.1rem; color: #b5c0c6; }
.status { display: inline-flex; align-items: center; gap: .4rem; font: 650 .68rem/1 var(--display); letter-spacing: .07em; text-transform: uppercase; }
.status::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.status.pass, .status.released { color: var(--pass); }
.status.fail { color: var(--fail); }
.status.blocked { color: var(--blocked); }
.status.other, .status.candidate { color: var(--signal); }
.check-controls { display: flex; flex-wrap: wrap; gap: .65rem; justify-content: space-between; margin-bottom: 1rem; }
.search { width: min(100%, 330px); padding: .65rem .8rem; border: 1px solid var(--line); border-radius: 7px; background: var(--surface); color: var(--text); }
.table-shell { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); }
table { width: 100%; border-collapse: collapse; font-size: .85rem; }
th, td { padding: .85rem 1rem; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--quiet); font: 600 .65rem/1.2 var(--display); letter-spacing: .1em; text-transform: uppercase; }
tbody tr:last-child td { border-bottom: 0; }
tbody tr:hover { background: rgba(255,255,255,.018); }
.gate-name { font: 550 .78rem/1.35 var(--display); overflow-wrap: anywhere; }
.plain-meaning { color: var(--muted); min-width: 260px; }
.metric-preview { color: var(--quiet); font: .72rem/1.5 var(--display); }
.technical-list { display: grid; gap: .65rem; }
details.tech { border: 1px solid var(--line); border-radius: 10px; background: var(--surface-raised); }
details.tech > summary { padding: .9rem 1rem; display: flex; align-items: center; gap: .7rem; cursor: pointer; list-style: none; }
details.tech > summary::-webkit-details-marker { display: none; }
details.tech > summary::after { content: "+"; margin-left: auto; color: var(--muted); font: 1rem/1 var(--display); }
details.tech[open] > summary::after { content: "−"; }
.finding { padding: .9rem 1rem; border-top: 1px solid var(--line); }
.finding-code { color: var(--fail); font: .7rem/1.2 var(--display); }
.finding p { margin: .45rem 0; color: #b5c0c6; }
.finding-path { color: var(--signal); font: .7rem/1.45 var(--display); overflow-wrap: anywhere; }
pre { margin: .6rem 0 0; padding: .8rem; overflow: auto; border-radius: 7px; background: #070a0c; color: #8f9ca3; font: .7rem/1.5 var(--display); white-space: pre-wrap; overflow-wrap: anywhere; }
.detail-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 1rem; }
.detail-card { padding: 1.25rem; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface-raised); }
.detail-card h3 { margin: 0 0 1rem; font: 600 .92rem/1.2 var(--display); }
.detail-list { display: grid; grid-template-columns: minmax(110px,.7fr) 1.3fr; gap: .65rem 1rem; margin: 0; font-size: .84rem; }
.detail-list dt { color: var(--quiet); }
.detail-list dd { margin: 0; overflow-wrap: anywhere; }
.model-table { margin-top: .8rem; }
.model-table summary { cursor: pointer; color: var(--signal); }
.toast { position: fixed; right: 1.2rem; bottom: 1.2rem; z-index: 50; max-width: 360px; padding: .8rem 1rem; border: 1px solid var(--signal); border-radius: 8px; background: #0b1518; color: var(--text); box-shadow: 0 18px 50px rgba(0,0,0,.42); transform: translateY(130%); transition: transform .22s ease; }
.toast.show { transform: translateY(0); }
.footer { padding-top: 2rem; color: var(--quiet); border-top: 1px solid var(--line); font: .7rem/1.6 var(--display); }
@media (max-width: 820px) {
  .hero { grid-template-columns: 1fr; min-height: auto; }
  .signal-card { min-height: 310px; }
  .section-heading { grid-template-columns: 1fr; align-items: start; }
  .action-card { grid-template-columns: 28px 1fr; }
  .action-control { grid-column: 2; }
  .decision-guide { grid-column: 2; }
  .decision-guide-grid { grid-template-columns: 1fr; }
  .workflow-steps { grid-template-columns: 1fr; }
  .three-d-grid { grid-template-columns: 1fr; }
  .assembly-viewer,.assembly-viewer canvas,.assembly-viewer img { min-height: 22rem; }
  .detail-grid { grid-template-columns: 1fr; }
}
@media (max-width: 520px) {
  .site-header { padding: 0 1rem; }
  .header-meta span { display: none; }
  main { width: min(100% - 1.25rem, 1180px); }
  .hero { padding-top: 3.5rem; gap: 2.5rem; }
  h1 { font-size: clamp(2.45rem, 14vw, 4rem); }
  .section { padding: 4rem 0; }
  .button { width: 100%; }
  .toolbar .selection-count { width: 100%; }
  .filter-group { width: 100%; }
  .action-card { padding: 1rem .85rem; gap: .7rem; }
  .detail-list { grid-template-columns: 1fr; gap: .2rem; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
</head>
<body data-project="@@PROJECT_ATTR@@" data-bundle-hash="@@HASH_ATTR@@">
<a class="skip-link" href="#main">Skip to review result</a>
<header class="site-header">
  <div class="brand">
    <svg class="brand-mark" viewBox="0 0 28 32" aria-hidden="true"><path d="M5 1.5h18l3.5 3.5v22L23 30.5H5L1.5 27V5z" fill="none" stroke="currentColor" stroke-width="1.5"/><path class="signal" d="M14 5v21" stroke-width="2"/><circle cx="18.5" cy="25.5" r="1.8" fill="currentColor"/></svg>
    <span>hw-codesign / review</span>
  </div>
  <div class="header-meta"><span>Evidence snapshot</span><br>@@HASH_SHORT@@</div>
</header>
<main id="main">
  <section class="hero" aria-labelledby="review-title">
    <div>
      <p class="eyebrow">Candidate review · @@REVISION@@</p>
      <h1 id="review-title">@@HEADLINE@@</h1>
      <p class="lede">@@LEDE@@</p>
      <div class="hero-actions">
        <a class="button primary" href="#resolution">Build a resolution plan <span aria-hidden="true">↓</span></a>
        <a class="button" href="#checks">See every check</a>
      </div>
      <div class="context-strip" aria-label="Project context">
        <span class="context-chip">@@PROJECT_NAME@@</span>
        <span class="context-chip">@@BACKEND@@ backend</span>
        <span class="context-chip">@@TARGET_USE@@</span>
        <span class="context-chip">generated @@GENERATED_AT@@</span>
      </div>
    </div>
    <aside class="signal-card" aria-label="Review status">
      <div class="signal-card-head">
        <span class="state-label">Current decision</span>
        <strong class="state-value @@STATE_CLASS@@">@@STATE_LABEL@@</strong>
      </div>
      <div class="signal-counts">
        <div class="count fail"><strong>@@FAIL_COUNT@@</strong><span>need a fix</span></div>
        <div class="count blocked"><strong>@@BLOCKED_COUNT@@</strong><span>could not run</span></div>
        <div class="count pass"><strong>@@PASS_COUNT@@</strong><span>validated</span></div>
      </div>
    </aside>
  </section>

  <section id="resolution" class="section" aria-labelledby="resolution-title">
    <div class="section-heading">
      <div><p class="kicker">What to do next</p><h2 id="resolution-title">Resolve the blockers</h2></div>
      <p class="section-intro">Each item below explains what stopped, why it matters, and the safest next move. Select only the work you want an agent or engineer to handle now.</p>
    </div>
    <div class="workflow-note"><span aria-hidden="true">⌁</span><div><strong>This page does not silently change your hardware project.</strong><br>It turns your selections and notes into a scoped agent workflow. Human approvals and physical test evidence stay human-controlled.</div></div>
    @@ACTION_TOOLBAR@@
    <div id="action-list" class="action-list">@@ACTION_CARDS@@</div>
    @@EMPTY_ACTIONS@@
    <div class="workflow-steps" aria-label="Resolution workflow">
      <div class="workflow-step"><span>01 / SCOPE</span><strong>Select and add context</strong><p>Choose the blockers to address. Add decisions, constraints, or evidence in the note fields.</p></div>
      <div class="workflow-step"><span>02 / REPAIR</span><strong>Hand off to your agent</strong><p>The copied prompt requests a repair plan first, safe changes second, and asks before approvals.</p></div>
      <div class="workflow-step"><span>03 / VERIFY</span><strong>Run every check again</strong><p>Regenerate the evidence snapshot. A local note or copied plan never counts as a passed gate.</p></div>
    </div>
  </section>

  @@THREE_D_HTML@@

  <section id="checks" class="section" aria-labelledby="checks-title">
    <div class="section-heading">
      <div><p class="kicker">Validation matrix</p><h2 id="checks-title">Every check</h2></div>
      <p class="section-intro"><strong>Failed</strong> means the check found a problem. <strong>Blocked</strong> means the check could not reach a result, usually because a tool, input, evidence record, or prerequisite is missing.</p>
    </div>
    <div class="check-controls">
      <input id="gate-search" class="search" type="search" placeholder="Search checks" aria-label="Search checks">
      <div class="filter-group" aria-label="Filter checks">
        <button class="filter gate-filter" data-status="all" aria-pressed="true">All @@TOTAL_COUNT@@</button>
        <button class="filter gate-filter" data-status="fail" aria-pressed="false">Failed @@FAIL_COUNT@@</button>
        <button class="filter gate-filter" data-status="blocked" aria-pressed="false">Blocked @@BLOCKED_COUNT@@</button>
        <button class="filter gate-filter" data-status="pass" aria-pressed="false">Passed @@PASS_COUNT@@</button>
      </div>
    </div>
    <div class="table-shell">@@GATE_TABLE@@</div>
  </section>

  @@FAILURES_HTML@@
  <section class="section" aria-labelledby="details-title">
    <div class="section-heading">
      <div><p class="kicker">Candidate context</p><h2 id="details-title">Design details</h2></div>
      <p class="section-intro">These values identify the exact candidate and evidence snapshot reviewed above. They are context, not proof of release readiness.</p>
    </div>
    <div class="detail-grid">@@DETAIL_CARDS@@</div>
  </section>
  <footer class="footer">hw-codesign evidence snapshot · bundle @@BUNDLE_HASH@@ · generated @@GENERATED_AT@@</footer>
</main>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script>
(() => {
  const body = document.body;
  const project = body.dataset.project;
  const hash = body.dataset.bundleHash;
  const storageKey = `hw-review:${hash}`;
  const cards = [...document.querySelectorAll('.action-card')];
  const toast = document.getElementById('toast');
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch (_) { saved = {}; }

  const announce = (message) => {
    toast.textContent = message;
    toast.classList.add('show');
    window.clearTimeout(announce.timer);
    announce.timer = window.setTimeout(() => toast.classList.remove('show'), 2400);
  };
  const persist = () => {
    const state = {};
    cards.forEach(card => {
      state[card.dataset.taskId] = {
        selected: card.querySelector('.task-check').checked,
        note: card.querySelector('.task-note').value,
        choice: card.querySelector('.decision-choice:checked')?.value || ''
      };
    });
    try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {}
  };
  const updateCount = () => {
    const selected = cards.filter(card => card.querySelector('.task-check').checked).length;
    const count = document.getElementById('selection-count');
    if (count) count.textContent = `${selected} of ${cards.length} blockers selected`;
  };
  cards.forEach(card => {
    const task = saved[card.dataset.taskId];
    if (task) {
      card.querySelector('.task-check').checked = task.selected !== false;
      card.querySelector('.task-note').value = task.note || '';
      const savedChoice = [...card.querySelectorAll('.decision-choice')].find(input => input.value === task.choice);
      if (savedChoice) savedChoice.checked = true;
    }
    card.querySelector('.task-check').addEventListener('change', () => { persist(); updateCount(); });
    card.querySelector('.task-note').addEventListener('input', persist);
    card.querySelectorAll('.decision-choice').forEach(input => input.addEventListener('change', persist));
  });
  updateCount();

  const selectedTasks = () => cards.filter(card => card.querySelector('.task-check').checked).map(card => ({
    type: card.dataset.kind,
    title: card.dataset.title,
    status: card.dataset.status,
    summary: card.dataset.summary,
    next: card.dataset.next,
    note: card.querySelector('.task-note').value.trim(),
    choice: card.querySelector('.decision-choice:checked')?.value || ''
  }));
  const workflowText = () => {
    const tasks = selectedTasks();
    const list = tasks.map((task, i) => {
      const note = task.note ? `\n   Reviewer context: ${task.note}` : '';
      const choice = task.type === 'decision' ? `\n   Reviewer choice: ${task.choice || 'Not selected — ask before proceeding'}` : '';
      return `${i + 1}. [${task.status.toUpperCase()} / ${task.type}] ${task.title}\n   Evidence: ${task.summary}\n   Next move: ${task.next}${choice}${note}`;
    }).join('\n');
    return `Use the hw-codesign MCP tools to resolve the selected blockers for project "${project}".\n\nSelected scope:\n${list || '(No blockers selected.)'}\n\nWorkflow contract:\n- Open the project and confirm this evidence snapshot (bundle ${hash.slice(0, 12)}) is still current.\n- Generate a repair plan before changing files with hw_generate_repair_plan.\n- Apply only safe, scoped repairs. Use hw_apply_repair_plan with approved=false unless I explicitly approve a proposal.\n- Never resolve an assumption, approve physical evidence, or waive a safety-critical requirement without asking me.\n- Run hw_run_all_checks with include_external=true after changes.\n- If all checks pass, run hw_check_release_gate; do not infer release eligibility from this report.\n- Export a fresh review bundle and summarize what changed, what passed, and what still needs me.\n`;
  };
  const copyText = async (text, success) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (_) {
      const area = document.createElement('textarea');
      area.value = text; area.style.position = 'fixed'; area.style.opacity = '0';
      document.body.appendChild(area); area.select(); document.execCommand('copy'); area.remove();
    }
    announce(success);
  };
  document.getElementById('copy-workflow')?.addEventListener('click', () => copyText(workflowText(), 'Agent workflow copied'));
  document.getElementById('copy-recheck')?.addEventListener('click', () => copyText(`hw --root . check ${project} && hw --root . export-review ${project}`, 'Re-check command copied'));
  document.getElementById('download-brief')?.addEventListener('click', () => {
    const fence = String.fromCharCode(96).repeat(3);
    const markdown = `# Resolution brief: ${project}\n\nBundle: ${hash}\n\n${fence}text\n${workflowText()}\n${fence}\n`;
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([markdown], {type: 'text/markdown'}));
    link.download = `${project}-resolution-brief.md`;
    link.click(); URL.revokeObjectURL(link.href);
    announce('Resolution brief downloaded');
  });
  document.querySelectorAll('.action-filter').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.action-filter').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    cards.forEach(card => card.classList.toggle('hidden', button.dataset.kind !== 'all' && card.dataset.kind !== button.dataset.kind));
  }));

  let gateStatus = 'all';
  const filterGates = () => {
    const term = (document.getElementById('gate-search')?.value || '').toLowerCase();
    document.querySelectorAll('.gate-row').forEach(row => {
      const statusMatch = gateStatus === 'all' || row.dataset.status === gateStatus;
      row.hidden = !(statusMatch && row.textContent.toLowerCase().includes(term));
    });
  };
  document.querySelectorAll('.gate-filter').forEach(button => button.addEventListener('click', () => {
    gateStatus = button.dataset.status;
    document.querySelectorAll('.gate-filter').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterGates();
  }));
  document.getElementById('gate-search')?.addEventListener('input', filterGates);
})();
</script>
</body>
</html>
"""


def _status_badge(status: str) -> str:
    safe_status = escape(status or "other")
    label = escape(_STATUS_LABEL.get(status, status or "Unknown"))
    return f'<span class="status {safe_status}">{label}</span>'


def _plain_gate_meaning(report: dict[str, Any]) -> str:
    status = str(report.get("status", "other"))
    failures = report.get("failures", [])
    if status == "pass":
        if failures:
            return "The check passed, with advisory observations retained below."
        return "The available evidence satisfied this check."
    if status == "fail":
        return "The check ran and found a design, source, or evidence problem that must be corrected."
    if status == "blocked":
        return "No result was reached because a required tool, input, prior check, or evidence record is missing."
    return "Review the technical evidence before using this result."


def _action_kind(report: dict[str, Any]) -> tuple[str, str]:
    failures = report.get("failures", [])
    codes = {str(item.get("code", "")) for item in failures}
    categories = {str(item.get("category", "")) for item in failures}
    gate = str(report.get("gate", ""))
    if gate == "physical_qualification" or "physical_evidence_missing" in codes:
        return "evidence", "Test evidence"
    if any(item.get("requires_user_decision") for item in failures) or "unresolved_critical_assumption" in codes:
        return "decision", "Your decision"
    if "TOOL_ERROR" in categories or any("tool" in code or "external_gate" in code for code in codes):
        return "environment", "Toolchain"
    if report.get("status") == "fail":
        return "design", "Design repair"
    return "environment", "Prerequisite"


def _next_move(report: dict[str, Any]) -> str:
    failures = report.get("failures", [])
    codes = {str(item.get("code", "")) for item in failures}
    if "physical_evidence_missing" in codes:
        return "Complete the named bench tests, attach the required records, and approve only evidence you actually reviewed."
    if "unresolved_critical_assumption" in codes or any(item.get("requires_user_decision") for item in failures):
        return "Record the missing decision or evidence with your rationale; do not let an automated repair approve it for you."
    if codes & {"external_gate_not_run", "tool_unavailable", "xtensa_toolchain_unavailable", "tool_timeout"}:
        return "Diagnose or enable the required native toolchain, then run the full external check matrix again."
    if codes & {"supplier_availability_unknown", "supplier_record_missing"}:
        return "Add current supplier evidence or select a qualified alternate, then rerun sourcing checks."
    if codes & {"compile_prerequisite_failed", "gate_not_run", "failed_gate", "missing_export"}:
        return "Fix the upstream failed check first, regenerate the candidate outputs, then rerun this dependent check."
    if "compiled_circuit_contains_errors" in codes:
        return "Inspect the compiler error elements, repair the authored circuit source, and compile again."
    if "missing_required_protection_role" in codes:
        return "Add the required protection circuit block, regenerate the electrical graph, and rerun semantic checks."
    if report.get("status") == "fail":
        return "Generate a repair plan, review the proposed change, apply the scoped fix, and rerun all checks."
    return "Restore the missing prerequisite or evidence, then rerun this check."


def _failure_summary(report: dict[str, Any]) -> str:
    failures = report.get("failures", [])
    if not failures:
        return _plain_gate_meaning(report)
    first = str(failures[0].get("message", "A blocking finding was recorded."))
    extra = len(failures) - 1
    return f"{first} (+{extra} more finding{'s' if extra != 1 else ''})" if extra else first


def _decision_guide(name: str, assumption: dict[str, Any] | None = None) -> dict[str, Any]:
    assumption = assumption or {}
    proposed = str(assumption.get("proposed_value") or assumption.get("value") or "No value proposed")
    confidence = str(assumption.get("confidence") or "unknown")
    reason = str(assumption.get("reason") or "No design rationale was recorded.")
    if name == "rf_antenna_clearance":
        return {
            "decision_question": "Will the final PCB and enclosure preserve the antenna keep-out with no copper, metal, battery, or cable intrusion?",
            "decision_basis": proposed,
            "decision_confidence": confidence,
            "decision_reason": reason,
            "decision_recommendation": "Keep the antenna at the board edge and preserve the full manufacturer-specified keep-out in both PCB copper and nearby enclosure contents.",
            "decision_evidence": "PCB copper-zone review, antenna-to-board-edge placement, and enclosure clearance around the antenna volume.",
            "decision_escalation": "Choose specialist review if the enclosure is metal, a battery or cable must sit near the antenna, the product needs certified RF range, or the reference keep-out cannot be preserved.",
            "decision_options": [
                "Use the recommended antenna keep-out",
                "Change the PCB or enclosure before approval",
                "Request RF specialist review",
            ],
        }
    return {
        "decision_question": f"Can the project safely adopt the proposed basis for {name.replace('_', ' ')}?",
        "decision_basis": proposed,
        "decision_confidence": confidence,
        "decision_reason": reason,
        "decision_recommendation": "Treat the proposed value as a starting point only. Approve it only after matching it to a measurable requirement or reviewed evidence.",
        "decision_evidence": "A requirement, calculation, datasheet limit, test result, or domain-owner confirmation that supports the proposed value.",
        "decision_escalation": "Request specialist review when the confidence is low, the evidence is missing, or the choice affects safety, compliance, thermals, RF, power, or mechanical integrity.",
        "decision_options": [
            "Use the proposed basis after evidence review",
            "Change the requirement or design first",
            "Request specialist review",
        ],
    }


def _action_items(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    assumptions = bundle.get("assumptions") or {}
    assumption_items = {
        str(item.get("name", "")): item
        for item in assumptions.get("unresolved_critical_items", [])
        if isinstance(item, dict) and item.get("name")
    }
    assumption_names = assumptions.get("unresolved_critical_names", []) or list(assumption_items)
    for name in assumption_names:
        metadata = assumption_items.get(str(name), {})
        guide = _decision_guide(str(name), metadata)
        items.append(
            {
                "kind": "decision",
                "label": "Your decision",
                "status": "blocked",
                "title": f"Resolve assumption: {name}",
                "summary": guide["decision_reason"],
                "next": "Choose a guided option below. The agent must ask before recording any approval.",
                **guide,
            }
        )
    requirements = bundle.get("requirements") or {}
    for requirement in requirements.get("active_unresolved", []):
        req_id = str(requirement.get("id", "Unresolved requirement"))
        source = str(requirement.get("source", "The requirement needs clarification."))
        items.append(
            {
                "kind": "decision",
                "label": "Requirement",
                "status": "blocked",
                "title": f"Clarify requirement: {req_id}",
                "summary": source,
                "next": "Choose how to clarify the requirement. The agent must not invent an acceptance criterion.",
                "decision_question": f"What measurable outcome should requirement {req_id} guarantee?",
                "decision_basis": str(requirement.get("reason") or "No measurable acceptance criterion recorded"),
                "decision_confidence": "unknown",
                "decision_reason": source,
                "decision_recommendation": "Define a numeric limit, operating condition, or pass/fail test before changing the design.",
                "decision_evidence": "Requirement-owner confirmation plus a measurable acceptance criterion and affected validation gate.",
                "decision_escalation": "Request specialist review if the requirement concerns safety, certification, RF, thermal limits, power integrity, or mechanical loading.",
                "decision_options": [
                    "Define a measurable acceptance criterion",
                    "Change or remove the requirement with rationale",
                    "Request specialist review",
                ],
            }
        )

    reports = [report for report in bundle.get("gate_reports", []) if report.get("status") in {"fail", "blocked"}]
    root_entries = (bundle.get("root_cause_analysis") or {}).get("top_root_causes", [])
    failed_gates = {str(report.get("gate", "")) for report in reports if report.get("status") == "fail"}
    downstream_codes = {
        "compile_prerequisite_failed",
        "gate_not_run",
        "failed_gate",
        "missing_export",
        "compiled_electronics_backend_required",
    }
    if root_entries:
        chosen = [
            {
                "gate": entry.get("gate"),
                "status": entry.get("status"),
                "failures": entry.get("failures", []),
                "root_cause": True,
                "affected_gates": entry.get("affected_gates", []),
                "repair_order": entry.get("repair_order"),
            }
            for entry in root_entries
        ]
        chosen_gates = {str(report.get("gate", "")) for report in chosen}
        chosen.extend(
            report
            for report in reports
            if _action_kind(report)[0] in {"decision", "evidence"}
            and str(report.get("gate", "")) not in {"release", "design_dependency_graph"}
            and str(report.get("gate", "")) not in chosen_gates
        )
    else:
        direct = []
        for report in reports:
            gate = str(report.get("gate", ""))
            codes = {str(failure.get("code", "")) for failure in report.get("failures", [])}
            if gate in {"release", "design_dependency_graph"}:
                continue
            if report.get("status") == "blocked" and codes and codes <= downstream_codes:
                continue
            if gate == "supplier_availability" and failed_gates & {"sourcing", "component_provenance"}:
                continue
            direct.append(report)
        chosen = direct or reports
    external_skips = [
        report
        for report in chosen
        if report.get("status") == "blocked"
        and {str(failure.get("code", "")) for failure in report.get("failures", [])} == {"external_gate_not_run"}
    ]
    if external_skips:
        gate_names = ", ".join(str(report.get("gate", "")).replace("_", " ") for report in external_skips)
        items.append(
            {
                "kind": "environment",
                "label": "Toolchain",
                "status": "blocked",
                "title": "Run the native toolchain checks",
                "summary": f"{len(external_skips)} checks were skipped because external tools were not requested: {gate_names}.",
                "next": "Run full validation with external tools enabled. If a check remains blocked, diagnose that specific tool.",
            }
        )
    for report in chosen:
        if report in external_skips:
            continue
        kind, label = _action_kind(report)
        item: dict[str, Any] = {
            "kind": kind,
            "label": label,
            "status": str(report.get("status", "blocked")),
            "title": str(report.get("gate", "Unknown check")).replace("_", " "),
            "summary": _failure_summary(report),
            "next": _next_move(report),
        }
        if report.get("root_cause"):
            affected = report.get("affected_gates", [])
            item["label"] = f"Root cause #{report.get('repair_order', '?')}"
            if affected:
                item["summary"] = (
                    f"{item['summary']} This root cause affects {len(affected)} downstream gates: {', '.join(str(gate) for gate in affected[:6])}."
                )
        if kind == "decision":
            item.update(_decision_guide(str(report.get("gate", "gate decision"))))
        items.append(item)
    priority = {"decision": 0, "evidence": 1, "design": 2, "environment": 3}
    return sorted(items, key=lambda item: (priority.get(item["kind"], 9), item["title"]))


def _decision_guide_html(item: dict[str, Any], task_id: str) -> str:
    if item.get("kind") != "decision":
        return ""
    options = []
    for option_index, option in enumerate(item.get("decision_options", [])):
        recommended = '<span class="recommended-tag">Recommended</span>' if option_index == 0 else ""
        options.append(
            f'<label class="decision-option"><input class="decision-choice" type="radio" name="decision-{escape(task_id, quote=True)}" value="{escape(str(option), quote=True)}"><span>{escape(str(option))}</span>{recommended}</label>'
        )
    return f"""<div class="decision-guide">
  <div class="decision-guide-grid">
    <div class="decision-guide-block"><span>Decision to make</span><strong>{escape(str(item.get("decision_question", "Review this decision.")))}</strong></div>
    <div class="decision-guide-block"><span>System proposal <span class="confidence">{escape(str(item.get("decision_confidence", "unknown")))} confidence</span></span><p>{escape(str(item.get("decision_basis", "No value proposed")))}</p><p class="decision-rationale">{escape(str(item.get("decision_reason", "No design rationale was recorded.")))}</p></div>
    <div class="decision-guide-block"><span>Recommended starting point</span><p>{escape(str(item.get("decision_recommendation", "Review the available evidence before approval.")))}</p></div>
    <div class="decision-guide-block"><span>Evidence to check</span><p>{escape(str(item.get("decision_evidence", "Reviewed engineering evidence.")))}</p></div>
    <div class="decision-guide-block"><span>When to involve an expert</span><p>{escape(str(item.get("decision_escalation", "Escalate when evidence is incomplete or the impact is safety-critical.")))}</p></div>
  </div>
  <fieldset class="decision-options"><legend>Choose how to proceed — no option is applied automatically</legend>{"".join(options)}</fieldset>
</div>"""


def _action_cards_html(items: list[dict[str, Any]]) -> str:
    cards = []
    for index, item in enumerate(items, 1):
        task_id = f"task-{index}"
        attrs = " ".join(
            f'data-{name}="{escape(str(item[key]), quote=True)}"'
            for name, key in (("kind", "kind"), ("title", "title"), ("status", "status"), ("summary", "summary"), ("next", "next"))
        )
        guide_html = _decision_guide_html(item, task_id)
        cards.append(f"""<article class="action-card" data-task-id="{task_id}" {attrs}>
  <input class="task-check" type="checkbox" checked aria-label="Include {escape(item["title"], quote=True)} in resolution workflow">
  <div><span class="task-type">{escape(item["label"])} · {escape(item["status"])}</span>
    <h3 class="task-title">{escape(item["title"])}</h3><p class="task-summary">{escape(item["summary"])}</p></div>
  <div class="action-control"><p class="task-next"><strong>Next:</strong> {escape(item["next"])}</p>
    <textarea class="task-note" aria-label="Context for {escape(item["title"], quote=True)}" placeholder="Optional context, constraint, or evidence note…"></textarea></div>{guide_html}
</article>""")
    return "".join(cards)


def _action_toolbar(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    kinds = {item["kind"] for item in items}
    buttons = ['<button class="filter action-filter" data-kind="all" aria-pressed="true">All</button>']
    for kind, label in (("decision", "Decisions"), ("design", "Design"), ("environment", "Toolchain"), ("evidence", "Evidence")):
        if kind in kinds:
            buttons.append(f'<button class="filter action-filter" data-kind="{kind}" aria-pressed="false">{label}</button>')
    return f"""<div class="toolbar"><span id="selection-count" class="selection-count"></span>
  <div class="filter-group" aria-label="Filter blockers">{"".join(buttons)}</div>
  <button id="copy-workflow" class="button small primary">Copy agent workflow</button>
  <button id="download-brief" class="button small">Download brief</button>
  <button id="copy-recheck" class="button small">Copy re-check command</button>
</div>"""


def _gate_table(gate_reports: list[dict[str, Any]]) -> str:
    rows = []
    for report in gate_reports:
        status = str(report.get("status", "other"))
        metrics = report.get("metrics", {})
        preview = " · ".join(f"{key}: {value}" for key, value in list(metrics.items())[:2]) or "—"
        rows.append(
            f'<tr class="gate-row" data-status="{escape(status, quote=True)}"><td class="gate-name">{escape(str(report.get("gate", "")))}</td>'
            f'<td>{_status_badge(status)}</td><td class="plain-meaning">{escape(_plain_gate_meaning(report))}</td>'
            f'<td>{len(report.get("failures", []))}</td><td class="metric-preview">{escape(preview)}</td></tr>'
        )
    return f"""<table><thead><tr><th>Check</th><th>Result</th><th>What it means</th><th>Findings</th><th>Evidence sample</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>"""


def _failures_html(gate_reports: list[dict[str, Any]]) -> str:
    reports = [report for report in gate_reports if report.get("failures")]
    if not reports:
        return ""
    groups = []
    for report in reports:
        findings = []
        for finding in report.get("failures", []):
            details = finding.get("details")
            details_html = f"<pre>{escape(json.dumps(details, indent=2, sort_keys=True))}</pre>" if details else ""
            path_html = f'<div class="finding-path">path · {escape(str(finding["path"]))}</div>' if finding.get("path") else ""
            findings.append(f"""<div class="finding"><span class="finding-code">{escape(str(finding.get("severity", "error")))} / {escape(str(finding.get("code", "finding")))}</span>
<p>{escape(str(finding.get("message", "")))}</p>{path_html}{details_html}</div>""")
        groups.append(
            f"""<details class="tech"><summary>{_status_badge(str(report.get("status", "other")))} <span class="gate-name">{escape(str(report.get("gate", "")))}</span><span>{len(findings)} finding{"s" if len(findings) != 1 else ""}</span></summary>{"".join(findings)}</details>"""
        )
    return f"""<section class="section" aria-labelledby="evidence-title"><div class="section-heading"><div><p class="kicker">Raw evidence</p><h2 id="evidence-title">Technical findings</h2></div><p class="section-intro">Use this section when repairing or auditing the candidate. Messages and paths are preserved from the gate reports.</p></div><div class="technical-list">{"".join(groups)}</div></section>"""


def _three_d_html(preview: dict[str, Any] | None, vrml_payload: str | None = None) -> str:
    if not preview:
        return ""
    status = str(preview.get("status", "unavailable"))
    source = escape(str(preview.get("source", "3D-model source not recorded")))
    note = escape(str(preview.get("note", "")))
    models = preview.get("models", []) if isinstance(preview.get("models"), list) else []
    available = preview.get("available_model_count", sum(1 for model in models if model.get("available")))
    count = preview.get("model_count", len(models))
    fallback_image = preview.get("fallback_image")
    viewer_asset = preview.get("viewer_asset")
    interactive = bool(preview.get("interactive") and vrml_payload and viewer_asset)
    coverage = f"{available} of {count} referenced models available"
    if not fallback_image and not interactive:
        reason = escape(str(preview.get("reason", "Preview assets were not generated")))
        return f"""<section class="section" aria-labelledby="assembly-title"><div class="section-heading"><div><p class="kicker">Visual evidence</p><h2 id="assembly-title">3D Assembly Preview</h2></div><p class="section-intro">A visual preview helps reviewers orient themselves, but it does not replace CAD interference checks or fabrication qualification.</p></div><div class="evidence-card">{_status_badge(status)}<h3>Preview unavailable</h3><p>{reason}</p><p>Source: {source}. {coverage}.</p></div></section>"""
    model_rows = "".join(
        f"<tr><td>{escape(str(model.get('reference', '')))}</td><td>{escape(str(model.get('footprint', '')))}</td><td>{escape(str(model.get('model', '')))}</td><td>{'Available' if model.get('available') else 'Missing'}</td></tr>"
        for model in models
    )
    image_html = f'<img src="{escape(str(fallback_image), quote=True)}" alt="Isometric PCB assembly preview">' if fallback_image else ""
    interactive_html = ""
    if interactive:
        interactive_html = (
            f'<script id="hw-review-vrml" type="application/octet-stream">{escape(vrml_payload)}</script>'
            f'<script src="{escape(str(viewer_asset), quote=True)}"></script>'
            '<script>window.HWReview3D&&window.HWReview3D.mount("hw-review-3d","hw-review-vrml");</script>'
        )
    instruction = (
        "Drag to orbit, scroll to zoom, and double-click to reset."
        if interactive
        else "Static isometric rendering from the native toolchain."
    )
    model_detail = (
        f'<details class="model-table"><summary>Review model coverage</summary><div class="table-shell"><table><thead><tr><th>Ref</th><th>Footprint</th><th>Model</th><th>State</th></tr></thead><tbody>{model_rows}</tbody></table></div></details>'
        if models
        else ""
    )
    return f"""<section class="section" aria-labelledby="assembly-title"><div class="section-heading"><div><p class="kicker">Visual evidence</p><h2 id="assembly-title">3D Assembly Preview</h2></div><p class="section-intro">Use the model to understand the candidate layout. Release still depends on the checks and physical evidence, not the image.</p></div><div class="three-d-grid"><div id="hw-review-3d" class="assembly-viewer">{image_html}</div><aside class="evidence-card">{_status_badge(status)}<h3>What you are seeing</h3><p>{instruction}</p><ul><li>Source: {source}</li><li>{coverage}</li></ul><p>{note}</p>{model_detail}</aside></div>{interactive_html}</section>"""


def _detail_cards(bundle: dict[str, Any]) -> str:
    project = bundle.get("project", {})
    placement = bundle.get("placement") or {}
    component = bundle.get("component_resolution") or {}
    assumptions = bundle.get("assumptions") or {}
    requirements = bundle.get("requirements") or {}
    project_card = f"""<article class="detail-card"><h3>Candidate identity</h3><dl class="detail-list"><dt>Project</dt><dd>{escape(str(project.get("name", "—")))}</dd><dt>Revision</dt><dd>{escape(str(project.get("revision", "—")))}</dd><dt>Backend</dt><dd>{escape(str(project.get("backend", "—")))}</dd><dt>Target use</dt><dd>{escape(str(project.get("target_use", "—")))}</dd></dl></article>"""
    placement_card = f"""<article class="detail-card"><h3>Board and placement</h3><dl class="detail-list"><dt>Board</dt><dd>{escape(str(placement.get("board_width_mm", "—")))} × {escape(str(placement.get("board_height_mm", "—")))} mm</dd><dt>Placements</dt><dd>{escape(str(placement.get("placement_count", "—")))}</dd><dt>Constraints</dt><dd>{escape(str(placement.get("constraint_count", "—")))}</dd><dt>Unenforced kinds</dt><dd>{escape(", ".join(map(str, placement.get("unenforced_constraint_kinds", []))) or "none")}</dd></dl></article>"""
    evidence_card = f"""<article class="detail-card"><h3>Evidence coverage</h3><dl class="detail-list"><dt>Components</dt><dd>{escape(str(component.get("resolved", "—")))} of {escape(str(component.get("requested", "—")))} resolved</dd><dt>Supplier source</dt><dd>{escape(str(component.get("supplier_provider", "—")))}</dd><dt>Critical assumptions</dt><dd>{escape(str(assumptions.get("unresolved_critical", 0)))} unresolved</dd><dt>Requirements</dt><dd>{escape(str(requirements.get("active_unresolved_count", 0)))} unresolved</dd></dl></article>"""
    bundle_card = f"""<article class="detail-card"><h3>Snapshot integrity</h3><dl class="detail-list"><dt>Bundle version</dt><dd>{escape(str(bundle.get("bundle_version", "—")))}</dd><dt>Bundle hash</dt><dd>{escape(str(bundle.get("bundle_hash", "—")))}</dd><dt>Artifacts indexed</dt><dd>{len(bundle.get("artifacts", []))}</dd><dt>Iterations indexed</dt><dd>{len(bundle.get("iterations", []))}</dd></dl></article>"""
    return project_card + placement_card + evidence_card + bundle_card


def _review_state(bundle: dict[str, Any]) -> tuple[str, str, str, str]:
    reports = bundle.get("gate_reports", [])
    summary = bundle.get("summary", {})
    release_report = next((report for report in reports if report.get("gate") == "release"), None)
    if release_report and release_report.get("status") in {"pass", "released"}:
        return "released", "Release gate passed", "This candidate passed the authoritative release gate.", "Release gate passed"
    if summary.get("fail", 0):
        return (
            "fail",
            "Changes required",
            "Do not release or fabricate this candidate yet. One or more checks found design or source problems. Start with the selected repair workflow below.",
            "This candidate needs changes",
        )
    if summary.get("blocked", 0):
        return (
            "blocked",
            "Evidence incomplete",
            "No design failure was reported, but some checks could not finish. Restore the missing tools, inputs, approvals, or physical evidence before release.",
            "This candidate is not fully verified",
        )
    if not summary.get("total", 0):
        return (
            "blocked",
            "Not checked",
            "No gate results are present in this snapshot. Run the validation workflow before making a release or fabrication decision.",
            "This candidate has not been checked",
        )
    return (
        "pass",
        "Ready for final gate",
        "All recorded checks passed. Run the authoritative release gate before treating the candidate as release-eligible.",
        "All recorded checks passed",
    )


def render_html(bundle: dict[str, Any], vrml_payload: str | None = None) -> str:
    project = bundle.get("project", {})
    summary = bundle.get("summary", {})
    gate_reports = bundle.get("gate_reports", [])
    state_class, state_label, lede, headline = _review_state(bundle)
    items = _action_items(bundle)
    empty = (
        ""
        if items
        else '<div class="empty-actions"><strong>No blockers are listed in this snapshot.</strong><p>Run the authoritative release gate before fabrication or release. If the candidate changed after this report was generated, export a fresh report first.</p></div>'
    )
    replacements = {
        "PROJECT_NAME": escape(str(project.get("name", "Unnamed project"))),
        "PROJECT_ATTR": escape(str(project.get("name", "")), quote=True),
        "REVISION": escape(str(project.get("revision", "—"))),
        "BACKEND": escape(str(project.get("backend", "unknown"))),
        "TARGET_USE": escape(str(project.get("target_use", "target use not recorded"))),
        "GENERATED_AT": escape(str(bundle.get("generated_at", "unknown"))),
        "BUNDLE_HASH": escape(str(bundle.get("bundle_hash", ""))),
        "HASH_ATTR": escape(str(bundle.get("bundle_hash", "")), quote=True),
        "HASH_SHORT": escape(str(bundle.get("bundle_hash", ""))[:12] or "no hash"),
        "HEADLINE": escape(headline),
        "LEDE": escape(lede),
        "STATE_CLASS": state_class,
        "STATE_LABEL": escape(state_label),
        "PASS_COUNT": str(summary.get("pass", 0)),
        "BLOCKED_COUNT": str(summary.get("blocked", 0)),
        "FAIL_COUNT": str(summary.get("fail", 0)),
        "TOTAL_COUNT": str(summary.get("total", 0)),
        "ACTION_TOOLBAR": _action_toolbar(items),
        "ACTION_CARDS": _action_cards_html(items),
        "EMPTY_ACTIONS": empty,
        "THREE_D_HTML": _three_d_html(bundle.get("three_d_preview"), vrml_payload),
        "GATE_TABLE": _gate_table(gate_reports),
        "FAILURES_HTML": _failures_html(gate_reports),
        "DETAIL_CARDS": _detail_cards(bundle),
    }
    html = _HTML_TEMPLATE
    for key, value in replacements.items():
        html = html.replace(f"@@{key}@@", value)
    return html


def generate_html_report(bundle_path: Path, output_path: Path | None = None) -> Path:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    if output_path is None:
        output_path = bundle_path.parent / "report.html"
    vrml_payload = _load_vrml_payload(bundle_path.parent, bundle)
    output_path.write_text(render_html(bundle, vrml_payload), encoding="utf-8")
    return output_path


def _load_vrml_payload(review_dir: Path, bundle: dict[str, Any]) -> str | None:
    preview = bundle.get("three_d_preview")
    if not isinstance(preview, dict) or not preview.get("interactive"):
        return None
    asset = preview.get("vrml_asset")
    if not isinstance(asset, str) or Path(asset).is_absolute():
        return None
    candidate = (review_dir / asset).resolve()
    try:
        candidate.relative_to(review_dir.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return base64.b64encode(candidate.read_bytes()).decode("ascii")
