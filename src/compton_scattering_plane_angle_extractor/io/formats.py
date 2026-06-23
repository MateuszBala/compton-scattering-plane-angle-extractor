"""Rozpoznawanie i normalizacja formatów plików wejścia/wyjścia.

Obsługiwane formaty to CSV oraz HDF5. Format można wskazać jawnie (np. z opcji
``--output-format``) lub wywnioskować z rozszerzenia ścieżki.

Funkcje publiczne
-----------------
format_from_extension(path: Path) -> str | None
    Zwraca format dla rozszerzenia ścieżki lub ``None``, gdy nieznane.
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


def format_from_extension(path: Path) -> str | None:
    """Zwraca format dla rozszerzenia ścieżki lub ``None``, gdy nieznane.

    Parameters
    ----------
    path : Path
        Ścieżka, której rozszerzenie jest sprawdzane.

    Returns
    -------
    str | None
        Identyfikator formatu (:data:`CSV` lub :data:`HDF5`) albo ``None``, gdy
        rozszerzenie nie odpowiada żadnemu obsługiwanemu formatowi.
    """
    return _EXTENSION_TO_FORMAT.get(path.suffix.lower())


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
    resolved = format_from_extension(path)
    if resolved is None:
        supported = ", ".join(sorted(_EXTENSION_TO_FORMAT))
        raise ValueError(
            f'Nie można rozpoznać formatu po rozszerzeniu "{path.suffix}". '
            f"Obsługiwane rozszerzenia: {supported}."
        )
    return resolved


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
