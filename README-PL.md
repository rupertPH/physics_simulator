# Symulator Układów Fizycznych

Projekt udostępnia zautomatyzowane środowisko do kompilacji numerycznego solvera (w języku C) oraz uruchamiania symulacji dynamicznych (w języku Python) dla różnych układów fizycznych. Obliczenia realizowane są za pomocą wydajnego algorytmu Rungego-Kutty 4. rzędu (RK4).

## Wymagania systemowe

Przed uruchomieniem upewnij się, że w Twoim systemie zainstalowane są:
*   **GNU Make**
*   **Kompilator GCC** (z obsługą flag `-shared` oraz `-fPIC`)
*   **Python 3** wraz z menedżerem pakietów `pip`

---

## Szybki start

### 1. Weryfikacja środowiska
Uruchom pełny test zgodności, aby sprawdzić obecność Pythona, kompilatora GCC oraz wymaganych bibliotek:
```bash
make check
```
*(Możesz też sprawdzać poszczególne elementy osobno za pomocą komend: `make check_python`, `make check_gcc` lub `make check_dependencies`)*

### 2. Instalacja zależności Pythona
Jeśli test zależności wykaże braki, zainstaluj wymagane pakiety poleceniem:
```bash
make install_dependencies
```

### 3. Kompilacja solvera dynamicznego
Sercem obliczeniowym projektu jest szybki solver napisany w C. Skompiluj go do biblioteki współdzielonej `.so`:
```bash
make compile_solver
```

### 4. Uruchomienie domyślnej symulacji
Po udanej kompilacji uruchom symulację z domyślnym plikiem konfiguracyjnym (wahadło podwójne):
```bash
make run
```

---

## Zaawansowane zarządzanie konfiguracją

Program pozwala na symulację różnych układów fizycznych. Możesz wybrać plik konfiguracji na **dwa sposoby**:

### Sposób 1: Przekazanie parametru w konsoli (Zalecane)
Nie musisz edytować kodu źródłowego. Możesz wskazać dowolny plik `.ini` bezpośrednio podczas wywoływania komendy `make run`, nadpisując zmienną `CONFIG`:

```bash
# Uruchomienie symulacji układu wielu klocków i sprężyn
make run CONFIG=config/config_multiple_spring_masses.ini

# Uruchomienie symulacji pojedynczego wahadła
make run CONFIG=config/config_pendulum.ini
```

### Sposób 2: Edycja pliku Makefile
Otwórz plik `Makefile` w edytorze tekstu i zmień aktywną zmienną `CONFIG` poprzez odkomentowanie właściwej linii, a zakomentowanie pozostałych znakami `#`:

```makefile
# Przykład zmiany w pliku Makefile:
# CONFIG=config/config_double_pendulum.ini
CONFIG=config/config_multiple_spring_masses.ini
```

### Dostępne szablony konfiguracji:
*   `config_double_pendulum.ini` – Wahadło podwójne (domyślne)
*   `config_pendulum.ini` – Wahadło pojedyncze
*   `config_spring_mass.ini` – Pojedynczy klocek na sprężynie
*   `config_multiple_spring_masses.ini` – Układ trzech klocków połączonych sprężynami

---

## Tworzenie własnego pliku konfiguracyjnego (*.ini)

Każdy układ fizyczny w projekcie definiowany jest za pomocą pliku tekstowego `*.ini`. Plik ten musi zachować ścisłą strukturę podzieloną na sekcje:

1.  **`[VARIABLES]`**
    *   `number_q` – liczba stopni swobody układu (liczba zmiennych opisujących ruch, np. `2` dla podwójnego wahadła, `3` dla trzech klocków).

2.  **`[PARAMETERS]`**
    *   Sekcja na stałe fizyczne układu: masy (`m1, m2...`), stałe sprężystości (`k1, k2...`), długości (`l1, d1...`) oraz przyspieszenie ziemskie (`g`).

3.  **`[INITIAL STATE]`**
    *   `q_start` – początkowe pozycje/kąty dla każdej zmiennej, rozdzielone przecinkami.
    *   `qd_start` – początkowe prędkości (pochodne pozycje po czasie) dla każdej zmiennej, rozdzielone przecinkami.

4.  **`[LAGRANGIAN]`**
    *   `L` – funkcja Lagrange'a układu ($L = T - V$, gdzie $T$ to energia kinetyczna, a $V$ to energia potencjalna). 
    *   **Zasady zapisu**: Używaj standardowych operatorów matematycznych (`*`, `/`, `**` do potęgowania) oraz funkcji trygonometrycznych typu `sin(...)` i `cos(...)`. Zmienne prędkości zapisuj jako `qd1, qd2`, a pozycje jako `q1, q2`.

5.  **`[2D VISUALIZATION]`**
    *   Definicje mapowania współrzędnych uogólnionych na rzeczywiste punkty na ekranie ($X, Y$) dla każdego elementu (np. `X1, Y1`, `X2, Y2`), używane do rysowania animacji.

6.  **`[RENDER]`**
    *   `scale` – mnożnik pikseli (skalowanie matematycznych odległości na ekran).
    *   `origin_x`, `origin_y` – punkt zakotwiczenia układu (środek ekranu/układu współrzędnych) w pikselach.

**Przykład:** Stwórz nowy plik `config/my_system.ini`, uzupełnij sekcje według powyższego schematu, a następnie uruchom poleceniem: `make run CONFIG=config/my_system.ini`.

---

## Czyszczenie projektu

Aby usunąć skompilowane pliki binarne solvera (`solver.so`) i przywrócić katalog do czystego stanu przed ponowną kompilacją, wykonaj:
```bash
make clean
```
