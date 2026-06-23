"""Rozpoznawanie i normalizacja formatów plików wejścia/wyjścia.

Obsługiwane formaty to CSV oraz HDF5. Format można wskazać jawnie (np. z opcji
``--output-format``) lub wywnioskować z rozszerzenia ścieżki.

Funkcje publiczne
-----------------
infer_format(path: Path) -> str
    Rozpoznaje format na podstawie rozszerzenia ścieżki.
normalize_format(value: str) -> str
    Sprawdza i normalizuje jawnie podaną nazwę formatu.
"""

from pathlib import Path
from typing import Final

# Identyfikatory obsługiwanych formatów.
CSV: Final[str] = "csv"
HDF5: Final[str] = "hdf5"

# Obsługiwane formaty w kolejności prezentacji w komunikatach błędów.
SUPPORTED_FORMATS: Final[tuple[str, ...]] = (CSV, HDF5)

# Mapowanie rozszerzeń plików na identyfikatory formatów.
_EXTENSION_TO_FORMAT: Final[dict[str, str]] = {
    ".csv": CSV,
    ".h5": HDF5,
    ".hdf5": HDF5,
    ".hdf": HDF5,
}


def infer_format(path: Path) -> str:
    """Rozpoznaje format pliku na podstawie rozszerzenia.

    Parameters
    ----------
    path : Path
        Ścieżka pliku, której rozszerzenie określa format.

    Returns
    -------
    str
        Identyfikator formatu (:data:`CSV` lub :data:`HDF5`).

    Raises
    ------
    ValueError
        Gdy rozszerzenie nie odpowiada żadnemu obsługiwanemu formatowi.
    """
    suffix = path.suffix.lower()
    if suffix not in _EXTENSION_TO_FORMAT:
        supported = ", ".join(sorted(_EXTENSION_TO_FORMAT))
        raise ValueError(
            f'Nie można rozpoznać formatu po rozszerzeniu "{path.suffix}". '
            f"Obsługiwane rozszerzenia: {supported}."
        )
    return _EXTENSION_TO_FORMAT[suffix]


def normalize_format(value: str) -> str:
    """Sprawdza i normalizuje jawnie podaną nazwę formatu.

    Parameters
    ----------
    value : str
        Nazwa formatu, np. ``"CSV"`` lub ``"hdf5"`` (wielkość liter dowolna).

    Returns
    -------
    str
        Znormalizowany identyfikator formatu.

    Raises
    ------
    ValueError
        Gdy nazwa formatu nie jest obsługiwana.
    """
    normalized = value.strip().lower()
    if normalized not in SUPPORTED_FORMATS:
        supported = ", ".join(SUPPORTED_FORMATS)
        raise ValueError(f'Nieobsługiwany format: "{value}". Dostępne formaty: {supported}.')
    return normalized
