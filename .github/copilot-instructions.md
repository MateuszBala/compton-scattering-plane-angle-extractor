# Copilot Instructions

## Cel projektu

To repozytorium zawiera narzędzie do obliczania kątów płaszczyzn rozpraszania Comptonowskiego.
Projekt jest napisany w Python 3.11+ z wykorzystaniem NumPy i Pandas.
Główny cel to wysoka wydajność obliczeń numerycznych i przejrzysty, dokumentowany kod.

## Źródła zasad

Traktuj pliki w `docs/` jako obowiązujące źródło zasad projektu:

- `docs/CODING_CONVENTIONS.md` - standard Python, type hints, Ruff, MyPy.
- `docs/TESTING_CONVENTIONS.md` - testy Python z pytest i AAA pattern.
- `docs/DOCUMENTATION_CONVENTIONS.md` - docstrings NumPy style i dokumentacja.
- `docs/SCRIPTING_CONVENTIONS.md` - standard skryptów bash.
- `docs/COMMIT_CONVENTIONS.md` - format commitów i tytułów PR.
- `docs/CONTRIBUTION.md` - workflow kontrybucji i wymagania PR.

Jeśli te instrukcje i dokumenty w `docs/` różnią się szczegółem, stosuj bardziej konkretną zasadę z `docs/`.

## Kontekst techniczny narzędzia

- Narzędzie wczytuje dane rozpraszania z CSV lub HDF5.
- Oblicza kąty rozpraszania (theta), kąty azymutalne (phi) i kąty między płaszczyznami.
- Obsługuje konwersję jednostek (radiany ↔ stopnie).
- Interfejs CLI pozwala na wybór kolumn wejścia i formatu wyjścia.
- Nie dodawaj nowych procesów fizycznych bez bezpośredniej prośby.
- Nie zmieniaj interfejsu CLI ani nazw flag bez wyraźnej potrzeby.

## Struktura repozytorium

- `.github/`: workflowy CI/CD, szablony issue/PR i instrukcje Copilota.
- `docs/`: dokumentacja projektu, konwencje i zasady kontrybucji.
- `src/compton-scattering-plane-angle-extractor/`: kod źródłowy Python (moduły, CLI).
  - `__init__.py` - inicjalizacja pakietu.
  - `angle_calculator.py` - główne obliczenia kątów.
  - `data_loader.py` - wczytywanie danych CSV/HDF5.
  - `output_writer.py` - zapis wyników.
  - `cli.py` - interfejs linii komend.
- `tests/`: testy aplikacji.
  - `unit/` - testy jednostkowe (`test_<module>.py`).
  - `integration/` - testy integracyjne.
  - `conftest.py` - wspólne fixtures pytest.
- `scripts/`: skrypty bash do uruchamiania, testów, itp.
- `pyproject.toml` - konfiguracja projektu (uv, pytest, Ruff, MyPy).
- `README.md` - dokumentacja główna projektu.

## Build i testy

Używaj komend opisanych w README:

- `uv sync` - instalacja zależności.
- `uv run pytest` - uruchomienie testów.
- `uv run ruff check` - linting.
- `uv run ruff format` - formatowanie kodu.
- `uv run mypy src/` - type checking.

Przy zmianach w `src/` po edycji uruchom:
- `uv run pytest` (minimalne testy).
- `uv run ruff check && uv run ruff format --check` (walidacja stylu).
- `uv run mypy src/` (type checking).

Przy zmianach w skryptach bash używaj ShellCheck, jeśli jest dostępny.
Przy zmianach dokumentacji wystarczy walidacja Markdown/diff, jeśli nie ma testu wykonywalnego.

## Uruchamianie narzędzia

Uruchamiaj aplikację przez `python -m compton-scattering-plane-angle-extractor.cli`.

Wymagane argumenty:

- `--input-file` lub `-i`: ścieżka do pliku CSV/HDF5 z danymi.
- `--output-dir` lub `-o`: ścieżka do folderu dla wyjścia.
- `--first-scattering-initial-direction`: kolumny (x,y,z) dla pędu przed rozproszeniem A.
- `--first-scattering-final-direction`: kolumny (x,y,z) dla pędu po rozproszeniu A.
- `--second-scattering-initial-direction`: kolumny (x,y,z) dla pędu przed rozproszeniem B.
- `--second-scattering-final-direction`: kolumny (x,y,z) dla pędu po rozproszeniu B.

Opcjonalne argumenty:

- `--output-file-name`: nazwa pliku wyjściowego (domyślnie: `compton-scattering-plane-angles.<format>`).
- `--output-format`: format wyjścia (`csv` lub `hdf5`, domyślnie: format wejścia).
- `--rad2deg`: konwersja kątów z radianów na stopnie.

Zasady uruchomienia:

- Folder wyjściowy musi istnieć (chyba że użytkownik doda flag tworzenia).
- Podaj dokładnie te kolumny, które użytkownik wskazuje jako argumenty.
- Zachowaj schemat CSV i semantykę kolumn.

## Struktury danych wejścia i wyjścia

### Wejście

Plik CSV lub HDF5 zawierający kolumny z wektorami pędu dla dwóch rozpraszań.
Użytkownik podaje nazwy kolumn jako argumenty CLI.

Przykład CSV:
```
k0_a_x, k0_a_y, k0_a_z, k_a_x, k_a_y, k_a_z, k0_b_x, k0_b_y, k0_b_z, k_b_x, k_b_y, k_b_z
1.0,    0.0,    0.0,    0.9,   0.436, 0.0,   0.8,    0.6,    0.0,    0.7,   0.7,   0.0
...
```

### Wyjście

Plik CSV lub HDF5 zawierający kolumny:

- `thetaA`: kąt rozpraszania w płaszczyźnie A (domyślnie rad, opcjonalnie deg).
- `phiA`: kąt azymutalny w płaszczyźnie A.
- `thetaB`: kąt rozpraszania w płaszczyźnie B.
- `phiB`: kąt azymutalny w płaszczyźnie B.
- `planeAngle`: kąt między płaszczyznami A i B.

Każdy rząd wyjścia odpowiada jednemu eventowi z wejścia.
Zachowuj tę strukturę i semantykę zawsze.

## Zasady Python

- Używaj wyłącznie Python 3.11+.
- Kod ma przechodzić: `ruff check`, `ruff format --check` i `mypy src/`.
- Wcięcie 4 spacje, maksimum 88 znaków na linię (Ruff default).
- Type hints obowiązkowe dla wszystkich funkcji publicznych.
- Nazwy: funkcje/zmienne `snake_case`, klasy `PascalCase`, stałe `UPPERCASE`.
- Każdy moduł, klasa, funkcja publiczna musi mieć docstring w stylu NumPy.
- Docstring modułu zawiera: opis, listę funkcji publicznych w formacie `funkcja(param: typ) -> typ`.
- Preferuj NumPy/Pandas dla obliczeń numerycznych, unikaj pętli (vectorizuj).
- Preferuj `typing.Optional` i `None` zamiast wartości domyślnych.
- Unikaj zmiennych globalnych i stanu globalnego.
- Używaj `logging` (nie `print()`), dla komunikatów diagnostycznych.
- Dokumentuj decyzje architektoniczne i złożoną logikę w komentarzach.

## Zasady testów

- Testy Python pisz w pytest.
- Pliki testów: `test_<module>.py`.
- Nazwy testów: `test_<expected_outcome>` (opisują zachowanie, nie implementację).
- Struktura: Arrange-Act-Assert (AAA).
- Jeden test = jedno zachowanie (nie mieszaj asercji dla różnych konceptów).
- Dodawaj testy dla: nowego kodu, ścieżek krytycznych, przypadków brzegowych, naprawianych błędów.
- Coverage >= 80% (target 90%+).
- Używaj fixtures dla wspólnego setupu.
- Parametryzuj testy dla wielu wejść.
- Mockuj zewnętrzne zależności (pliki, API), nie NumPy/Pandas.

## Zasady skryptów bash

- Każdy skrypt zaczynaj nagłówkiem: `FILE`, `ABOUT`, `ARGUMENTS`, `USAGE`.
- Shebang: `#!/bin/bash`, zawsze `set -euo pipefail`.
- Wcięcie 2 spacje, maksimum 100 znaków na linię.
- Warunki: `[[ ]]`, zmienne: `"${VAR}"`.
- Funkcje: `snake_case`, definiuj przez `function name() { ... }`.
- Zmienne globalne: `UPPERCASE_WITH_UNDERSCORES`.
- Parametry lokalne: prefiks `PARAM_`.
- Dokumentuj wszystkie funkcje: parametry, kody zwrotu.

## Zasady dokumentacji

- Dokumentacja wyjaśnia dlaczego kod istnieje, jak go używać i jakie są założenia.
- Aktualizuj README razem ze zmianami CLI, flag, formatów lub workflow.
- Markdown jest samodzielny i jasny bez kontekstu zewnętrznego.
- Komentarze w kodzie tylko gdzie wyjaśniają nietrywialne decyzje lub logikę.
- Docstrings NumPy: Summary, Extended Description, Parameters, Returns, Raises, Examples.
- Nie dodawaj generatorów dokumentacji bez wyraźnej potrzeby.

## Język

- Dokumentacja i komentarze w `.md`, `.py` i `.sh` muszą być pisane po polsku.
- Komunikaty CLI, logów i pomocy pisz po polsku.
- Commity, tytuły PR i nazwy gałęzi pisz po angielsku (patrz `docs/COMMIT_CONVENTIONS.md`).

## Workflow kontrybucji

- Standardowo nie pracuj na `main` ani `develop`; twórz gałąź od `develop`.
- Wyjątek: zmiany inicjalnego szkieletu projektu na `main`, jeśli użytkownik potwierdzi.
- Nazwy gałęzi: `feature/<description>`, `bugfix/<description>`, `docs/<description>` itp. (patrz `docs/CONTRIBUTION.md`).
- Format commita: `<type>(<scope>): <subject>` albo `<type>: <subject>`.
- Temat: tryb rozkazujący, mała litera, bez kropki, max 110 znaków.
- Nie commituj bez bezpośredniej prośby użytkownika.
- Commit obejmuje tylko pliki bezpośrednio związane z zadaniem.
- Przy zmianach w `src/` commituj dopiero po testach lub po odnotowaniu, że walidacja nie była możliwa.
- Nigdy nie wymuszaj ignorowanych plików (`git add -f`).
- Nigdy nie wysyłaj zmian z `.tmp/` do zdalnego repo.
- Pliki w `.tmp/`: tylko edycja/usuwanie, bez commitów.

## Pliki pomocnicze

Tworząc pomocnicze pliki, umieszczaj je w `.tmp/<kategoria>/`:

- `.tmp/scripts` - skrypty pomocnicze.
- `.tmp/docs` - dokumentacja pomocnicza.
- `.tmp/tests` - testy pomocnicze.
- `.tmp/artifacts` - artefakty pomocnicze.
- `.tmp/sessions` - sesje pomocnicze.
- `.tmp/other` - inne pliki.

## Jak Copilot powinien pomagać

- Preferuj minimalne, celowane zmiany.
- Przed większą zmianą przeczytaj dokumenty i testy kontrolujące zachowanie.
- Nie refaktoryzuj niezwiązanych fragmentów.
- Szanuj istniejący styl repo nawet wtedy, gdy dokumenty są szkicem.
- Po edycji uruchom najwęższą sensowną walidację i podaj wynik użytkownikowi.
- Sugeruj zmiany zgodne z konwencjami, ale nie wymuszaj ich bez zgody.

## Szczególne uwagi dla tego projektu

- Wszystkie obliczenia kątów muszą być numerycznie stabilne (unikaj dzielenia przez bardzo małe liczby).
- Zadbaj o wydajność przy przetwarzaniu dużych zbiorów danych (DataFrames z milionami wierszy).
- Zachowaj semantykę wyjścia nawet jeśli refaktoryzujesz wewnętrzne obliczenia.
- Kiedy zmieniasz strukturę danych wewnętrznych, upewnij się, że testy to akceptują.
