#!/bin/bash
# FILE: run_hdf5_file_analysis.sh
#
# ABOUT: Przykład użycia dla pliku HDF5: wylicza kąty rozpraszania dla dołączonego
#        pliku HDF5 i zapisuje wynik do katalogu examples/output. Format wyjścia
#        jest domyślnie taki sam jak wejścia (HDF5).
#
# ARGUMENTS:
#   (brak) : skrypt nie przyjmuje argumentów.
#
# USAGE:
#   bash examples/run_hdf5_file_analysis.sh

set -euo pipefail

# Katalog tego skryptu oraz katalog główny repozytorium.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Ścieżki danych wejściowych i wyników.
INPUT_FILE="${SCRIPT_DIR}/data/example_scattering.h5"
OUTPUT_DIR="${SCRIPT_DIR}/output"

# Uruchamia narzędzie na przykładowych danych HDF5 (kąty w stopniach).
# Zwraca: kod wyjścia interfejsu CLI.
function main() {
  bash "${REPO_ROOT}/scripts/extractor.sh" \
    --input-file-path "${INPUT_FILE}" \
    --output-dir-path "${OUTPUT_DIR}" \
    --first-scattering-initial-direction a0x,a0y,a0z \
    --first-scattering-final-direction a1x,a1y,a1z \
    --second-scattering-initial-direction b0x,b0y,b0z \
    --second-scattering-final-direction b1x,b1y,b1z \
    --rad2deg
}

main "$@"
