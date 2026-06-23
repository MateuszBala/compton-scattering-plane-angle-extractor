"""Wspólne fixtures pytest dla testów pakietu.

Fixtures
--------
sample_dataframe() -> pd.DataFrame
    Przykładowa ramka z kolumnami składowych wektora pędu.
"""

import pandas as pd
import pytest


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
