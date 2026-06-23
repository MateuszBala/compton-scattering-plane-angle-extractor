"""Konfiguracja uruchomienia narzędzia.

Moduł definiuje strukturę :class:`RunConfig` przechowującą sparsowane argumenty
uruchomienia: ścieżki wejścia/wyjścia, specyfikacje kolumn dla obu rozproszeń,
opcjonalną nazwę i format pliku wyjściowego oraz flagę konwersji na stopnie.

Funkcje publiczne
-----------------
RunConfig
    Niemodyfikowalny zbiór parametrów pojedynczego uruchomienia narzędzia.
"""

from dataclasses import dataclass
from pathlib import Path

from .column_spec import ColumnTriplet


@dataclass(frozen=True)
class RunConfig:
    """Parametry pojedynczego uruchomienia obliczeń.

    Attributes
    ----------
    input_path : Path
        Ścieżka do pliku wejściowego CSV/HDF5.
    output_dir : Path
        Katalog, do którego zapisany zostanie plik wyjściowy.
    first_initial : ColumnTriplet
        Kolumny składowych pędu przed rozproszeniem w płaszczyźnie A.
    first_final : ColumnTriplet
        Kolumny składowych pędu po rozproszeniu w płaszczyźnie A.
    second_initial : ColumnTriplet
        Kolumny składowych pędu przed rozproszeniem w płaszczyźnie B.
    second_final : ColumnTriplet
        Kolumny składowych pędu po rozproszeniu w płaszczyźnie B.
    output_file_name : str | None
        Nazwa pliku wyjściowego. Gdy ``None``, używana jest nazwa domyślna.
    output_format : str | None
        Format pliku wyjściowego (``"csv"`` lub ``"hdf5"``). Gdy ``None``,
        używany jest format pliku wejściowego.
    rad2deg : bool
        Gdy ``True``, kąty w wyniku są wyrażone w stopniach zamiast radianów.
    """

    input_path: Path
    output_dir: Path
    first_initial: ColumnTriplet
    first_final: ColumnTriplet
    second_initial: ColumnTriplet
    second_final: ColumnTriplet
    output_file_name: str | None = None
    output_format: str | None = None
    rad2deg: bool = False
