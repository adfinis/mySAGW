#!/bin/sh

set -e

export COVERAGE_FILE="/tmp/.coverage"
export ENV="test"

# Only install deps if not yet done - speeds up local development
pip show pytest-cov 2>/dev/null >/dev/null || pip install --user -r requirements-dev.txt

pytest -n0 \
    caluma/extensions/ \
    --ff \
    -o cache_dir=/tmp/pytest.cache \
    --cov=caluma/extensions/ \
    -vv "$@"
