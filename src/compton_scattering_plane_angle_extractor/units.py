"""Konwersje jednostek i normalizacja zakresów kątów.

Funkcje publiczne
-----------------
rad_to_deg(angles: np.ndarray) -> np.ndarray
    Konwertuje kąty z radianów na stopnie.
wrap_to_two_pi(phi: np.ndarray) -> np.ndarray
    Normalizuje kąt azymutalny do zakresu ``[0, 2*pi)``.
"""

from typing import Final

import numpy as np

# Pełny kąt pełny w radianach, używany do normalizacji kąta azymutalnego.
TWO_PI: Final[float] = 2.0 * np.pi


def rad_to_deg(angles: np.ndarray) -> np.ndarray:
    """Konwertuje kąty z radianów na stopnie.

    Parameters
    ----------
    angles : np.ndarray
        Kąty wyrażone w radianach.

    Returns
    -------
    np.ndarray
        Kąty wyrażone w stopniach.
    """
    degrees: np.ndarray = np.degrees(angles)
    return degrees


def wrap_to_two_pi(phi: np.ndarray) -> np.ndarray:
    """Normalizuje kąt azymutalny do zakresu ``[0, 2*pi)``.

    Implementuje transformację z dokumentacji metody: ujemne wartości kąta
    (zwracane przez ``arctan2`` z zakresu ``(-pi, pi]``) są przesuwane o pełny
    kąt, tak aby wynik znalazł się w ``[0, 2*pi)``.

    Parameters
    ----------
    phi : np.ndarray
        Kąty azymutalne w radianach, zwykle z zakresu ``(-pi, pi]``.

    Returns
    -------
    np.ndarray
        Kąty przesunięte do zakresu ``[0, 2*pi)``.
    """
    return np.where(phi < 0.0, phi + TWO_PI, phi)
