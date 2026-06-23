"""Testy jednostkowe rozpoznawania formatów (``io.formats``)."""

from pathlib import Path

import pytest

from compton_scattering_plane_angle_extractor.io import formats


def test_infer_format_recognizes_csv() -> None:
    """Rozszerzenie .csv jest rozpoznawane jako format CSV."""
    # Arrange
    path = Path("dane/wejscie.csv")

    # Act
    result = formats.infer_format(path)

    # Assert
    assert result == formats.CSV


def test_infer_format_recognizes_hdf5_extensions() -> None:
    """Rozszerzenie .h5 jest rozpoznawane jako format HDF5."""
    # Arrange
    path = Path("dane/wejscie.h5")

    # Act
    result = formats.infer_format(path)

    # Assert
    assert result == formats.HDF5


def test_infer_format_raises_for_unknown_extension() -> None:
    """Nieznane rozszerzenie zgłasza ValueError."""
    # Arrange
    path = Path("dane/wejscie.txt")

    # Act / Assert
    with pytest.raises(ValueError):
        formats.infer_format(path)


def test_normalize_format_is_case_insensitive() -> None:
    """Nazwa formatu jest normalizowana niezależnie od wielkości liter."""
    # Arrange
    value = "HDF5"

    # Act
    result = formats.normalize_format(value)

    # Assert
    assert result == formats.HDF5


def test_normalize_format_raises_for_unsupported_value() -> None:
    """Nieobsługiwana nazwa formatu zgłasza ValueError."""
    # Arrange
    value = "parquet"

    # Act / Assert
    with pytest.raises(ValueError):
        formats.normalize_format(value)
