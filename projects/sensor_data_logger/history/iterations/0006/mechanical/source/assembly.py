"""Generated parametric mechanical assembly entrypoint."""
import argparse
import json
from pathlib import Path
from hw_codesign.backends.mechanical import OpenCascadeMechanicalBackend

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--board-step", type=Path)
    args = parser.parse_args()
    contract = json.loads(Path(__file__).with_name("mechanical_contract.json").read_text(encoding="utf-8"))
    report = OpenCascadeMechanicalBackend().generate_from_contract(contract, args.output, board_step=args.board_step)
    print(json.dumps(report.to_dict(), sort_keys=True))
    raise SystemExit(0 if report.status == "pass" else 1)
