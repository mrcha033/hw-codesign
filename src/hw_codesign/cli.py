from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    service = HardwareService(args.root)
    try:
        if args.command == "create-project":
            result = service.create_project(args.name, args.template)
        elif args.command == "read-spec":
            result = service.read_spec(args.project)
        elif args.command == "update-requirements":
            result = service.update_requirements(args.project, args.requirements_text)
        elif args.command == "validate-spec":
            result = service.validate_spec(args.project)
        elif args.command == "generate":
            result = service.generate_all(args.project)
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
        else:
            raise AssertionError(args.command)
        _emit(result)
        return 0
    except (HardwarePlatformError, FileExistsError, ValueError) as exc:
        _emit({"status": "error", "error": type(exc).__name__, "message": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
