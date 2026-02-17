import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from .estimator import estimate_from_config
from .pricing import get_default_pricing
from .report import generate_markdown_table


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Failed to parse YAML config: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a mapping/object at the top level")

    return data


def cmd_estimate(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    try:
        config = load_config(config_path)
        pricing_table = get_default_pricing()
        results = estimate_from_config(config, pricing_table=pricing_table)
        markdown = generate_markdown_table(results)
        print(markdown)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tokenscope",
        description="Estimate monthly LLM usage cost across multiple models.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    estimate_parser = subparsers.add_parser(
        "estimate", help="Estimate monthly cost from a config file (YAML)."
    )
    estimate_parser.add_argument(
        "config", help="Path to a YAML config file describing workload tokens."
    )
    estimate_parser.set_defaults(func=cmd_estimate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1

    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())


