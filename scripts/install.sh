#!/bin/bash
# FILE: install.sh
#
# ABOUT: Instaluje narzędzie dla użytkownika końcowego w izolowanym środowisku
#        wirtualnym Pythona (venv). Nie modyfikuje globalnego Pythona ani jego
#        pakietów i nie wymaga narzędzia uv. Wymaga jedynie interpretera Pythona
#        w wersji >= 3.11.
#
# ARGUMENTS:
#   (brak) : skrypt konfigurowany jest zmiennymi środowiskowymi.
#
# ENVIRONMENT:
#   PYTHON          : interpreter Pythona do utworzenia venv (domyślnie python3).
#   CSPAE_VENV_DIR  : katalog środowiska wirtualnego (domyślnie
#                     ${CSPAE_HOME:-$HOME/.local/share/cspae}/venv).
#
# USAGE:
#   bash scripts/install.sh
#   PYTHON=python3.11 bash scripts/install.sh
#   CSPAE_VENV_DIR=/scratch/$USER/cspae-venv bash scripts/install.sh

set -euo pipefail

# Katalog główny repozytorium (na podstawie położenia skryptu).
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Interpreter Pythona oraz katalog środowiska wirtualnego.
PYTHON_BIN="${PYTHON:-python3}"
VENV_DIR="${CSPAE_VENV_DIR:-${CSPAE_HOME:-${HOME}/.local/share/cspae}/venv}"

# Sprawdza, że wskazany interpreter istnieje i ma wymaganą wersję (>= 3.11).
# Zwraca: kończy z kodem 1, gdy warunek nie jest spełniony.
function check_python() {
  if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "Błąd: nie znaleziono interpretera Pythona: ${PYTHON_BIN}." >&2
    echo "Wskaż go zmienną PYTHON, np. PYTHON=python3.11 bash scripts/install.sh." >&2
    exit 1
  fi
  if ! "${PYTHON_BIN}" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 11) else 1)'; then
    echo "Błąd: wymagany Python >= 3.11 (znaleziono: $("${PYTHON_BIN}" -V 2>&1))." >&2
    exit 1
  fi
}

# Tworzy środowisko wirtualne i instaluje pakiet wraz z zależnościami.
# Zwraca: kod wyjścia komend instalacji (0 = sukces).
function main() {
  check_python
  echo "Tworzę środowisko wirtualne w: ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/python" -m pip install --upgrade pip
  "${VENV_DIR}/bin/python" -m pip install "${REPO_ROOT}"
  echo "Zainstalowano narzędzie w środowisku: ${VENV_DIR}"
  echo "Uruchom narzędzie poleceniem: bash scripts/extractor.sh --help"
}

main "$@"
