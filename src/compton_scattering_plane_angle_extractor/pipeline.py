"""Potok obliczeń łączący wczytywanie danych, geometrię i zapis wyników.

Moduł spina warstwę IO z obliczeniami geometrycznymi: wczytuje dane wejściowe,
wyznacza kąty rozpraszania i azymutalne dla obu płaszczyzn oraz kąt między
płaszczyznami, a następnie zapisuje ramkę wynikową z kolumnami ``thetaA``,
``phiA``, ``thetaB``, ``phiB`` i ``planeAngle``.

Funkcje publiczne
-----------------
compute_angles(frame: pd.DataFrame, config: RunConfig) -> pd.DataFrame
    Wyznacza ramkę kątów na podstawie danych wejściowych i konfiguracji.
run(config: RunConfig) -> Path
    Wykonuje pełny przepływ: wczytanie, obliczenia i zapis wyników.
"""

from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd

from .config import RunConfig
from .geometry.plane import plane_angle
from .geometry.scattering import azimuthal_angle, scattering_angle
from .io import formats
from .io.readers import extract_vectors, load_data
from .io.writers import write_data
from .logging_setup import get_logger
from .units import rad_to_deg

logger = get_logger(__name__)

# Kolumny ramki wynikowej w wymaganej kolejności.
OUTPUT_COLUMNS: Final[tuple[str, ...]] = (
    "thetaA",
    "phiA",
    "thetaB",
    "phiB",
    "planeAngle",
)

# Rdzeń domyślnej nazwy pliku wyjściowego (bez rozszerzenia).
DEFAULT_OUTPUT_STEM: Final[str] = "compton-scattering-plane-angles"


def compute_angles(frame: pd.DataFrame, config: RunConfig) -> pd.DataFrame:
    """Wyznacza ramkę kątów na podstawie danych wejściowych.

    Parameters
    ----------
    frame : pd.DataFrame
        Dane wejściowe z kolumnami składowych pędu.
    config : RunConfig
        Konfiguracja uruchomienia (kolumny, flaga ``rad2deg``).

    Returns
    -------
    pd.DataFrame
        Ramka z kolumnami :data:`OUTPUT_COLUMNS`. Kąty w radianach albo, gdy
        ``config.rad2deg`` jest ustawione, w stopniach.
    """
    initial_a = extract_vectors(frame, config.first_initial)
    final_a = extract_vectors(frame, config.first_final)
    initial_b = extract_vectors(frame, config.second_initial)
    final_b = extract_vectors(frame, config.second_final)

    angles: dict[str, np.ndarray] = {
        "thetaA": scattering_angle(initial_a, final_a),
        "phiA": azimuthal_angle(initial_a, final_a),
        "thetaB": scattering_angle(initial_b, final_b),
        "phiB": azimuthal_angle(initial_b, final_b),
        "planeAngle": plane_angle(initial_a, final_a, initial_b, final_b),
    }
    if config.rad2deg:
        angles = {name: rad_to_deg(values) for name, values in angles.items()}
    return pd.DataFrame(angles, columns=list(OUTPUT_COLUMNS))


def run(config: RunConfig) -> Path:
    """Wykonuje pełny przepływ: wczytanie, obliczenia i zapis wyników.

    Parameters
    ----------
    config : RunConfig
        Konfiguracja uruchomienia.

    Returns
    -------
    Path
        Ścieżka zapisanego pliku wynikowego.
    """
    frame = load_data(config.input_path)
    logger.info("Wczytano %d wierszy z %s", len(frame), config.input_path)

    result = compute_angles(frame, config)

    output_path, output_format = _resolve_output(config)
    write_data(result, output_path, fmt=output_format)
    logger.info("Zapisano wyniki (%s) do %s", output_format, output_path)
    return output_path


def _resolve_output(config: RunConfig) -> tuple[Path, str]:
    """Wyznacza ścieżkę i format pliku wyjściowego.

    Format wyjścia to jawnie podany ``config.output_format`` albo — gdy go brak —
    format pliku wejściowego. Nazwa pliku to ``config.output_file_name`` albo
    nazwa domyślna ``compton-scattering-plane-angles.<format>``.
    """
    input_format = formats.infer_format(config.input_path)
    if config.output_format is not None:
        output_format = formats.normalize_format(config.output_format)
    else:
        output_format = input_format

    if config.output_file_name is not None:
        file_name = config.output_file_name
    else:
        file_name = f"{DEFAULT_OUTPUT_STEM}.{output_format}"

    return config.output_dir / file_name, output_format
