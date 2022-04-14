#!/bin/sh

set -e

export COVERAGE_FILE="/tmp/.coverage"
export ENV="test"

poetry run pytest -n0 \
    caluma/extensions/ \
    --ff \
    -o cache_dir=/tmp/pytest.cache \
    --cov=caluma/extensions/ \
    -vv "$@"
