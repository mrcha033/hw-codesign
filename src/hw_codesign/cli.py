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
    parser = argparse.ArgumentParser(prog="hw", description="Agent-native hardware co-design CLI")
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
    serve = commands.add_parser("serve-review")
    serve.add_argument("project")
    serve.add_argument("--port", type=int, default=7474)
    serve.add_argument("--no-open", action="store_true", help="Do not open a browser tab automatically")
    upload = commands.add_parser("upload-review")
    upload.add_argument("project")
    upload.add_argument("--destination", default=None, help="Hosted viewer endpoint URL")
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
        elif args.command == "serve-review":
            from .review_viewer import serve_review
            serve_review(service, args.project, port=args.port, open_browser=not args.no_open)
            return 0
        elif args.command == "upload-review":
            result = service.upload_review(args.project, destination=args.destination)
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
