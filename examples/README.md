# Przykłady

Ten katalog zawiera przykładowe dane i skrypty pokazujące użycie narzędzia.

## Zawartość

- `data/example_scattering.csv` — przykładowy plik wejściowy z kolumnami składowych
  pędu przed i po rozproszeniu dla dwóch płaszczyzn (A i B):
  - `a0x, a0y, a0z` — pęd przed rozproszeniem w płaszczyźnie A,
  - `a1x, a1y, a1z` — pęd po rozproszeniu w płaszczyźnie A,
  - `b0x, b0y, b0z` — pęd przed rozproszeniem w płaszczyźnie B,
  - `b1x, b1y, b1z` — pęd po rozproszeniu w płaszczyźnie B.
- `run_csv_file_analysis.sh` — uruchamia narzędzie na powyższych danych i zapisuje
  wynik (kąty w stopniach) do katalogu `examples/output`.
- `data/example_scattering_extra_columns.csv` — te same wektory pędu co wyżej, ale
  z dodatkowymi kolumnami (`event_id`, `energy_keV`, `detector`, `weight`), które
  nie są używane przez narzędzie.
- `run_csv_file_analysis_extra_columns.sh` — uruchamia narzędzie na danych z
  dodatkowymi kolumnami; wynik jest identyczny z `run_csv_file_analysis.sh`, co
  pokazuje, że wczytywane są wyłącznie wskazane kolumny wektorów pędu.

Analogiczne pliki w formacie HDF5 (każda kolumna to osobny zbiór danych):

- `data/example_scattering.h5` — odpowiednik `example_scattering.csv`.
- `run_hdf5_file_analysis.sh` — uruchamia narzędzie na pliku HDF5; format wyjścia
  jest domyślnie taki sam jak wejścia (HDF5).
- `data/example_scattering_extra_columns.h5` — odpowiednik wariantu z dodatkowymi
  kolumnami (zbiory `event_id`, `energy_keV`, `detector`, `weight` są ignorowane).
- `run_hdf5_file_analysis_extra_columns.sh` — uruchamia narzędzie na pliku HDF5 z
  dodatkowymi kolumnami; wynik zawiera te same wartości co `run_hdf5_file_analysis.sh`.

## Uruchomienie

Najpierw zainstaluj zależności (z katalogu głównego repozytorium):

```bash
make install
```

Następnie uruchom przykład:

```bash
bash examples/run_csv_file_analysis.sh
```

Wynik pojawi się w pliku
`examples/output/compton-scattering-plane-angles.csv` z kolumnami
`thetaA`, `phiA`, `thetaB`, `phiB`, `planeAngle`.

## Ignorowanie dodatkowych kolumn

Narzędzie czyta tylko kolumny wskazane w argumentach, więc dodatkowe kolumny w
pliku wejściowym są pomijane. Uruchom drugi przykład:

```bash
bash examples/run_csv_file_analysis_extra_columns.sh
```

a następnie porównaj oba wyniki — są identyczne:

```bash
diff examples/output/compton-scattering-plane-angles.csv \
     examples/output/compton-scattering-plane-angles-extra-columns.csv
```

## Przykłady HDF5

Te same scenariusze działają dla plików HDF5:

```bash
bash examples/run_hdf5_file_analysis.sh
bash examples/run_hdf5_file_analysis_extra_columns.sh
```

Wynik trafia do plików `examples/output/compton-scattering-plane-angles.hdf5` oraz
`compton-scattering-plane-angles-extra-columns.hdf5`. Pliki HDF5 są binarne, więc do
porównania wartości najwygodniej wczytać je ponownie, np.:

```bash
uv run python -c "
from compton_scattering_plane_angle_extractor.io.readers import load_data
print(load_data('examples/output/compton-scattering-plane-angles.hdf5'))
"
```

Wyniki dla wejścia CSV i HDF5 (oraz wariantów z dodatkowymi kolumnami) zawierają te
same wartości kątów — różni je jedynie format zapisu.
