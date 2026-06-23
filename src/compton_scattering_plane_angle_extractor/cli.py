"""Interfejs linii komend pakietu.

Moduł definiuje punkt wejścia uruchamiany przez ``python -m
compton_scattering_plane_angle_extractor`` oraz skrypty konsolowe
``compton-scattering-plane-angle-extractor`` i ``cspae``.

Funkcje publiczne
-----------------
main(argv: list[str] | None = None) -> int
    Parsuje argumenty, uruchamia potok obliczeń i zwraca kod wyjścia.
"""


def main(argv: list[str] | None = None) -> int:
    """Uruchamia narzędzie z poziomu linii komend.

    Parameters
    ----------
    argv : list[str] | None
        Lista argumentów do sparsowania. Gdy ``None``, użyte zostaną argumenty
        z ``sys.argv``.

    Returns
    -------
    int
        Kod wyjścia procesu (0 oznacza sukces).

    Raises
    ------
    NotImplementedError
        Implementacja zostanie dodana w etapie interfejsu CLI.
    """
    raise NotImplementedError("Interfejs CLI zostanie zaimplementowany w etapie 4.")
