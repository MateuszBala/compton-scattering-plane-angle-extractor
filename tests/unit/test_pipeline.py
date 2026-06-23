"""Testy jednostkowe potoku obliczeń (``pipeline``)."""

from pathlib import Path

import numpy as np
import pandas as pd

from compton_scattering_plane_angle_extractor import pipeline
from compton_scattering_plane_angle_extractor.column_spec import ColumnTriplet
from compton_scattering_plane_angle_extractor.config import RunConfig


def test_compute_angles_returns_expected_columns_and_values(
    scattering_frame: pd.DataFrame,
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Obliczenia zwracają kolumny w ustalonej kolejności i poprawne wartości."""
    # Arrange
    config = RunConfig(
        input_path=Path("in.csv"),
        output_dir=Path("out"),
        **scattering_columns,
    )

    # Act
    result = pipeline.compute_angles(scattering_frame, config)

    # Assert
    assert list(result.columns) == list(pipeline.OUTPUT_COLUMNS)
    np.testing.assert_allclose(
        result.iloc[0].to_numpy(),
        [np.pi / 2, 0.0, np.pi / 2, np.pi / 2, np.pi / 2],
        atol=1e-9,
    )


def test_compute_angles_converts_to_degrees_when_requested(
    scattering_frame: pd.DataFrame,
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Flaga rad2deg powoduje wyrażenie kątów w stopniach."""
    # Arrange
    config = RunConfig(
        input_path=Path("in.csv"),
        output_dir=Path("out"),
        rad2deg=True,
        **scattering_columns,
    )

    # Act
    result = pipeline.compute_angles(scattering_frame, config)

    # Assert
    np.testing.assert_allclose(result.iloc[0].to_numpy(), [90.0, 0.0, 90.0, 90.0, 90.0], atol=1e-9)


def test_resolve_output_uses_default_name_and_input_format(
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Bez jawnych ustawień nazwa i format wynikają z pliku wejściowego."""
    # Arrange
    config = RunConfig(
        input_path=Path("dane/in.csv"),
        output_dir=Path("out"),
        **scattering_columns,
    )

    # Act
    path, fmt = pipeline._resolve_output(config)

    # Assert
    assert fmt == "csv"
    assert path == Path("out/compton-scattering-plane-angles.csv")


def test_resolve_output_uses_explicit_format(
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Jawny format wyjścia ma pierwszeństwo nad formatem wejścia."""
    # Arrange
    config = RunConfig(
        input_path=Path("dane/in.csv"),
        output_dir=Path("out"),
        output_format="hdf5",
        **scattering_columns,
    )

    # Act
    path, fmt = pipeline._resolve_output(config)

    # Assert
    assert fmt == "hdf5"
    assert path == Path("out/compton-scattering-plane-angles.hdf5")


def test_resolve_output_uses_custom_file_name(
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Podana nazwa pliku wyjściowego jest używana dosłownie."""
    # Arrange
    config = RunConfig(
        input_path=Path("dane/in.csv"),
        output_dir=Path("out"),
        output_file_name="wynik.csv",
        **scattering_columns,
    )

    # Act
    path, _ = pipeline._resolve_output(config)

    # Assert
    assert path == Path("out/wynik.csv")
