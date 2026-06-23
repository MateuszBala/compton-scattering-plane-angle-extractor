#!/bin/bash
# FILE: extractor.sh
#
# ABOUT: Uruchamia narzędzie wyliczające kąty rozpraszania Comptonowskiego,
#        przekazując argumenty do interfejsu CLI pakietu. Skrypt sam wybiera
#        dostępne środowisko uruchomieniowe (nie wymaga aktywacji venv).
#
# ARGUMENTS:
#   $@ : argumenty przekazywane bezpośrednio do interfejsu CLI
#        (pełna lista: bash scripts/extractor.sh --help).
#
# ENVIRONMENT:
#   CSPAE_PYTHON   : interpreter Pythona wymuszony do uruchomienia (opcjonalny).
#   CSPAE_VENV_DIR : katalog środowiska wirtualnego utworzonego przez install.sh
#                    (domyślnie ${CSPAE_HOME:-$HOME/.local/share/cspae}/venv).
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

# Katalog główny repozytorium oraz katalog środowiska wirtualnego użytkownika.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${CSPAE_VENV_DIR:-${CSPAE_HOME:-${HOME}/.local/share/cspae}/venv}"

# Sprawdza, czy podany interpreter potrafi zaimportować pakiet narzędzia.
# Parametry:
#   PARAM_PYTHON : ścieżka interpretera Pythona.
# Zwraca: 0, gdy pakiet jest dostępny; w przeciwnym razie wartość niezerową.
function can_import() {
  local PARAM_PYTHON="$1"
  "${PARAM_PYTHON}" -c \
    'import importlib.util, sys; sys.exit(importlib.util.find_spec(sys.argv[1]) is None)' \
    "${PYTHON_MODULE}" >/dev/null 2>&1
}

# Wybiera środowisko uruchomieniowe i wykonuje interfejs CLI z argumentami.
# Kolejność: CSPAE_PYTHON -> venv z install.sh -> bieżący python3 (jeśli ma
# pakiet) -> uv (tryb developerski). Brak środowiska kończy się błędem.
# Zwraca: kod wyjścia interfejsu CLI lub 1, gdy nie znaleziono środowiska.
function main() {
  if [[ -n "${CSPAE_PYTHON:-}" ]]; then
    exec "${CSPAE_PYTHON}" -m "${PYTHON_MODULE}" "$@"
  fi
  if [[ -x "${VENV_DIR}/bin/python" ]] && can_import "${VENV_DIR}/bin/python"; then
    exec "${VENV_DIR}/bin/python" -m "${PYTHON_MODULE}" "$@"
  fi
  if command -v python3 >/dev/null 2>&1 && can_import python3; then
    exec python3 -m "${PYTHON_MODULE}" "$@"
  fi
  if command -v uv >/dev/null 2>&1; then
    exec uv run --project "${REPO_ROOT}" python -m "${PYTHON_MODULE}" "$@"
  fi
  echo "Błąd: nie znaleziono środowiska z zainstalowanym narzędziem." >&2
  echo "Zainstaluj je najpierw: bash scripts/install.sh" >&2
  echo "(albo wskaż interpreter zmienną CSPAE_PYTHON lub venv zmienną CSPAE_VENV_DIR)." >&2
  exit 1
}

main "$@"
