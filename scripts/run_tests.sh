#!/bin/bash
# FILE: run_tests.sh
#
# ABOUT: Uruchamia zestaw testów projektu (pytest) w środowisku uv.
#
# ARGUMENTS:
#   $@ : opcjonalne argumenty przekazywane bezpośrednio do pytest.
#
# USAGE:
#   bash scripts/run_tests.sh
#   bash scripts/run_tests.sh tests/unit -k vectors

set -euo pipefail

# Uruchamia pytest z opcjonalnymi argumentami.
# Parametry:
#   PARAM_PYTEST_ARGS : argumenty przekazywane do pytest.
# Zwraca: kod wyjścia pytest (0 = sukces).
function main() {
  local PARAM_PYTEST_ARGS=("$@")
  uv run pytest "${PARAM_PYTEST_ARGS[@]}"
}

main "$@"
