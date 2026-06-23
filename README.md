# compton-scattering-plane-angle-extractor

[![CI](https://github.com/MateuszBala/compton-scattering-plane-angle-extractor/actions/workflows/ci.yaml/badge.svg)](https://github.com/MateuszBala/compton-scattering-plane-angle-extractor/actions/workflows/ci.yaml)
[![Wersja](https://img.shields.io/badge/wersja-0.0.0-informational)](https://github.com/MateuszBala/python-cspae/releases)
[![Standard Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)]()
[![Standard Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)]()
[![Standard Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)]()
[![Standard Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)]()
[![Licencja](https://img.shields.io/badge/licencja-GPL--3.0-brightgreen)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Narzędzie do wyznaczania kątów rozpraszania Comptonowskiego na podstawie wektorów pędu przed i po rozproszeniu: kątów rozpraszania (θ) i azymutalnych (φ) w dwóch płaszczyznach rozpraszania (A i B) oraz kąta pomiędzy tymi płaszczyznami. Obliczenia są w pełni wektoryzowane (NumPy), co pozwala wydajnie przetwarzać duże zbiory zdarzeń, a dane wejściowe i wyniki obsługiwane są w formatach CSV oraz HDF5. Implementacja jest deterministyczna i pokryta testami, stanowiąc jednoznaczny, referencyjny punkt odniesienia dla poprawności tych wyliczeń.

## Metoda wyznaczania kątów

Bazuje na dwóch parach wektorów jednostkowych $\|\hat{k}\|=1$:

- $(\hat{k_0}_a,\hat{k}_a)$ - kierunek pędu przed i po rozporoszeniu tworzące płaszczyznę rozpraszania A
- $(\hat{k_0}_b,\hat{k}_b)$ - kierunek pędu przed i po rozporoszeniu tworzące płaszczyznę rozpraszania B

Kąty rozproszenia $\theta\in [0,\pi]$ jest dany z równania

$$
\boxed{
\hat{k_0}\cdot\hat{k} = \cos\theta
}
$$

Azymutalny kąt rozpraszania $\varphi\in (-\pi,\pi]$ wyznaczany jest z:


$$
\boxed{
\varphi =
\text{atan2}
\left[
\hat{k}\cdot \hat{e}_2,
\hat{k}\cdot \hat{e}_1
\right]
}
$$

gdzie

$$
\boxed{
\hat{\mathbf e}_1 =
\frac{\hat a \times \hat k_0}
{|\hat a \times \hat k_0|}
}
$$

$$
\boxed{
\hat{ \mathbf e}_2 =
\hat k_0 \times \hat e_1.
}
$$

$$
\boxed{
\hat{\mathbf a} =
\begin{cases}
(0,0,1), & \text{gdy } |\hat{k_0}_z| < 0.9,\\
(1,0,0), & \text{gdy } |\hat{k_0}_z| \ge 0.9.
\end{cases}
}
$$

Na potrzeby dalszych analiz kąt $\varphi$ jest transformowany do zakresu $\varphi\in [0,2\pi)$ za pomocą

$$
\boxed{
\varphi =
\begin{cases}
\varphi, & \text{gdy } \varphi  \ge 0,\\
\varphi+2\pi, & \text{gdy } \varphi < 0.
\end{cases}
}
$$

Kąt pomiędzy płaszczyznami rozpraszania $\phi\in[0,\pi]$:

$$
\boxed{
\phi = \arccos\left(\hat{n}_a\cdot\hat{n}_b\right)
}
$$

gdzie $\hat{n}_Q$ to wektor normalny do płaszczyzny rozpraszania $\text{Q}=\{\text{a},\text{b}\}$:

$$
\boxed{
\hat{n}_a = \frac{\hat{k_0}_a\times\hat{k}_a}{\|\hat{k_0}_a\times\hat{k}_a\|}
}
$$

$$
\boxed{
\hat{n}_b = \frac{\hat{k_0}_b\times\hat{k}_b}{\|\hat{k_0}_b\times\hat{k}_b\|}
}
$$

## Szybki start

### Instalacja (użytkownik końcowy)

Narzędzie instaluje się w izolowanym środowisku wirtualnym Pythona. Wymagany jest
tylko interpreter Pythona w wersji `>= 3.11` — instalacja nie modyfikuje globalnego
Pythona ani jego pakietów i nie wymaga narzędzia `uv`.

```bash
bash scripts/install.sh
```

Konfiguracja zmiennymi środowiskowymi (opcjonalnie):

- `PYTHON` — interpreter użyty do utworzenia środowiska (domyślnie `python3`),
  np. `PYTHON=python3.11 bash scripts/install.sh`.
- `CSPAE_VENV_DIR` — katalog środowiska wirtualnego (domyślnie
  `${CSPAE_HOME:-$HOME/.local/share/cspae}/venv`).

Na klastrze obliczeniowym (HPC) wykonaj instalację na węźle dostępowym (z dostępem
do internetu), a uruchamiaj narzędzie na węźle obliczeniowym, wskazując ten sam
katalog `CSPAE_VENV_DIR` (współdzielony system plików). Skrypt uruchomieniowy nie
wymaga aktywacji środowiska.

### Instalacja (developer)

W repozytorium do pracy nad kodem używamy menedżera `uv`:

```bash
make init
make install
```

### Użycie

```bash
bash scripts/extractor.sh \
  --input-file-path <path-to-file> \
  --output-dir-path <path-to-dir> \
  --first-scattering-initial-direction x,y,z \
  --first-scattering-final-direction x,y,z \
  --second-scattering-initial-direction x,y,z \
  --second-scattering-final-direction x,y,z \
  [--output-file-name NAME] \
  [--output-format csv|hdf5] \
  [--rad2deg]
```


| Komenda | Obowiązkowa                  | Opis |
| ---     | ---                          | ---  |
| `--input-file-path`                    | Tak/Nie     | ścieżka do pliku wejściowego CSV/HDF5  |
| `--output-dir-path`                    | Tak/Nie     | ścieżka do folderu gdzie zapisać dane |
| `--first-scattering-initial-direction` | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu przed rozproszeniem w płaszczyźnie A  |
| `--first-scattering-final-direction`   | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu po rozproszeniu w płaszczyźnie A  |
| `--second-scattering-initial-direction`| Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu przed rozproszeniem w płaszczyźnie B  |
| `--second-scattering-final-direction`  | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu po rozproszeniu w płaszczyźnie B  |
| `--output-file-name`                   | Tak/Nie     | nazwa pliku wyjściowego, domyślna nazwa to `compton-scattering-plane-angles.<format>` gdzie format jest taki sam jak plik wejściowy  |
| `--output-format`                      | Tak/Nie     | format pliku wyjściowego: CSF,HDF5  |
| `--rad2deg`                            | Nie         | jeśli flaga jest ustawiona to wartości kątów w kolumnach pliku wyjściowego są wyrażone w stopniach; domyślnie kąty są wyrażone w radianach |


## Format pliku wyjściowego

### Struktura

Niezależnie czy CSV czy HDF5 plik wyjściowy ma następujące kolumny

- `thetaA` : kąt rozpraszania w płaszczyźnie rozpraszania A
- `phiA` : azymutalny kąt rozpraszania w płaszczyźnie rozpraszania A
- `thetaB` : kąt rozpraszania w płaszczyźnie rozpraszania B
- `phiB`: azymutalny kąt rozpraszania w płaszczyźnie rozpraszania B
- `planeAngle`: kąt pomiędzy płaszczyną rozpraszania A a płaszczyną B

Domyślnie kąty są wyrażane w **radianach** [rad], ale użytkownik może ustawić aby te kąty były wrażane w **stopniach** [deg] poprzez ustawienie flagii `--rad2deg`.

### Format

Jeśli użytkownik nie ustawi formatu pliku wyjściowego za pomocą komendy `--output-format` to format pliku wyjściowego jest taki sam jak pliku wejściowego.

## Struktura repozytorium

```
compton-scattering-plane-angle-extractor/
├── .github/
│   ├── workflows/
│   │   └── ci.yaml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── copilot-instructions.md
│   └── get_review.sh
├── docs/
│   ├── CODING_CONVENTIONS.md
│   ├── COMMIT_CONVENTIONS.md
│   ├── CONTRIBUTION.md
│   ├── DOCUMENTATION_CONVENTIONS.md
│   ├── README.md
│   ├── SCRIPTING_CONVENTIONS.md
│   └── TESTING_CONVENTIONS.md
├── examples/
│   ├── data/
│   ├── run_csv_file_analysis.sh
│   ├── run_csv_file_analysis_extra_columns.sh
│   ├── run_hdf5_file_analysis.sh
│   ├── run_hdf5_file_analysis_extra_columns.sh
│   └── README.md
├── scripts/
│   ├── extractor.sh
│   ├── install.sh
│   └── run_tests.sh
├── src/
│   └── compton_scattering_plane_angle_extractor/
│       ├── geometry/
│       ├── io/
│       ├── cli.py
│       ├── config.py
│       ├── column_spec.py
│       ├── pipeline.py
│       ├── units.py
│       ├── logging_setup.py
│       └── __main__.py
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── pyproject.toml
├── LICENSE
├── README.md
└── Makefile
```

## Licencja

GNU General Public License v3.0

Kontakt: [GitHub](https://github.com/MateuszBala)

## Autor

Projekt został zaprojektowany i wykonany przez **Mateusz Jakub Bała**.

Kontakt: [GitHub](https://github.com/MateuszBala)

## Kontrybucja

Chcąc dodać nową funkcjonalność należy:

- stworzyć branch dziedziczący od `develop`
- wprowadzać zmiany zgodnie z [zasdami dla commitów](docs/COMMIT_CONVENTIONS.md)
- owtorzyć PR zgdonie z [wzorcem PR](.github/PULL_REQUEST_TEMPLATE.md)
- przestrzegać [zasad kontrybucji](docs/CONTRIBUTION.md)

