"""Testy jednostkowe kąta między płaszczyznami rozpraszania (``geometry.plane``)."""

import numpy as np
import pytest

from compton_scattering_plane_angle_extractor.geometry import plane


def test_plane_normal_is_unit_cross_product() -> None:
    """Wektor normalny to znormalizowany iloczyn wektorowy pędów."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[0.0, 1.0, 0.0]])

    # Act
    result = plane.plane_normal(initial, final)

    # Assert
    np.testing.assert_allclose(result, [[0.0, 0.0, 1.0]])


def test_plane_normal_raises_for_collinear_momenta() -> None:
    """Współliniowe pędy nie wyznaczają płaszczyzny i zgłaszają ValueError."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[2.0, 0.0, 0.0]])

    # Act / Assert
    with pytest.raises(ValueError):
        plane.plane_normal(initial, final)


def test_plane_angle_perpendicular_planes_is_half_pi() -> None:
    """Prostopadłe płaszczyzny rozpraszania dają kąt pi/2."""
    # Arrange: normalna A = (0,0,1), normalna B = (0,-1,0)
    initial_a = np.array([[1.0, 0.0, 0.0]])
    final_a = np.array([[0.0, 1.0, 0.0]])
    initial_b = np.array([[1.0, 0.0, 0.0]])
    final_b = np.array([[0.0, 0.0, 1.0]])

    # Act
    result = plane.plane_angle(initial_a, final_a, initial_b, final_b)

    # Assert
    np.testing.assert_allclose(result, [np.pi / 2])


def test_plane_angle_identical_planes_is_zero() -> None:
    """Identyczne płaszczyzny rozpraszania dają kąt 0."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[0.0, 1.0, 0.0]])

    # Act
    result = plane.plane_angle(initial, final, initial, final)

    # Assert
    np.testing.assert_allclose(result, [0.0], atol=1e-12)


def test_plane_angle_opposite_normals_is_pi() -> None:
    """Przeciwne normalne płaszczyzn dają kąt pi."""
    # Arrange: normalna A = (0,0,1), normalna B = (0,0,-1)
    initial_a = np.array([[1.0, 0.0, 0.0]])
    final_a = np.array([[0.0, 1.0, 0.0]])
    initial_b = np.array([[0.0, 1.0, 0.0]])
    final_b = np.array([[1.0, 0.0, 0.0]])

    # Act
    result = plane.plane_angle(initial_a, final_a, initial_b, final_b)

    # Assert
    np.testing.assert_allclose(result, [np.pi])
