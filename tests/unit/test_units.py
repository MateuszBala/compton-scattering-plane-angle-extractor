"""Testy jednostkowe konwersji jednostek (``units``)."""

import numpy as np

from compton_scattering_plane_angle_extractor import units


def test_rad_to_deg_converts_radians_to_degrees() -> None:
    """Konwersja radianów na stopnie zwraca poprawne wartości."""
    # Arrange
    angles = np.array([0.0, np.pi / 2, np.pi])

    # Act
    result = units.rad_to_deg(angles)

    # Assert
    np.testing.assert_allclose(result, [0.0, 90.0, 180.0])


def test_wrap_to_two_pi_shifts_negative_angles() -> None:
    """Ujemne kąty są przesuwane do zakresu [0, 2*pi)."""
    # Arrange
    phi = np.array([-np.pi / 2])

    # Act
    result = units.wrap_to_two_pi(phi)

    # Assert
    np.testing.assert_allclose(result, [3.0 * np.pi / 2])


def test_wrap_to_two_pi_keeps_nonnegative_angles() -> None:
    """Nieujemne kąty pozostają bez zmian."""
    # Arrange
    phi = np.array([0.0, np.pi / 2])

    # Act
    result = units.wrap_to_two_pi(phi)

    # Assert
    np.testing.assert_allclose(result, [0.0, np.pi / 2])
