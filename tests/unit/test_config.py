"""Testy jednostkowe konfiguracji uruchomienia (``config``)."""

import dataclasses
from pathlib import Path

import pytest

from compton_scattering_plane_angle_extractor.column_spec import ColumnTriplet
from compton_scattering_plane_angle_extractor.config import RunConfig


def _minimal_config() -> RunConfig:
    """Buduje minimalną konfigurację do testów."""
    triplet = ColumnTriplet("x", "y", "z")
    return RunConfig(
        input_path=Path("wejscie.csv"),
        output_dir=Path("wyniki"),
        first_initial=triplet,
        first_final=triplet,
        second_initial=triplet,
        second_final=triplet,
    )


def test_run_config_uses_expected_defaults() -> None:
    """Pola opcjonalne mają domyślne wartości None/False."""
    # Arrange / Act
    config = _minimal_config()

    # Assert
    assert config.output_file_name is None
    assert config.output_format is None
    assert config.rad2deg is False


def test_run_config_is_frozen() -> None:
    """Konfiguracja jest niemodyfikowalna."""
    # Arrange
    config = _minimal_config()

    # Act / Assert
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.rad2deg = True  # type: ignore[misc]
