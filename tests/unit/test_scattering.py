"""Testy jednostkowe kątów rozpraszania i azymutalnych (``geometry.scattering``)."""

import numpy as np
import pytest

from compton_scattering_plane_angle_extractor.geometry import scattering


def test_reference_axis_raises_for_one_dimensional_input() -> None:
    """Pojedynczy wektor (3,) zgłasza czytelny ValueError zamiast IndexError."""
    # Arrange
    initial_unit = np.array([0.0, 0.0, 1.0])

    # Act / Assert
    with pytest.raises(ValueError):
        scattering.reference_axis(initial_unit)


def test_scattering_angle_perpendicular_is_half_pi() -> None:
    """Prostopadłe kierunki pędu dają kąt rozpraszania pi/2."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[0.0, 1.0, 0.0]])

    # Act
    result = scattering.scattering_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [np.pi / 2])


def test_scattering_angle_parallel_is_zero() -> None:
    """Równoległe kierunki pędu dają kąt rozpraszania 0."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[2.0, 0.0, 0.0]])

    # Act
    result = scattering.scattering_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [0.0], atol=1e-12)


def test_scattering_angle_antiparallel_is_pi() -> None:
    """Przeciwbieżne kierunki pędu dają kąt rozpraszania pi."""
    # Arrange
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[-1.0, 0.0, 0.0]])

    # Act
    result = scattering.scattering_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [np.pi])


def test_reference_axis_uses_z_for_small_z_component() -> None:
    """Dla |k0_z| < 0.9 oś referencyjna to (0, 0, 1)."""
    # Arrange
    initial_unit = np.array([[1.0, 0.0, 0.0]])

    # Act
    result = scattering.reference_axis(initial_unit)

    # Assert
    np.testing.assert_allclose(result, [[0.0, 0.0, 1.0]])


def test_reference_axis_uses_x_for_large_z_component() -> None:
    """Dla |k0_z| >= 0.9 oś referencyjna to (1, 0, 0)."""
    # Arrange
    initial_unit = np.array([[0.0, 0.0, 1.0]])

    # Act
    result = scattering.reference_axis(initial_unit)

    # Assert
    np.testing.assert_allclose(result, [[1.0, 0.0, 0.0]])


def test_azimuthal_angle_along_e2_is_half_pi() -> None:
    """Kierunek wzdłuż osi e2 daje kąt azymutalny pi/2."""
    # Arrange: k0 wzdłuż Z (oś referencyjna X), e1=(0,-1,0), e2=(1,0,0)
    initial = np.array([[0.0, 0.0, 1.0]])
    final = np.array([[1.0, 0.0, 0.0]])

    # Act
    result = scattering.azimuthal_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [np.pi / 2])


def test_azimuthal_angle_along_negative_e2_wraps_to_three_half_pi() -> None:
    """Kierunek przeciwny do e2 daje kąt azymutalny 3*pi/2 (po normalizacji)."""
    # Arrange
    initial = np.array([[0.0, 0.0, 1.0]])
    final = np.array([[-1.0, 0.0, 0.0]])

    # Act
    result = scattering.azimuthal_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [3.0 * np.pi / 2])


def test_azimuthal_angle_along_e1_is_zero() -> None:
    """Kierunek wzdłuż osi e1 daje kąt azymutalny 0."""
    # Arrange: k0 wzdłuż X (oś referencyjna Z), e1=(0,1,0), e2=(0,0,1)
    initial = np.array([[1.0, 0.0, 0.0]])
    final = np.array([[0.0, 1.0, 0.0]])

    # Act
    result = scattering.azimuthal_angle(initial, final)

    # Assert
    np.testing.assert_allclose(result, [0.0], atol=1e-12)
