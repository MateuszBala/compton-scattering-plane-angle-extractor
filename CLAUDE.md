# CLAUDE.md

## Rola pliku

Ten plik zawiera stałe instrukcje projektowe dla Claude Code. Traktuj go jako zwięzły
kontekst startowy, a szczegółowe zasady sprawdzaj w dokumentach z `docs/`.

## Źródła zasad

- `docs/CODING_CONVENTIONS.md` - standard Python, type hints, Ruff, MyPy.
- `docs/TESTING_CONVENTIONS.md` - testy Python z pytest i AAA pattern.
- `docs/DOCUMENTATION_CONVENTIONS.md` - docstrings NumPy style i dokumentacja.
- `docs/SCRIPTING_CONVENTIONS.md` - standard skryptów bash.
- `docs/COMMIT_CONVENTIONS.md` - format commitów i tytułów PR.
- `docs/CONTRIBUTION.md` - workflow kontrybucji i wymagania PR.

Jeśli reguły są niepełne albo sprzeczne, stosuj najbardziej konkretną zasadę z `docs/`.

## Kontekst projektu

- Repozytorium zawiera narzędzie do obliczania kątów płaszczyzn rozpraszania Comptonowskiego.
- Projekt napisany w Python 3.11+ z wykorzystaniem NumPy i Pandas.
- Manager projektów: `uv` (instalacja zależności, Virtual Environment).
- Priorytetem jest wydajność obliczeń numerycznych i przejrzystość kodu.
- Główna funkcjonalność: wczytywanie danych (CSV/HDF5) → obliczanie kątów → zapis wyników.
- Nie dodawaj nowych procesów fizycznych ani zmieniaj interfejsu CLI bez wyraźnej prośby.
- Nie zmieniaj nazw flag, formatów wejścia/wyjścia ani struktury danych bez uzasadnienia.

## Struktura repozytorium

- `.github/` - workflowy CI/CD, szablony i instrukcje agentów.
- `docs/` - obowiązujące konwencje i dokumentacja projektu.
- `src/compton-scattering-plane-angle-extractor/` - kod źródłowy Python (moduły i CLI).
  - `__init__.py` - inicjalizacja pakietu.
  - `angle_calculator.py` - główne obliczenia kątów.
  - `data_loader.py` - wczytywanie danych CSV/HDF5.
  - `output_writer.py` - zapis wyników.
  - `cli.py` - interfejs linii komend.
- `tests/` - testy aplikacji.
  - `unit/` - testy jednostkowe (test_<module>.py).
  - `integration/` - testy integracyjne.
  - `conftest.py` - wspólne fixtures pytest.
- `scripts/` - skrypty bash do uruchamiania, testów, itp.
- `pyproject.toml` - konfiguracja projektu (uv, pytest, Ruff, MyPy).
- `README.md` - dokumentacja główna projektu.

## Komendy

Używaj komend opisanych w README:

- Instalacja zależności: `uv sync`.
- Uruchamianie aplikacji: `python -m compton-scattering-plane-angle-extractor.cli ...`.
- Testy: `uv run pytest`.
- Linting i formatowanie: `uv run ruff check` / `uv run ruff format`.
- Type checking: `uv run mypy src/`.

Nie uruchamiaj komend przeznaczonych wyłącznie dla człowieka zespołu:

- `uv lock` (zarządzanie lock-file).
- Publikacja pakietu (jeśli niezbędne).

## Interfejs CLI

Główny skrypt: `python -m compton-scattering-plane-angle-extractor.cli`

Wymagane argumenty:

- `--input-file` lub `-i`: ścieżka do pliku CSV/HDF5 z danymi rozpraszania.
- `--output-dir` lub `-o`: ścieżka do folderu dla plików wyjściowych.
- `--first-scattering-initial-direction`: kolumny wejścia (x,y,z) dla pędu przed rozproszeniem w płaszczyźnie A.
- `--first-scattering-final-direction`: kolumny wejścia (x,y,z) dla pędu po rozproszeniu w płaszczyźnie A.
- `--second-scattering-initial-direction`: kolumny wejścia (x,y,z) dla pędu przed rozproszeniem w płaszczyźnie B.
- `--second-scattering-final-direction`: kolumny wejścia (x,y,z) dla pędu po rozproszeniu w płaszczyźnie B.

Opcjonalne argumenty:

- `--output-file-name`: nazwa pliku wyjściowego (domyślnie: `compton-scattering-plane-angles.<format>`).
- `--output-format`: format wyjścia (`csv` lub `hdf5`, domyślnie: format wejścia).
- `--rad2deg`: konwersja kątów z radianów na stopnie.

Zachowaj semantykę flag i interfejs bez zmian, chyba że użytkownik wyraźnie tego zażąda.

## Struktury danych wejścia i wyjścia

### Wejście

Plik CSV/HDF5 zawierający kolumny z wektorami pędu dla dwóch rozpraszań.
Użytkownik podaje nazwy kolumn jako argumenty.

### Wyjście

Plik CSV/HDF5 zawierający kolumny:

- `thetaA`: kąt rozpraszania w płaszczyźnie A (domyślnie rad, opcjonalnie deg).
- `phiA`: kąt azymutalny w płaszczyźnie A.
- `thetaB`: kąt rozpraszania w płaszczyźnie B.
- `phiB`: kąt azymutalny w płaszczyźnie B.
- `planeAngle`: kąt między płaszczyznami A i B.

Zawsze zachowuj tę strukturę i semantykę.

## Python

- Używaj Python 3.11+, bez żadnych starszych wersji.
- Kod ma kompilować się i przechodzić: `uv run ruff check`, `uv run ruff format --check`, `uv run mypy src/`.
- Stosuj wcięcie 4 spacje, maksymalna długość linii 88 znaków (Ruff default).
- Typ hints są obowiązkowe dla wszystkich funkcji publicznych.
- Nazwy funkcji i zmiennych: `snake_case`, klasy: `PascalCase`, stałe: `UPPERCASE_WITH_UNDERSCORES`.
- Wszystkie publiczne moduły, klasy, funkcje muszą mieć docstring w stylu NumPy.
- Docstring modułu zawiera: krótki opis, listę funkcji publicznych w formacie `funkcja(param: typ) -> typ`.
- Preferuj NumPy i Pandas dla obliczeń numerycznych, unikaj niskich pętli (vectorizuj).
- Preferuj `std::optional` równoważnik (typing.Optional, None zamiast wartości domyślnych).
- Unikaj zmiennych globalnych i stanu globalnego.
- Używaj logowania, nie `print()`, dla komunikatów diagnostycznych.

## Testy i walidacja

- Testy Python pisz w pytest.
- Nazwy plików testowych: `test_<module>.py`.
- Nazwy funkcji testowych: `test_<expected_outcome>` (opisują oczekiwane zachowanie).
- Stosuj Arrange-Act-Assert (AAA) dla każdego testu.
- Jeden test sprawdza jedno zachowanie; nie mieszaj wielu asercji dla różnych konceptów.
- Po zmianach w `src/` uruchom: `uv run pytest`, `uv run ruff check`, `uv run mypy src/`.
- Po zmianach w skryptach bash uruchom ShellCheck, jeśli jest dostępny.
- Przy zmianach dokumentacji wystarczy walidacja Markdown/diff, jeśli nie ma testu wykonywalnego.
- Coverage powinno być >= 80% (target 90%+).

## Bash

- Każdy skrypt zaczynaj nagłówkiem z polami `FILE`, `ABOUT`, `ARGUMENTS` i `USAGE`.
- Używaj `#!/bin/bash` oraz `set -euo pipefail`.
- Stosuj wcięcie 2 spacje i maksymalną długość linii 100 znaków.
- Warunki zapisuj z `[[ ]]`, zmienne cytuj jako `"${VAR}"`.
- Funkcje nazywaj `snake_case` i definiuj przez `function name() { ... }`.
- Zmienne globalne: `UPPERCASE_WITH_UNDERSCORES`, lokalne parametry z prefiksem `PARAM_`.
- Dokumentuj funkcje, parametry i kody zwrotu.

## Dokumentacja i język

- Dokumentacja wyjaśnia dlaczego kod istnieje, jak go używać i jakie są założenia.
- Aktualizuj README przy zmianach komend, flag, formatów wejścia/wyjścia lub workflow.
- Markdown jest samodzielny i jasny bez kontekstu zewnętrznego.
- Dokumentacja, komentarze w `.md`, `.py` i `.sh` muszą być pisane po polsku.
- Komunikaty dla użytkownika, logów i helpów CLI pisz po polsku.
- Commity, tytuły PR i nazwy gałęzi pisz po angielsku.

## Git i workflow

- Każda instancja agenta pracuje w osobnym worktree i zapisuje zmiany TYLKO w swoim worktree.
- Standardowo nie pracuj bezpośrednio na `main` ani `develop`; twórz gałąź od `develop`.
- Jedyny poprawny sposób tworzenia nowych worktree to `make worktree BRANCH_NAME=<nazwa>`.
- Jedyny poprawny sposób przechodzenia do worktree to `make switch-to-worktree BRANCH_NAME=<nazwa>`.
- Polecenie użytkownika `przejdź na branch <nazwa>` wykonuj priorytetowo i natychmiast.
- Przed przełączeniem gałęzi nie wykonuj żadnych innych działań roboczych.
- Jeśli wskazana gałąź nie istnieje, zapytaj użytkownika o zgodę na jej utworzenie.
- Po przełączeniu potwierdź aktywną gałąź i dopiero kontynuuj zadanie.
- Przed każdym commitem zweryfikuj, że aktywna gałąź należy do bieżącego worktree.
- Twardo zabrania się commitów z `develop` lub `main`, chyba że użytkownik jawnie to nakaże.
- Wyjątek: zmiany inicjalnego szkieletu projektu mogą być na `main`, jeśli użytkownik potwierdzi.
- Nie wykonuj commitów bez bezpośredniej prośby użytkownika.
- Format commita: `<type>(<scope>): <subject>` albo `<type>: <subject>`.
- Temat: tryb rozkazujący, mała litera, bez kropki, max 110 znaków.
- Commit obejmuje tylko pliki bezpośrednio związane z zadaniem.
- Nigdy nie wymuszaj ignorowanych plików (`git add -f`).
- Nigdy nie wysyłaj zmian z `.tmp/` do zdalnego repo.
- Jeśli użytkownik prosi o pliki w `.tmp/`, wykonaj tylko to i nie przygotowuj commita.

## Code review dla agenta

- Szukaj komentarzy CR wyłącznie w `.tmp/code-reviews` bieżącego worktree.
- Wybieraj najnowszy plik CR na podstawie znacznika czasu `-RRRRMMDD-HHMMSS`.
- Jeśli nie ma pliku CR, poproś członka zespołu o pobranie.
- Nigdy nie uruchamiaj `.github/get_review.sh` ani komend `gh`.

## Styl pracy agenta

- Preferuj minimalne, celowane zmiany.
- Najpierw czytaj dokumenty i testy kontrolujące zachowanie.
- Nie refaktoryzuj niezwiązanych fragmentów.
- Nie nadpisuj zmian użytkownika bez wyraźnej prośby.
- Pliki pomocnicze umieszczaj w `.tmp/<kategoria>/`.
- Po edycji uruchom najwęższą sensowną walidację i podaj wynik.