"""Testy jednostkowe parsowania specyfikacji kolumn (``column_spec``)."""

import pytest

from compton_scattering_plane_angle_extractor import column_spec


def test_parse_column_spec_returns_triplet() -> None:
    """Poprawna specyfikacja zwraca trójkę nazw kolumn."""
    # Arrange
    spec = "px,py,pz"

    # Act
    result = column_spec.parse_column_spec(spec)

    # Assert
    assert result == column_spec.ColumnTriplet("px", "py", "pz")


def test_parse_column_spec_strips_whitespace() -> None:
    """Białe znaki wokół nazw kolumn są usuwane."""
    # Arrange
    spec = " px , py , pz "

    # Act
    result = column_spec.parse_column_spec(spec)

    # Assert
    assert result == column_spec.ColumnTriplet("px", "py", "pz")


def test_parse_column_spec_raises_for_wrong_count() -> None:
    """Inna liczba nazw niż trzy zgłasza ValueError."""
    # Arrange
    spec = "px,py"

    # Act / Assert
    with pytest.raises(ValueError):
        column_spec.parse_column_spec(spec)


def test_parse_column_spec_raises_for_empty_name() -> None:
    """Pusta nazwa kolumny zgłasza ValueError."""
    # Arrange
    spec = "px,,pz"

    # Act / Assert
    with pytest.raises(ValueError):
        column_spec.parse_column_spec(spec)
