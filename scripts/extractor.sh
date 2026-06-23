#!/bin/bash
# FILE: extractor.sh
#
# ABOUT: Uruchamia narzędzie wyliczające kąty rozpraszania Comptonowskiego,
#        przekazując argumenty do modułu Pythona pakietu w środowisku uv.
#
# ARGUMENTS:
#   $@ : argumenty przekazywane bezpośrednio do interfejsu CLI
#        (pełna lista: bash scripts/extractor.sh --help).
#
# USAGE:
#   bash scripts/extractor.sh \
#     --input-file-path <plik> \
#     --output-dir-path <katalog> \
#     --first-scattering-initial-direction x,y,z \
#     --first-scattering-final-direction x,y,z \
#     --second-scattering-initial-direction x,y,z \
#     --second-scattering-final-direction x,y,z \
#     [--output-file-name NAZWA] [--output-format csv|hdf5] [--rad2deg]

set -euo pipefail

# Nazwa modułu Pythona uruchamianego jako interfejs CLI.
PYTHON_MODULE="compton_scattering_plane_angle_extractor"

# Uruchamia interfejs CLI pakietu, przekazując otrzymane argumenty.
# Parametry:
#   PARAM_ARGS : argumenty przekazywane do interfejsu CLI.
# Zwraca: kod wyjścia interfejsu CLI.
function main() {
  local PARAM_ARGS=("$@")
  uv run python -m "${PYTHON_MODULE}" "${PARAM_ARGS[@]}"
}

main "$@"
