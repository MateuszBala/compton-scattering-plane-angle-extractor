"""Testy jednostkowe interfejsu linii komend (``cli``)."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from compton_scattering_plane_angle_extractor import cli, pipeline
from compton_scattering_plane_angle_extractor.io.readers import load_data


def _base_argv(input_path: Path, output_dir: Path) -> list[str]:
    """Buduje listę argumentów z wymaganymi flagami dla danych testowych."""
    return [
        "--input-file-path",
        str(input_path),
        "--output-dir-path",
        str(output_dir),
        "--first-scattering-initial-direction",
        "a0x,a0y,a0z",
        "--first-scattering-final-direction",
        "a1x,a1y,a1z",
        "--second-scattering-initial-direction",
        "b0x,b0y,b0z",
        "--second-scattering-final-direction",
        "b1x,b1y,b1z",
    ]


def test_build_parser_requires_input() -> None:
    """Brak wymaganych argumentów kończy parsowanie wyjątkiem SystemExit."""
    # Arrange
    parser = cli.build_parser()

    # Act / Assert
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_main_writes_output_and_returns_zero(
    tmp_path: Path, scattering_frame: pd.DataFrame
) -> None:
    """Poprawne uruchomienie zapisuje plik wynikowy i zwraca kod 0."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    output_dir = tmp_path / "out"

    # Act
    exit_code = cli.main(_base_argv(input_path, output_dir))

    # Assert
    assert exit_code == 0
    output_path = output_dir / "compton-scattering-plane-angles.csv"
    result = pd.read_csv(output_path)
    assert list(result.columns) == list(pipeline.OUTPUT_COLUMNS)


def test_main_rad2deg_produces_degrees(tmp_path: Path, scattering_frame: pd.DataFrame) -> None:
    """Flaga --rad2deg powoduje zapis kątów w stopniach."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    output_dir = tmp_path / "out"
    argv = [*_base_argv(input_path, output_dir), "--rad2deg"]

    # Act
    exit_code = cli.main(argv)

    # Assert
    assert exit_code == 0
    result = pd.read_csv(output_dir / "compton-scattering-plane-angles.csv")
    np.testing.assert_allclose(result["thetaA"].to_numpy(), [90.0], atol=1e-9)


def test_main_returns_one_for_missing_input_file(tmp_path: Path) -> None:
    """Brak pliku wejściowego jest obsłużony i zwraca kod 1."""
    # Arrange
    input_path = tmp_path / "brak.csv"
    output_dir = tmp_path / "out"

    # Act
    exit_code = cli.main(_base_argv(input_path, output_dir))

    # Assert
    assert exit_code == 1


def test_main_returns_one_for_invalid_column_spec(
    tmp_path: Path, scattering_frame: pd.DataFrame
) -> None:
    """Niepoprawna specyfikacja kolumn jest obsłużona i zwraca kod 1."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    argv = _base_argv(input_path, tmp_path / "out")
    spec_index = argv.index("--first-scattering-initial-direction") + 1
    argv[spec_index] = "a0x,a0y"  # tylko dwie nazwy

    # Act
    exit_code = cli.main(argv)

    # Assert
    assert exit_code == 1


def test_main_writes_requested_output_format(
    tmp_path: Path, scattering_frame: pd.DataFrame
) -> None:
    """--output-format hdf5 dla wejścia CSV daje czytelny plik HDF5."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    output_dir = tmp_path / "out"
    argv = [*_base_argv(input_path, output_dir), "--output-format", "hdf5"]

    # Act
    exit_code = cli.main(argv)

    # Assert
    assert exit_code == 0
    output_path = output_dir / "compton-scattering-plane-angles.hdf5"
    reloaded = load_data(output_path)
    np.testing.assert_allclose(reloaded["thetaA"].to_numpy(), [np.pi / 2], atol=1e-9)


def test_main_accepts_uppercase_output_format(
    tmp_path: Path, scattering_frame: pd.DataFrame
) -> None:
    """--output-format HDF5 jest akceptowane niezależnie od wielkości liter."""
    # Arrange
    input_path = tmp_path / "in.csv"
    scattering_frame.to_csv(input_path, index=False)
    output_dir = tmp_path / "out"
    argv = [*_base_argv(input_path, output_dir), "--output-format", "HDF5"]

    # Act
    exit_code = cli.main(argv)

    # Assert
    assert exit_code == 0
    assert (output_dir / "compton-scattering-plane-angles.hdf5").exists()


def test_parser_error_message_is_polish(capsys: pytest.CaptureFixture[str]) -> None:
    """Błąd parsowania argumentów jest komunikowany po polsku."""
    # Arrange
    parser = cli.build_parser()

    # Act / Assert
    with pytest.raises(SystemExit):
        parser.parse_args([])
    assert "błąd:" in capsys.readouterr().err
