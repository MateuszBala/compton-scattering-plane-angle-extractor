"""Podstawowe, wektoryzowane operacje na wektorach pędu.

Wszystkie funkcje operują na tablicach NumPy o kształcie ``(N, 3)``, gdzie ``N``
jest liczbą wektorów, a ostatnia oś przechowuje składowe ``(x, y, z)``. Operacje
są wykonywane wierszami (bez pętli w Pythonie).

Funkcje publiczne
-----------------
normalize(vectors: np.ndarray) -> np.ndarray
    Normalizuje wektory do długości jednostkowej.
dot(left: np.ndarray, right: np.ndarray) -> np.ndarray
    Iloczyn skalarny wierszami.
cross(left: np.ndarray, right: np.ndarray) -> np.ndarray
    Iloczyn wektorowy wierszami.
clip_cosine(values: np.ndarray) -> np.ndarray
    Przycina wartości kosinusa do zakresu ``[-1, 1]``.
"""

from typing import Final

import numpy as np

# Minimalna dopuszczalna norma wektora; poniżej tej wartości wektor uznajemy za
# zerowy (np. współliniowe pędy przy wyznaczaniu normalnej płaszczyzny).
MIN_NORM: Final[float] = 1e-12

# Granice zakresu kosinusa kąta po przycięciu błędów numerycznych.
COS_MIN: Final[float] = -1.0
COS_MAX: Final[float] = 1.0


def normalize(vectors: np.ndarray) -> np.ndarray:
    """Normalizuje wektory do długości jednostkowej.

    Parameters
    ----------
    vectors : np.ndarray
        Tablica wektorów o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Wektory jednostkowe o tym samym kształcie co wejście.

    Raises
    ------
    ValueError
        Gdy którykolwiek wektor ma normę mniejszą niż :data:`MIN_NORM`.

    Examples
    --------
    >>> normalize(np.array([[3.0, 4.0, 0.0]]))
    array([[0.6, 0.8, 0. ]])
    """
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    if np.any(norms < MIN_NORM):
        raise ValueError("Nie można znormalizować wektora o normie bliskiej zeru.")
    unit_vectors: np.ndarray = vectors / norms
    return unit_vectors


def dot(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Oblicza iloczyn skalarny wierszami.

    Parameters
    ----------
    left, right : np.ndarray
        Tablice wektorów o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Iloczyny skalarne o kształcie ``(N,)``.
    """
    return np.sum(left * right, axis=-1)


def cross(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Oblicza iloczyn wektorowy wierszami.

    Parameters
    ----------
    left, right : np.ndarray
        Tablice wektorów o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Iloczyny wektorowe o kształcie ``(N, 3)``.
    """
    return np.cross(left, right)


def clip_cosine(values: np.ndarray) -> np.ndarray:
    """Przycina wartości kosinusa do zakresu ``[-1, 1]``.

    Zabezpiecza przed błędami numerycznymi, które mogłyby wyprowadzić argument
    ``arccos`` poza dziedzinę.

    Parameters
    ----------
    values : np.ndarray
        Wartości kosinusa kąta.

    Returns
    -------
    np.ndarray
        Wartości przycięte do zakresu ``[COS_MIN, COS_MAX]``.
    """
    clipped: np.ndarray = np.clip(values, COS_MIN, COS_MAX)
    return clipped
