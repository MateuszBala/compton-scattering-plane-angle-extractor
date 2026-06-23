"""Testy szkieletu pakietu (smoke test po inicjalizacji)."""

import compton_scattering_plane_angle_extractor as pkg


def test_package_exposes_version() -> None:
    """Pakiet udostępnia atrybut ``__version__`` zgodny z konfiguracją."""
    # Arrange / Act
    version = pkg.__version__

    # Assert
    assert version == "0.0.0"
