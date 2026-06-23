"""Wyznaczanie kątów rozpraszania i azymutalnych w pojedynczej płaszczyźnie.

Moduł implementuje metodę opisaną w dokumentacji projektu (README): kąt
rozpraszania ``theta = arccos(k0 . k)`` oraz kąt azymutalny ``phi`` wyznaczany z
``atan2`` w układzie bazowym ``(e1, e2)`` zbudowanym względem osi referencyjnej.

Wszystkie funkcje przyjmują kierunki pędu jako tablice ``(N, 3)`` (niekoniecznie
znormalizowane) i zwracają kąty wierszami.

Funkcje publiczne
-----------------
reference_axis(initial_unit: np.ndarray) -> np.ndarray
    Wyznacza oś referencyjną ``a`` zależną od składowej ``z`` kierunku pędu.
scattering_angle(initial: np.ndarray, final: np.ndarray) -> np.ndarray
    Oblicza kąt rozpraszania ``theta`` w zakresie ``[0, pi]``.
azimuthal_angle(initial: np.ndarray, final: np.ndarray) -> np.ndarray
    Oblicza kąt azymutalny ``phi`` w zakresie ``[0, 2*pi)``.
"""

from typing import Final

import numpy as np

from ..units import wrap_to_two_pi
from .vectors import clip_cosine, cross, dot, normalize

# Próg składowej z, powyżej którego oś referencyjna przełącza się z osi Z na X,
# aby uniknąć degeneracji iloczynu wektorowego dla pędów blisko równoległych do Z.
Z_THRESHOLD: Final[float] = 0.9

# Osie referencyjne wybierane w zależności od orientacji kierunku pędu.
_AXIS_Z: Final[np.ndarray] = np.array([0.0, 0.0, 1.0])
_AXIS_X: Final[np.ndarray] = np.array([1.0, 0.0, 0.0])


def reference_axis(initial_unit: np.ndarray) -> np.ndarray:
    """Wyznacza oś referencyjną ``a`` dla każdego kierunku pędu.

    Zgodnie z metodą: ``a = (0, 0, 1)`` gdy ``|k0_z| < 0.9``, w przeciwnym razie
    ``a = (1, 0, 0)``.

    Parameters
    ----------
    initial_unit : np.ndarray
        Znormalizowane kierunki pędu przed rozproszeniem o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Osie referencyjne o kształcie ``(N, 3)``.
    """
    use_x_axis = np.abs(initial_unit[:, 2]) >= Z_THRESHOLD
    axes = np.broadcast_to(_AXIS_Z, initial_unit.shape).copy()
    axes[use_x_axis] = _AXIS_X
    return axes


def scattering_angle(initial: np.ndarray, final: np.ndarray) -> np.ndarray:
    """Oblicza kąt rozpraszania ``theta``.

    Parameters
    ----------
    initial : np.ndarray
        Kierunki pędu przed rozproszeniem o kształcie ``(N, 3)``.
    final : np.ndarray
        Kierunki pędu po rozproszeniu o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Kąty rozpraszania w radianach z zakresu ``[0, pi]``, kształt ``(N,)``.
    """
    initial_unit = normalize(initial)
    final_unit = normalize(final)
    cosine = clip_cosine(dot(initial_unit, final_unit))
    angle: np.ndarray = np.arccos(cosine)
    return angle


def azimuthal_angle(initial: np.ndarray, final: np.ndarray) -> np.ndarray:
    """Oblicza kąt azymutalny ``phi`` w zakresie ``[0, 2*pi)``.

    Buduje układ bazowy ``(e1, e2)`` względem osi referencyjnej:
    ``e1 = norm(a x k0)``, ``e2 = k0 x e1``, a następnie
    ``phi = atan2(k . e2, k . e1)`` znormalizowane do ``[0, 2*pi)``.

    Parameters
    ----------
    initial : np.ndarray
        Kierunki pędu przed rozproszeniem o kształcie ``(N, 3)``.
    final : np.ndarray
        Kierunki pędu po rozproszeniu o kształcie ``(N, 3)``.

    Returns
    -------
    np.ndarray
        Kąty azymutalne w radianach z zakresu ``[0, 2*pi)``, kształt ``(N,)``.
    """
    initial_unit = normalize(initial)
    final_unit = normalize(final)
    axis = reference_axis(initial_unit)
    e1 = normalize(cross(axis, initial_unit))
    e2 = cross(initial_unit, e1)
    phi = np.arctan2(dot(final_unit, e2), dot(final_unit, e1))
    return wrap_to_two_pi(phi)
