#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
PYTHON=${PYTHON:-python3.13}
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
"$PYTHON" -m unittest discover -s tests -p 'test_residual_gradient_v18_37.py' -v
"$PYTHON" scripts/frozen_preflight_v18_37.py
"$PYTHON" scripts/original_residual_gradient_v18_37.py "$@"
"$PYTHON" scripts/plot_v18_37.py
"$PYTHON" scripts/build_manifest.py
"$PYTHON" scripts/pack_sendback.py
