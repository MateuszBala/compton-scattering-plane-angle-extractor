"""Testy jednostkowe wczytywania danych (``io.readers``)."""

from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import pytest

from compton_scattering_plane_angle_extractor import column_spec
from compton_scattering_plane_angle_extractor.io import readers


def test_load_data_reads_csv(tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
    """Wczytanie pliku CSV zwraca zapisane dane."""
    # Arrange
    path = tmp_path / "wejscie.csv"
    sample_dataframe.to_csv(path, index=False)

    # Act
    result = readers.load_data(path)

    # Assert
    pd.testing.assert_frame_equal(result, sample_dataframe)


def test_load_data_reads_hdf5(tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
    """Wczytanie pliku HDF5 zwraca zapisane kolumny."""
    # Arrange
    path = tmp_path / "wejscie.h5"
    with h5py.File(path, "w") as handle:
        for column in sample_dataframe.columns:
            handle.create_dataset(column, data=sample_dataframe[column].to_numpy())

    # Act
    result = readers.load_data(path)

    # Assert
    np.testing.assert_allclose(result["px"].to_numpy(), [1.0, 0.0, 0.0])


def test_load_data_uses_explicit_format(tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
    """Jawnie podany format ma pierwszeństwo nad rozszerzeniem."""
    # Arrange: plik z rozszerzeniem .dat, ale treścią CSV
    path = tmp_path / "wejscie.dat"
    sample_dataframe.to_csv(path, index=False)

    # Act
    result = readers.load_data(path, fmt="csv")

    # Assert
    pd.testing.assert_frame_equal(result, sample_dataframe)


def test_load_data_raises_for_missing_file(tmp_path: Path) -> None:
    """Brak pliku wejściowego zgłasza FileNotFoundError."""
    # Arrange
    path = tmp_path / "brak.csv"

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        readers.load_data(path)


def test_load_data_raises_for_directory_path(tmp_path: Path) -> None:
    """Ścieżka wskazująca na katalog zgłasza FileNotFoundError, nie błąd pandas/h5py."""
    # Arrange
    directory = tmp_path / "katalog.csv"
    directory.mkdir()

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        readers.load_data(directory)


def test_extract_vectors_returns_array(sample_dataframe: pd.DataFrame) -> None:
    """Wyodrębnienie kolumn zwraca tablicę wektorów (N, 3)."""
    # Arrange
    columns = column_spec.ColumnTriplet("px", "py", "pz")

    # Act
    result = readers.extract_vectors(sample_dataframe, columns)

    # Assert
    np.testing.assert_allclose(result, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])


def test_extract_vectors_raises_for_missing_column(
    sample_dataframe: pd.DataFrame,
) -> None:
    """Brak wskazanej kolumny w danych zgłasza ValueError."""
    # Arrange
    columns = column_spec.ColumnTriplet("px", "py", "brak")

    # Act / Assert
    with pytest.raises(ValueError):
        readers.extract_vectors(sample_dataframe, columns)
