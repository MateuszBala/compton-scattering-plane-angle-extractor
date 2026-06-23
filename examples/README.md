# Przykłady

Ten katalog zawiera przykładowe dane i skrypt pokazujący użycie narzędzia.

## Zawartość

- `data/example_scattering.csv` — przykładowy plik wejściowy z kolumnami składowych
  pędu przed i po rozproszeniu dla dwóch płaszczyzn (A i B):
  - `a0x, a0y, a0z` — pęd przed rozproszeniem w płaszczyźnie A,
  - `a1x, a1y, a1z` — pęd po rozproszeniu w płaszczyźnie A,
  - `b0x, b0y, b0z` — pęd przed rozproszeniem w płaszczyźnie B,
  - `b1x, b1y, b1z` — pęd po rozproszeniu w płaszczyźnie B.
- `run_csv_file_analysis.sh` — uruchamia narzędzie na powyższych danych i zapisuje
  wynik (kąty w stopniach) do katalogu `examples/output`.

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
