from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .errors import HardwarePlatformError
from .service import HardwareService


def _emit(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hw", description="Agentic hardware design CLI")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Platform repository root")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create-project")
    create.add_argument("name")
    create.add_argument("--template", default="robotics_controller_full")
    read = commands.add_parser("read-spec")
    read.add_argument("project")
    requirements = commands.add_parser("update-requirements")
    requirements.add_argument("project")
    requirements.add_argument("requirements_text")
    validate = commands.add_parser("validate-spec")
    validate.add_argument("project")
    generate = commands.add_parser("generate")
    generate.add_argument("project")
    for name in ("generate-reference-intent", "generate-electronics-source", "generate-mechanical-source", "generate-firmware-source"):
        command = commands.add_parser(name)
        command.add_argument("project")
    design_candidate = commands.add_parser("design-candidate")
    design_candidate.add_argument("project")
    design_candidate.add_argument("--brief", default=None, help="Natural-language hardware requirements to lower before designing")
    design_candidate.add_argument("--external", action="store_true", help="Include native toolchain-dependent gates")
    design_candidate.add_argument("--no-review-bundle", action="store_true", help="Skip review bundle generation")
    design_space = commands.add_parser("design-space")
    design_space.add_argument("project")
    design_space.add_argument("--max-candidates", type=int, default=8, help="Maximum ranked alternatives to return")
    grounding = commands.add_parser("grounding-benchmark")
    grounding.add_argument("project")
    physical_plan = commands.add_parser("physical-qualification-plan")
    physical_plan.add_argument("project")
    physical_evidence = commands.add_parser("record-physical-evidence")
    physical_evidence.add_argument("project")
    physical_evidence.add_argument("--evidence", required=True, help="JSON evidence record with test_id, status, summary, and optional evidence_files")
    physical_evidence.add_argument("--approved", action="store_true", help="Mark this physical evidence record as approved")
    check = commands.add_parser("check")
    check.add_argument("project")
    check.add_argument("--no-external", action="store_true")
    iteration = commands.add_parser("iterate")
    iteration.add_argument("project")
    iteration.add_argument("--no-external", action="store_true")
    design = commands.add_parser("design-until-release")
    design.add_argument("project")
    design.add_argument("--max-iterations", type=int, default=8)
    design.add_argument("--external", action="store_true")
    release = commands.add_parser("release-gate")
    release.add_argument("project")
    report = commands.add_parser("design-report")
    report.add_argument("project")
    export_review = commands.add_parser("export-review")
    export_review.add_argument("project")
    export_standalone = commands.add_parser("export-standalone-review")
    export_standalone.add_argument("project")
    serve = commands.add_parser("serve-review")
    serve.add_argument("project")
    serve.add_argument("--port", type=int, default=7474)
    serve.add_argument("--no-open", action="store_true", help="Do not open a browser tab automatically")
    dashboard = commands.add_parser("serve-dashboard")
    dashboard.add_argument("--port", type=int, default=7475)
    dashboard.add_argument("--no-open", action="store_true")
    upload = commands.add_parser("upload-review")
    upload.add_argument("project")
    upload.add_argument("--destination", default=None, help="Hosted viewer endpoint URL")
    receiver = commands.add_parser("serve-receiver")
    receiver.add_argument("--port", type=int, default=7476)
    receiver.add_argument("--inbox-dir", default=None, help="Directory to store received bundles")
    receiver.add_argument("--no-open", action="store_true")
    commands.add_parser("list-projects")
    add_comment = commands.add_parser("add-review-comment")
    add_comment.add_argument("project")
    add_comment.add_argument("text")
    add_comment.add_argument("--author", default=None)
    add_comment.add_argument("--target-type", default="general", choices=["general", "gate_failure", "requirement", "component"])
    add_comment.add_argument("--target-id", default=None)
    add_comment.add_argument("--gate", default=None)
    commands.add_parser("list-review-comments").add_argument("project")
    commands.add_parser("list-candidates").add_argument("project")
    get_cand = commands.add_parser("get-candidate")
    get_cand.add_argument("project")
    get_cand.add_argument("candidate_id")
    review_cand = commands.add_parser("review-candidate")
    review_cand.add_argument("project")
    review_cand.add_argument("candidate_id")
    cmp_cand = commands.add_parser("compare-candidates")
    cmp_cand.add_argument("project")
    cmp_cand.add_argument("candidate_a")
    cmp_cand.add_argument("candidate_b")
    fab_review = commands.add_parser("prepare-fabrication-review")
    fab_review.add_argument("project")
    fab_review.add_argument("--candidate-id", default=None)
    design_part = commands.add_parser("design-part")
    design_part.add_argument("project")
    design_part.add_argument("--part-name", required=True)
    design_part.add_argument("--part-type", required=True,
                             choices=["pcb_mount_bracket", "standoff_tower", "cable_clip", "din_rail_adapter", "custom_enclosure_variant"])
    design_part.add_argument("--intent", default="{}", help="JSON string of intent parameters")
    commands.add_parser("list-parts").add_argument("project")
    commands.add_parser("get-part-types")
    propose_block = commands.add_parser("propose-circuit-block")
    propose_block.add_argument("category")
    add_block = commands.add_parser("add-circuit-block")
    add_block.add_argument("project")
    add_block.add_argument("--block", default="{}", help="JSON block spec")
    commands.add_parser("list-circuit-blocks").add_argument("project")
    set_constraint = commands.add_parser("set-placement-constraint")
    set_constraint.add_argument("project")
    set_constraint.add_argument("--constraint", default="{}", help="JSON constraint spec")
    commands.add_parser("list-placement-constraints").add_argument("project")
    record_decision = commands.add_parser("record-design-decision")
    record_decision.add_argument("project")
    record_decision.add_argument("--domain", required=True, choices=["electronics", "mechanical", "firmware", "pcb", "sourcing", "system"])
    record_decision.add_argument("--decision", required=True)
    record_decision.add_argument("--rationale", required=True)
    commands.add_parser("check-cross-domain-consistency").add_argument("project")
    diag = commands.add_parser("diagnose-environment")
    diag.add_argument("--target", default="fabrication_release", choices=["fabrication_release", "candidate", "firmware_only", "full_release"])
    diag.add_argument("--backend", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    service = HardwareService(args.root)
    try:
        if args.command == "create-project":
            result = service.create_project(args.name, args.template)
        elif args.command == "read-spec":
            result = {"status": "pass", "spec": service.read_spec(args.project)}
        elif args.command == "update-requirements":
            result = service.update_requirements(args.project, args.requirements_text)
        elif args.command == "validate-spec":
            result = service.validate_spec(args.project)
        elif args.command == "generate":
            result = service.generate_all(args.project)
        elif args.command == "generate-reference-intent":
            result = service.generate_reference_intent(args.project)
        elif args.command == "generate-electronics-source":
            result = service.generate_electronics_source(args.project)
        elif args.command == "generate-mechanical-source":
            result = service.generate_mechanical_source(args.project)
        elif args.command == "generate-firmware-source":
            result = service.generate_firmware_source(args.project)
        elif args.command == "design-candidate":
            result = service.design_candidate(
                args.project,
                include_external=args.external,
                with_review_bundle=not args.no_review_bundle,
                requirements_text=args.brief,
            )
        elif args.command == "design-space":
            result = service.explore_design_space(args.project, max_candidates=args.max_candidates)
        elif args.command == "grounding-benchmark":
            result = service.run_grounding_benchmark(args.project)
        elif args.command == "physical-qualification-plan":
            result = service.generate_physical_qualification_plan(args.project)
        elif args.command == "record-physical-evidence":
            import json as _json
            result = service.record_physical_evidence(args.project, _json.loads(args.evidence), approved=args.approved)
        elif args.command == "check":
            result = service.run_all_checks(args.project, include_external=not args.no_external)
        elif args.command == "iterate":
            result = service.run_design_iteration(args.project, include_external=not args.no_external)
        elif args.command == "design-until-release":
            result = service.design_until_release(args.project, args.max_iterations, include_external=args.external)
        elif args.command == "release-gate":
            result = service.check_release_gate(args.project)
        elif args.command == "design-report":
            result = service.generate_design_report(args.project)
        elif args.command == "export-review":
            result = service.export_review(args.project)
        elif args.command == "export-standalone-review":
            result = service.export_standalone_review(args.project)
        elif args.command == "serve-review":
            from .review_viewer import serve_review
            serve_review(service, args.project, port=args.port, open_browser=not args.no_open)
            return 0
        elif args.command == "serve-dashboard":
            from .review_viewer import serve_dashboard
            serve_dashboard(service, port=args.port, open_browser=not args.no_open)
            return 0
        elif args.command == "upload-review":
            result = service.upload_review(args.project, destination=args.destination)
        elif args.command == "serve-receiver":
            from pathlib import Path as _Path

            from .review_viewer import serve_receiver
            inbox = _Path(args.inbox_dir) if args.inbox_dir else args.root / ".review-inbox"
            serve_receiver(inbox, port=args.port, open_browser=not args.no_open)
            return 0
        elif args.command == "list-projects":
            result = service.list_project_summaries()
        elif args.command == "add-review-comment":
            result = service.add_review_comment(
                args.project, args.text, target_type=args.target_type,
                target_id=args.target_id, author=args.author, gate=args.gate,
            )
        elif args.command == "list-review-comments":
            result = service.list_review_comments(args.project)
        elif args.command == "list-candidates":
            result = service.list_candidates(args.project)
        elif args.command == "get-candidate":
            result = service.get_candidate(args.project, args.candidate_id)
        elif args.command == "review-candidate":
            result = service.review_candidate(args.project, args.candidate_id)
        elif args.command == "compare-candidates":
            result = service.compare_candidates(args.project, args.candidate_a, args.candidate_b)
        elif args.command == "prepare-fabrication-review":
            result = service.prepare_fabrication_review(args.project, args.candidate_id)
        elif args.command == "design-part":
            import json as _json
            result = service.design_part(args.project, args.part_name, args.part_type, _json.loads(args.intent))
        elif args.command == "list-parts":
            result = service.list_parts(args.project)
        elif args.command == "get-part-types":
            result = service.get_part_types()
        elif args.command == "propose-circuit-block":
            result = service.propose_circuit_block(args.category)
        elif args.command == "add-circuit-block":
            import json as _json
            result = service.add_circuit_block(args.project, _json.loads(args.block))
        elif args.command == "list-circuit-blocks":
            result = service.list_circuit_blocks(args.project)
        elif args.command == "set-placement-constraint":
            import json as _json
            result = service.set_placement_constraint(args.project, _json.loads(args.constraint))
        elif args.command == "list-placement-constraints":
            result = service.list_placement_constraints(args.project)
        elif args.command == "record-design-decision":
            result = service.record_design_decision(args.project, args.domain, args.decision, args.rationale)
        elif args.command == "check-cross-domain-consistency":
            result = service.check_cross_domain_consistency(args.project)
        elif args.command == "diagnose-environment":
            result = service.diagnose_environment(args.target, args.backend)
        else:
            raise AssertionError(args.command)
        _emit(result)
        return 0
    except (HardwarePlatformError, FileExistsError, ValueError) as exc:
        _emit({"status": "fail", "error": type(exc).__name__, "message": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
