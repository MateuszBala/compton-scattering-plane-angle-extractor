"""Zapis wyników do plików CSV/HDF5.

Format jest rozpoznawany na podstawie rozszerzenia ścieżki albo jawnie podanej
nazwy formatu. Pliki CSV są zapisywane przez ``pandas``, a pliki HDF5 przez
``h5py`` (każda kolumna trafia do osobnego zbioru danych). Katalog docelowy jest
tworzony, jeśli nie istnieje.

Funkcje publiczne
-----------------
write_data(frame: pd.DataFrame, path: str | Path, fmt: str | None = None) -> None
    Zapisuje ramkę do wskazanego pliku w rozpoznanym formacie.
"""

from pathlib import Path

import h5py
import pandas as pd

from .formats import CSV, HDF5, infer_format, normalize_format


def write_data(
    frame: pd.DataFrame,
    path: str | Path,
    fmt: str | None = None,
) -> None:
    """Zapisuje ramkę wyników do pliku.

    Parameters
    ----------
    frame : pd.DataFrame
        Ramka z wynikami do zapisania.
    path : str | Path
        Ścieżka pliku wyjściowego.
    fmt : str | None
        Jawnie wskazany format (``"csv"`` lub ``"hdf5"``). Gdy ``None``, format
        jest rozpoznawany na podstawie rozszerzenia ścieżki.

    Raises
    ------
    ValueError
        Gdy format jest nieobsługiwany lub nie można go rozpoznać.
    """
    file_path = Path(path)
    resolved = normalize_format(fmt) if fmt is not None else infer_format(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if resolved == CSV:
        _write_csv(frame, file_path)
        return
    if resolved == HDF5:
        _write_hdf5(frame, file_path)
        return
    raise ValueError(f"Nieobsługiwany format wyjścia: {resolved}.")


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    """Zapisuje ramkę do pliku CSV (bez kolumny indeksu)."""
    frame.to_csv(path, index=False)


def _write_hdf5(frame: pd.DataFrame, path: Path) -> None:
    """Zapisuje ramkę do pliku HDF5 (każda kolumna to osobny zbiór danych)."""
    with h5py.File(path, "w") as handle:
        for column in frame.columns:
            handle.create_dataset(str(column), data=frame[column].to_numpy())
