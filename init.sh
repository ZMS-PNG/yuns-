#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
python --version
python - <<'PY'
import sys
print('Python executable:', sys.executable)
PY
