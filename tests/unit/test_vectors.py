"""Testy jednostkowe operacji na wektorach (``geometry.vectors``)."""

import numpy as np
import pytest

from compton_scattering_plane_angle_extractor.geometry import vectors


def test_normalize_returns_unit_vectors() -> None:
    """Normalizacja zwraca wektory o długości jednostkowej."""
    # Arrange
    raw = np.array([[3.0, 4.0, 0.0]])

    # Act
    result = vectors.normalize(raw)

    # Assert
    np.testing.assert_allclose(result, [[0.6, 0.8, 0.0]])


def test_normalize_raises_for_zero_vector() -> None:
    """Normalizacja wektora zerowego zgłasza ValueError."""
    # Arrange
    raw = np.array([[0.0, 0.0, 0.0]])

    # Act / Assert
    with pytest.raises(ValueError):
        vectors.normalize(raw)


def test_normalize_raises_for_one_dimensional_input() -> None:
    """Normalizacja pojedynczego wektora (3,) zgłasza ValueError o kształcie."""
    # Arrange
    raw = np.array([3.0, 4.0, 0.0])

    # Act / Assert
    with pytest.raises(ValueError):
        vectors.normalize(raw)


def test_ensure_vector_array_raises_for_wrong_last_dimension() -> None:
    """Walidacja zgłasza ValueError, gdy ostatni wymiar nie ma 3 składowych."""
    # Arrange
    raw = np.array([[1.0, 2.0]])

    # Act / Assert
    with pytest.raises(ValueError):
        vectors.ensure_vector_array(raw)


def test_ensure_vector_array_accepts_valid_shape() -> None:
    """Walidacja przepuszcza poprawną tablicę o kształcie (N, 3)."""
    # Arrange
    raw = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    # Act
    result = vectors.ensure_vector_array(raw)

    # Assert
    assert result is None


def test_dot_computes_rowwise_scalar_product() -> None:
    """Iloczyn skalarny jest liczony wierszami."""
    # Arrange
    left = np.array([[1.0, 2.0, 3.0]])
    right = np.array([[4.0, 5.0, 6.0]])

    # Act
    result = vectors.dot(left, right)

    # Assert
    np.testing.assert_allclose(result, [32.0])


def test_cross_computes_rowwise_vector_product() -> None:
    """Iloczyn wektorowy jest liczony wierszami."""
    # Arrange
    left = np.array([[1.0, 0.0, 0.0]])
    right = np.array([[0.0, 1.0, 0.0]])

    # Act
    result = vectors.cross(left, right)

    # Assert
    np.testing.assert_allclose(result, [[0.0, 0.0, 1.0]])


def test_clip_cosine_limits_values_to_unit_range() -> None:
    """Przycinanie kosinusa ogranicza wartości do zakresu [-1, 1]."""
    # Arrange
    values = np.array([1.5, -1.5, 0.5])

    # Act
    result = vectors.clip_cosine(values)

    # Assert
    np.testing.assert_allclose(result, [1.0, -1.0, 0.5])
