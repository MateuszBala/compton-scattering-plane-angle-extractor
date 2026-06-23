"""Testy jednostkowe konfiguracji logowania (``logging_setup``)."""

import logging

from compton_scattering_plane_angle_extractor import logging_setup


def test_configure_logging_is_idempotent() -> None:
    """Wielokrotne wywołanie nie powiela procedur obsługi loggera."""
    # Arrange
    logger = logging.getLogger(logging_setup.LOGGER_NAME)
    logger.handlers.clear()

    # Act
    logging_setup.configure_logging()
    logging_setup.configure_logging()

    # Assert
    assert len(logger.handlers) == 1


def test_get_logger_returns_named_logger() -> None:
    """Funkcja zwraca logger o wskazanej nazwie."""
    # Arrange / Act
    logger = logging_setup.get_logger("przyklad")

    # Assert
    assert logger.name == "przyklad"
