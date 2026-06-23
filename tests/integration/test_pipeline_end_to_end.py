"""Testy integracyjne pełnego przepływu potoku (``pipeline.run``)."""

from pathlib import Path

import numpy as np
import pandas as pd

from compton_scattering_plane_angle_extractor import pipeline
from compton_scattering_plane_angle_extractor.column_spec import ColumnTriplet
from compton_scattering_plane_angle_extractor.config import RunConfig
from compton_scattering_plane_angle_extractor.io.readers import load_data


def test_run_writes_csv_with_expected_values(
    tmp_path: Path,
    scattering_frame: pd.DataFrame,
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Pełny przebieg dla CSV zapisuje plik o oczekiwanych kolumnach i wartościach."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    config = RunConfig(
        input_path=input_path,
        output_dir=tmp_path / "out",
        **scattering_columns,
    )

    # Act
    output_path = pipeline.run(config)

    # Assert
    assert output_path == tmp_path / "out" / "compton-scattering-plane-angles.csv"
    result = pd.read_csv(output_path)
    assert list(result.columns) == list(pipeline.OUTPUT_COLUMNS)
    np.testing.assert_allclose(
        result.iloc[0].to_numpy(),
        [np.pi / 2, 0.0, np.pi / 2, np.pi / 2, np.pi / 2],
        atol=1e-9,
    )


def test_run_honours_output_format_override(
    tmp_path: Path,
    scattering_frame: pd.DataFrame,
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Jawny format wyjścia HDF5 dla wejścia CSV daje plik HDF5 z poprawnymi danymi."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    config = RunConfig(
        input_path=input_path,
        output_dir=tmp_path / "out",
        output_format="hdf5",
        **scattering_columns,
    )

    # Act
    output_path = pipeline.run(config)

    # Assert
    assert output_path.suffix == ".hdf5"
    reloaded = load_data(output_path)
    np.testing.assert_allclose(reloaded["planeAngle"].to_numpy(), [np.pi / 2], atol=1e-9)


def test_run_with_hdf5_file_name_writes_reloadable_file(
    tmp_path: Path,
    scattering_frame: pd.DataFrame,
    scattering_columns: dict[str, ColumnTriplet],
) -> None:
    """Nazwa pliku z rozszerzeniem .hdf5 (bez jawnego formatu) daje plik HDF5."""
    # Arrange: wejście CSV, nazwa wyjścia z rozszerzeniem .hdf5, brak output_format
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    config = RunConfig(
        input_path=input_path,
        output_dir=tmp_path / "out",
        output_file_name="wynik.hdf5",
        **scattering_columns,
    )

    # Act
    output_path = pipeline.run(config)

    # Assert: plik daje się ponownie wczytać zgodnie z rozszerzeniem (format HDF5)
    assert output_path.name == "wynik.hdf5"
    reloaded = load_data(output_path)
    np.testing.assert_allclose(reloaded["thetaA"].to_numpy(), [np.pi / 2], atol=1e-9)
