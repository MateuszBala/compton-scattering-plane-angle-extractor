# compton-scattering-plane-angle-extractor

Maksymalnie prosty i przetestowane narzędzie do wyliczania kąta pomiędzy płaszczynami rozpraszania Comptonowskiego. Stworzone tylko po to by nie podważać wątku "czy jest to dobrze wyliczone"

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
\operatorname{atan2}
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
(0,0,1), & \text{gdy } |\hat{k_0}_z| < 0.9,\\[4pt]
(1,0,0), & \text{gdy } |\hat{k_0}_z| \ge 0.9.
\end{cases}
}
$$

Na potrzeby dalszych analiz kąt $\varphi$ jest transformowany do zakresu $\varphi\in [0,2\pi)$ za pomocą

$$
\boxed{
\varphi =
\begin{cases}
\varphi, & \text{gdy } \varphi  \ge 0,\\[4pt]
\varphi+2\pi, & \text{gdy } \varphi < 0.
\end{cases}
}
$$

Kąt pomiędzy płaszczyznami rozpraszania $\phi\in[0,\pi]$:

$$
\boxed{
\phi = \hat{n}_a\times\hat{n}_b
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


### Instalacja

```bash
make init
make install
```

### Użycia

```bash
bash scripts/extract.sh \
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
| `--first-scattering-initial-direction` | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu przed rozrposzeniem w płaszczyźnie A  |
| `--first-scattering-final-direction`   | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu po rozrposzeniu w płaszczyźnie A  |
| `--second-scattering-initial-direction`| Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu przed rozrposzeniem w płaszczyźnie B  |
| `-second-scattering-final-direction`   | Tak/Nie     | nazwy kolumn będących składowymi (X,Y,Z) kierunku pędu po rozrposzeniu w płaszczyźnie B  |
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

