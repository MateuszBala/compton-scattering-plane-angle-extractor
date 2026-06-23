"""Parsowanie i walidacja specyfikacji kolumn wektorów pędu.

Argument wiersza poleceń w formacie ``"x,y,z"`` opisuje nazwy kolumn będących
składowymi wektora pędu. Moduł zamienia go na zwalidowaną trójkę nazw.

Funkcje publiczne
-----------------
parse_column_spec(spec: str) -> ColumnTriplet
    Parsuje napis ``"x,y,z"`` na trójkę nazw kolumn ``(x, y, z)``.
"""

from typing import Final, NamedTuple

# Wymagana liczba składowych wektora (x, y, z).
COMPONENT_COUNT: Final[int] = 3


class ColumnTriplet(NamedTuple):
    """Trójka nazw kolumn opisujących składowe wektora pędu.

    Attributes
    ----------
    x, y, z : str
        Nazwy kolumn dla składowych odpowiednio ``x``, ``y`` i ``z``.
    """

    x: str
    y: str
    z: str


def parse_column_spec(spec: str) -> ColumnTriplet:
    """Parsuje specyfikację kolumn ``"x,y,z"`` na :class:`ColumnTriplet`.

    Parameters
    ----------
    spec : str
        Napis z nazwami kolumn rozdzielonymi przecinkami, np. ``"px,py,pz"``.
        Białe znaki wokół nazw są usuwane.

    Returns
    -------
    ColumnTriplet
        Trójka nazw kolumn ``(x, y, z)``.

    Raises
    ------
    ValueError
        Gdy specyfikacja nie zawiera dokładnie trzech nazw albo którakolwiek
        nazwa jest pusta.

    Examples
    --------
    >>> parse_column_spec("px, py, pz")
    ColumnTriplet(x='px', y='py', z='pz')
    """
    names = [name.strip() for name in spec.split(",")]
    if len(names) != COMPONENT_COUNT:
        raise ValueError(
            "Specyfikacja kolumn musi zawierać dokładnie trzy nazwy rozdzielone "
            f'przecinkami (x,y,z), otrzymano: "{spec}".'
        )
    if any(not name for name in names):
        raise ValueError(f'Nazwy kolumn nie mogą być puste, otrzymano: "{spec}".')
    return ColumnTriplet(names[0], names[1], names[2])
