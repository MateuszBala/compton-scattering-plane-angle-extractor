#!/bin/bash
# FILE: install.sh
#
# ABOUT: Instaluje zależności projektu i tworzy środowisko wirtualne przy użyciu uv.
#
# ARGUMENTS:
#   (brak) : skrypt nie przyjmuje argumentów.
#
# USAGE:
#   bash scripts/install.sh

set -euo pipefail

# Instaluje zależności na podstawie pyproject.toml.
# Zwraca: kod wyjścia uv (0 = sukces).
function main() {
  uv sync
}

main "$@"
