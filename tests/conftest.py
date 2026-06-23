"""Wspólne fixtures pytest dla testów pakietu.

Fixtures
--------
sample_dataframe() -> pd.DataFrame
    Przykładowa ramka z kolumnami składowych wektora pędu.
scattering_frame() -> pd.DataFrame
    Ramka z kolumnami obu rozproszeń dla testów potoku obliczeń.
scattering_columns() -> dict[str, ColumnTriplet]
    Specyfikacje kolumn obu rozproszeń jako argumenty dla ``RunConfig``.
"""

import pandas as pd
import pytest

from compton_scattering_plane_angle_extractor.column_spec import ColumnTriplet


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Zwraca przykładową ramkę z kolumnami ``px``, ``py``, ``pz``."""
    return pd.DataFrame(
        {
            "px": [1.0, 0.0, 0.0],
            "py": [0.0, 1.0, 0.0],
            "pz": [0.0, 0.0, 1.0],
        }
    )


@pytest.fixture
def scattering_frame() -> pd.DataFrame:
    """Zwraca ramkę z kolumnami pędów przed/po rozproszeniu w płaszczyznach A i B.

    Dla pojedynczego wiersza oczekiwane kąty wynoszą:
    ``thetaA=pi/2``, ``phiA=0``, ``thetaB=pi/2``, ``phiB=pi/2``, ``planeAngle=pi/2``.
    """
    return pd.DataFrame(
        {
            "a0x": [1.0],
            "a0y": [0.0],
            "a0z": [0.0],
            "a1x": [0.0],
            "a1y": [1.0],
            "a1z": [0.0],
            "b0x": [1.0],
            "b0y": [0.0],
            "b0z": [0.0],
            "b1x": [0.0],
            "b1y": [0.0],
            "b1z": [1.0],
        }
    )


@pytest.fixture
def scattering_columns() -> dict[str, ColumnTriplet]:
    """Zwraca specyfikacje kolumn obu rozproszeń jako argumenty ``RunConfig``."""
    return {
        "first_initial": ColumnTriplet("a0x", "a0y", "a0z"),
        "first_final": ColumnTriplet("a1x", "a1y", "a1z"),
        "second_initial": ColumnTriplet("b0x", "b0y", "b0z"),
        "second_final": ColumnTriplet("b1x", "b1y", "b1z"),
    }
