#!/bin/bash
# FILE: run_csv_file_analysis_extra_columns.sh
#
# ABOUT: Przykład pokazujący, że wczytywane są wyłącznie wskazane kolumny.
#        Plik wejściowy zawiera dodatkowe kolumny (event_id, energy_keV,
#        detector, weight), które są ignorowane. Wynik jest identyczny z
#        wynikiem skryptu run_csv_file_analysis.sh (te same wektory pędu).
#
# ARGUMENTS:
#   (brak) : skrypt nie przyjmuje argumentów.
#
# USAGE:
#   bash examples/run_csv_file_analysis_extra_columns.sh

set -euo pipefail

# Katalog tego skryptu oraz katalog główny repozytorium.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Ścieżki danych wejściowych i wyników.
INPUT_FILE="${SCRIPT_DIR}/data/example_scattering_extra_columns.csv"
OUTPUT_DIR="${SCRIPT_DIR}/output"

# Uruchamia narzędzie na danych z dodatkowymi kolumnami (kąty w stopniach),
# zapisując wynik pod osobną nazwą, aby umożliwić porównanie.
# Zwraca: kod wyjścia interfejsu CLI.
function main() {
  bash "${REPO_ROOT}/scripts/extractor.sh" \
    --input-file-path "${INPUT_FILE}" \
    --output-dir-path "${OUTPUT_DIR}" \
    --output-file-name compton-scattering-plane-angles-extra-columns.csv \
    --first-scattering-initial-direction a0x,a0y,a0z \
    --first-scattering-final-direction a1x,a1y,a1z \
    --second-scattering-initial-direction b0x,b0y,b0z \
    --second-scattering-final-direction b1x,b1y,b1z \
    --rad2deg
}

main "$@"
