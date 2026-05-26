from __future__ import annotations

import argparse

from .pipeline import evaluate_file


def main() -> None:
    parser = argparse.ArgumentParser(description="MAPES evaluator CLI")
    parser.add_argument("--input", required=True, help="Path to evaluation case JSON")
    parser.add_argument("--output", required=True, help="Path to output report JSON")
    args = parser.parse_args()
    reports = evaluate_file(args.input, args.output)
    print(f"Generated {len(reports)} report(s) -> {args.output}")


if __name__ == "__main__":
    main()
