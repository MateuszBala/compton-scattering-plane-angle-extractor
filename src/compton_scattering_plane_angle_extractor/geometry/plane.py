"""Wyznaczanie kąta pomiędzy płaszczyznami rozpraszania A i B.

Płaszczyzna rozpraszania jest rozpięta przez kierunki pędu przed i po
rozproszeniu. Jej orientację opisuje wektor normalny ``n = norm(k0 x k)``.
Kąt pomiędzy płaszczyznami to ``arccos(n_a . n_b)`` w zakresie ``[0, pi]``.

Funkcje publiczne
-----------------
plane_normal(initial: np.ndarray, final: np.ndarray) -> np.ndarray
    Wyznacza znormalizowany wektor normalny płaszczyzny rozpraszania.
plane_angle(initial_a, final_a, initial_b, final_b) -> np.ndarray
    Oblicza kąt pomiędzy płaszczyznami rozpraszania A i B.
"""

import numpy as np

from .vectors import clip_cosine, cross, dot, normalize


def plane_normal(initial: np.ndarray, final: np.ndarray) -> np.ndarray:
    """Wyznacza znormalizowany wektor normalny płaszczyzny rozpraszania.

    Parameters
    ----------
    initial : np.ndarray
        Kierunki pędu przed rozproszeniem o kształcie ``(N, 3)``.
    final : np.ndarray
        Kierunki pędu po rozproszeniu o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Znormalizowane wektory normalne o kształcie ``(N, 3)``.

    Raises
    ------
    ValueError
        Gdy pędy są współliniowe (płaszczyzna nieokreślona), co skutkuje
        iloczynem wektorowym o normie bliskiej zeru.
    """
    return normalize(cross(initial, final))


def plane_angle(
    initial_a: np.ndarray,
    final_a: np.ndarray,
    initial_b: np.ndarray,
    final_b: np.ndarray,
) -> np.ndarray:
    """Oblicza kąt pomiędzy płaszczyznami rozpraszania A i B.

    Parameters
    ----------
    initial_a, final_a : np.ndarray
        Kierunki pędu przed i po rozproszeniu w płaszczyźnie A, kształt ``(N, 3)``.
    initial_b, final_b : np.ndarray
        Kierunki pędu przed i po rozproszeniu w płaszczyźnie B, kształt ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Kąty pomiędzy płaszczyznami w radianach z zakresu ``[0, pi]``,
        kształt ``(N,)``.
    """
    normal_a = plane_normal(initial_a, final_a)
    normal_b = plane_normal(initial_b, final_b)
    cosine = clip_cosine(dot(normal_a, normal_b))
    angle: np.ndarray = np.arccos(cosine)
    return angle
