"""Wczytywanie danych rozpraszania z plików CSV/HDF5.

Format jest rozpoznawany na podstawie rozszerzenia ścieżki albo jawnie podanej
nazwy formatu. Pliki CSV są wczytywane przez ``pandas``, a pliki HDF5 przez
``h5py`` (każda kolumna jest osobnym zbiorem danych).

Funkcje publiczne
-----------------
load_data(path: str | Path, fmt: str | None = None) -> pd.DataFrame
    Wczytuje dane do ramki ``pandas`` z rozpoznaniem formatu.
extract_vectors(frame: pd.DataFrame, columns: ColumnTriplet) -> np.ndarray
    Wyodrębnia z ramki tablicę wektorów ``(N, 3)`` dla wskazanych kolumn.
"""

from pathlib import Path

import h5py
import numpy as np
import pandas as pd

from ..column_spec import ColumnTriplet
from .formats import CSV, HDF5, infer_format, normalize_format


def load_data(path: str | Path, fmt: str | None = None) -> pd.DataFrame:
    """Wczytuje dane rozpraszania do ramki ``pandas``.

    Parameters
    ----------
    path : str | Path
        Ścieżka do pliku wejściowego.
    fmt : str | None
        Jawnie wskazany format (``"csv"`` lub ``"hdf5"``). Gdy ``None``, format
        jest rozpoznawany na podstawie rozszerzenia.

    Returns
    -------
    pd.DataFrame
        Wczytane dane.

    Raises
    ------
    FileNotFoundError
        Gdy plik nie istnieje.
    ValueError
        Gdy format jest nieobsługiwany lub nie można go rozpoznać.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Plik wejściowy nie istnieje: {file_path}.")
    resolved = normalize_format(fmt) if fmt is not None else infer_format(file_path)
    if resolved == CSV:
        return _load_csv(file_path)
    if resolved == HDF5:
        return _load_hdf5(file_path)
    raise ValueError(f"Nieobsługiwany format wejścia: {resolved}.")


def extract_vectors(frame: pd.DataFrame, columns: ColumnTriplet) -> np.ndarray:
    """Wyodrębnia tablicę wektorów ``(N, 3)`` dla wskazanych kolumn.

    Parameters
    ----------
    frame : pd.DataFrame
        Ramka z danymi wejściowymi.
    columns : ColumnTriplet
        Nazwy kolumn ``(x, y, z)`` składowych wektora pędu.

    Returns
    -------
    np.ndarray
        Tablica wektorów o kształcie ``(N, 3)`` i typie ``float``.

    Raises
    ------
    ValueError
        Gdy którejkolwiek ze wskazanych kolumn brakuje w ramce.
    """
    missing = [name for name in columns if name not in frame.columns]
    if missing:
        raise ValueError(f"W danych brakuje wymaganych kolumn: {', '.join(missing)}.")
    vectors: np.ndarray = frame.loc[:, list(columns)].to_numpy(dtype=float)
    return vectors


def _load_csv(path: Path) -> pd.DataFrame:
    """Wczytuje dane z pliku CSV."""
    frame: pd.DataFrame = pd.read_csv(path)
    return frame


def _load_hdf5(path: Path) -> pd.DataFrame:
    """Wczytuje dane z pliku HDF5 (każdy zbiór danych to kolumna)."""
    with h5py.File(path, "r") as handle:
        data = {name: np.asarray(handle[name]) for name in handle}
    return pd.DataFrame(data)
