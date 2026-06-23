"""Konfiguracja logowania dla narzędzia.

Moduł konfiguruje logger pakietu (poziom, format, strumień), aby diagnostyka i
komunikaty dla użytkownika korzystały z modułu ``logging`` zamiast ``print``.

Funkcje publiczne
-----------------
configure_logging(level: int = logging.INFO) -> None
    Konfiguruje logger pakietu (idempotentnie).
get_logger(name: str) -> logging.Logger
    Zwraca logger o wskazanej nazwie.
"""

import logging
from typing import Final

# Nazwa głównego loggera pakietu.
LOGGER_NAME: Final[str] = "compton_scattering_plane_angle_extractor"

# Format komunikatów logowania.
LOG_FORMAT: Final[str] = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Konfiguruje logger pakietu.

    Funkcja jest idempotentna: ponowne wywołanie nie dodaje kolejnych
    procedur obsługi (``handler``), jedynie aktualizuje poziom logowania.

    Parameters
    ----------
    level : int
        Poziom logowania (np. ``logging.INFO``).
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Zwraca logger o wskazanej nazwie.

    Parameters
    ----------
    name : str
        Nazwa loggera (zwykle ``__name__`` modułu wywołującego).

    Returns
    -------
    logging.Logger
        Logger o wskazanej nazwie.
    """
    return logging.getLogger(name)
