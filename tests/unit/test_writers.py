"""Testy jednostkowe zapisu danych (``io.writers``)."""

from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import pytest

from compton_scattering_plane_angle_extractor.io import writers


def test_write_data_writes_csv(tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
    """Zapis do CSV tworzy plik o tej samej zawartości."""
    # Arrange
    path = tmp_path / "wynik.csv"

    # Act
    writers.write_data(sample_dataframe, path)

    # Assert
    reloaded = pd.read_csv(path)
    pd.testing.assert_frame_equal(reloaded, sample_dataframe)


def test_write_data_writes_hdf5(tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
    """Zapis do HDF5 tworzy zbiory danych dla każdej kolumny."""
    # Arrange
    path = tmp_path / "wynik.h5"

    # Act
    writers.write_data(sample_dataframe, path)

    # Assert
    with h5py.File(path, "r") as handle:
        stored = np.asarray(handle["py"])
    np.testing.assert_allclose(stored, [0.0, 1.0, 0.0])


def test_write_data_creates_parent_directory(
    tmp_path: Path, sample_dataframe: pd.DataFrame
) -> None:
    """Zapis tworzy nieistniejący katalog docelowy."""
    # Arrange
    path = tmp_path / "podkatalog" / "wynik.csv"

    # Act
    writers.write_data(sample_dataframe, path)

    # Assert
    assert path.exists()


def test_write_data_raises_for_unknown_format(
    tmp_path: Path, sample_dataframe: pd.DataFrame
) -> None:
    """Nieznane rozszerzenie pliku wyjściowego zgłasza ValueError."""
    # Arrange
    path = tmp_path / "wynik.txt"

    # Act / Assert
    with pytest.raises(ValueError):
        writers.write_data(sample_dataframe, path)
