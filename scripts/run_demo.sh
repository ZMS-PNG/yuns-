#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=src
python -m mapes.cli --input data/cases/demo_cases.json --output artifacts/demo_report.json
cat artifacts/demo_report.json
