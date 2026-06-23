"""Interfejs linii komend pakietu.

Moduł definiuje punkt wejścia uruchamiany przez ``python -m
compton_scattering_plane_angle_extractor`` oraz skrypty konsolowe
``compton-scattering-plane-angle-extractor`` i ``cspae``.

Funkcje publiczne
-----------------
build_parser() -> argparse.ArgumentParser
    Buduje parser argumentów wiersza poleceń.
main(argv: list[str] | None = None) -> int
    Parsuje argumenty, uruchamia potok obliczeń i zwraca kod wyjścia.
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

from .column_spec import parse_column_spec
from .config import RunConfig
from .io.formats import SUPPORTED_FORMATS
from .logging_setup import configure_logging, get_logger
from .pipeline import run

# Nazwa programu prezentowana w pomocy.
PROG_NAME = "compton-scattering-plane-angle-extractor"


class _PolishArgumentParser(argparse.ArgumentParser):
    """Parser argumentów emitujący komunikaty błędów po polsku."""

    def error(self, message: str) -> NoReturn:
        """Wypisuje sposób użycia i polski komunikat błędu, kończąc kodem 2."""
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: błąd: {message}\n")


def _normalized_format(value: str) -> str:
    """Normalizuje wartość ``--output-format`` (usuwa spacje, małe litery)."""
    return value.strip().lower()


def build_parser() -> argparse.ArgumentParser:
    """Buduje parser argumentów wiersza poleceń.

    Returns
    -------
    argparse.ArgumentParser
        Skonfigurowany parser z wszystkimi flagami narzędzia.
    """
    parser = _PolishArgumentParser(
        prog=PROG_NAME,
        description=(
            "Wylicza kąty rozpraszania w płaszczyznach A i B oraz kąt pomiędzy "
            "tymi płaszczyznami na podstawie wektorów pędu z pliku CSV/HDF5."
        ),
    )
    parser.add_argument(
        "--input-file-path",
        required=True,
        help="Ścieżka do pliku wejściowego CSV/HDF5 z danymi rozpraszania.",
    )
    parser.add_argument(
        "--output-dir-path",
        required=True,
        help="Ścieżka do katalogu, w którym zapisany zostanie plik wyjściowy.",
    )
    parser.add_argument(
        "--first-scattering-initial-direction",
        required=True,
        metavar="X,Y,Z",
        help="Nazwy kolumn (x,y,z) pędu przed rozproszeniem w płaszczyźnie A.",
    )
    parser.add_argument(
        "--first-scattering-final-direction",
        required=True,
        metavar="X,Y,Z",
        help="Nazwy kolumn (x,y,z) pędu po rozproszeniu w płaszczyźnie A.",
    )
    parser.add_argument(
        "--second-scattering-initial-direction",
        required=True,
        metavar="X,Y,Z",
        help="Nazwy kolumn (x,y,z) pędu przed rozproszeniem w płaszczyźnie B.",
    )
    parser.add_argument(
        "--second-scattering-final-direction",
        required=True,
        metavar="X,Y,Z",
        help="Nazwy kolumn (x,y,z) pędu po rozproszeniu w płaszczyźnie B.",
    )
    parser.add_argument(
        "--output-file-name",
        default=None,
        help=("Nazwa pliku wyjściowego. Domyślnie 'compton-scattering-plane-angles.<format>'."),
    )
    parser.add_argument(
        "--output-format",
        default=None,
        type=_normalized_format,
        choices=list(SUPPORTED_FORMATS),
        help="Format pliku wyjściowego (csv/hdf5). Domyślnie taki sam jak wejście.",
    )
    parser.add_argument(
        "--rad2deg",
        action="store_true",
        help="Wyraź kąty w stopniach zamiast w radianach.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Uruchamia narzędzie z poziomu linii komend.

    Parameters
    ----------
    argv : list[str] | None
        Lista argumentów do sparsowania. Gdy ``None``, użyte zostaną argumenty
        z ``sys.argv``.

    Returns
    -------
    int
        Kod wyjścia procesu (0 oznacza sukces, 1 oznacza błąd przetwarzania).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging()
    logger = get_logger(__name__)

    try:
        config = _config_from_args(args)
        output_path = run(config)
    except (FileNotFoundError, ValueError) as error:
        logger.error("Błąd: %s", error)
        return 1

    logger.info("Gotowe. Wynik zapisano w: %s", output_path)
    return 0


def _config_from_args(args: argparse.Namespace) -> RunConfig:
    """Buduje :class:`RunConfig` na podstawie sparsowanych argumentów."""
    return RunConfig(
        input_path=Path(args.input_file_path),
        output_dir=Path(args.output_dir_path),
        first_initial=parse_column_spec(args.first_scattering_initial_direction),
        first_final=parse_column_spec(args.first_scattering_final_direction),
        second_initial=parse_column_spec(args.second_scattering_initial_direction),
        second_final=parse_column_spec(args.second_scattering_final_direction),
        output_file_name=args.output_file_name,
        output_format=args.output_format,
        rad2deg=args.rad2deg,
    )
