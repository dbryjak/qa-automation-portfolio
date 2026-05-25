# Rozdział 10c — Automatyzacja testów krok po kroku
## Od zera do trzech poziomów — Monitor Tokenów jako przykład

**Poziom 1 (Unit testy):** ✅ Zrobione — 46 testów, 0 failed  
**Poziom 2 (Integration testy):** ✅ Zrobione — 18 testów, 0 failed  
**Poziom 3 (GUI testy):** 📝 Opisane — zaawansowane, opcjonalne  

---

## Zacznijmy od początku — czym są testy automatyczne?

Wyobraź sobie, że skończyłeś budować aplikację i chcesz sprawdzić czy działa.
Wchodzisz, klikasz, patrzysz — "OK, działa". Zapisujesz.

Tydzień później dodajesz nową funkcję. I znowu sprawdzasz ręcznie. I znowu. I znowu.
Po miesiącu masz 20 funkcji i żeby sprawdzić każdą — potrzebujesz godziny.

**Testy automatyczne rozwiązują ten problem.**

Zamiast klikać ręcznie, piszesz raz skrypt który:
1. Uruchamia funkcję z konkretnymi danymi wejściowymi
2. Sprawdza czy wynik jest taki jaki powinien być
3. Mówi "PASS" albo "FAIL"

I możesz uruchamiać ten skrypt w każdej chwili — zajmuje sekundy, nie godziny.

---

## Jak to wygląda w praktyce?

Mamy funkcję w naszej aplikacji:

```python
def czytaj_uzycie(claude_dir=None):
    """Czyta pliki JSONL i sumuje tokeny z dzisiaj."""
    ...
    return stats  # słownik z liczbą wywołań, tokenami, kosztem
```

Test automatyczny do tej funkcji wygląda tak:

```python
def test_wpis_dzisiejszy_jest_liczony(plik_jsonl):
    # 1. PRZYGOTUJ dane testowe
    katalog = plik_jsonl([wpis_jsonl(inp=1000, out=500)])

    # 2. URUCHOM testowaną funkcję
    stats = czytaj_uzycie(claude_dir=katalog)

    # 3. SPRAWDŹ czy wynik jest poprawny
    assert stats["liczba_wywolan"] == 1
    assert stats["tokeny_wejscia"] == 1000
```

Jeśli `assert` jest prawdziwy → **PASSED** (zielony).  
Jeśli `assert` jest fałszywy → **FAILED** (czerwony) — test wykrył błąd!

---

## Wzorzec AAA — Arrange, Act, Assert

Każdy dobry test ma trzy części. Po angielsku nazywa się to **AAA**:

```
ARRANGE  →  Przygotuj dane i środowisko
ACT      →  Uruchom testowaną funkcję
ASSERT   →  Sprawdź wynik
```

```python
def test_koszt_sonnet_input():
    # ARRANGE — przygotuj dane
    katalog = plik_jsonl([
        wpis_jsonl(model="claude-sonnet-4-6", inp=1_000_000, out=0)
    ])

    # ACT — uruchom
    stats = czytaj_uzycie(claude_dir=katalog)

    # ASSERT — sprawdź
    assert abs(stats["koszt_usd"] - 3.00) < 0.0001
```

Ten wzorzec stosuj zawsze. Testy które go nie mają są trudne do zrozumienia.

---

## Narzędzie: pytest

`pytest` to najpopularniejsza biblioteka do testów w Pythonie. Instaluje się ją raz:

```bash
pip install pytest
```

Uruchamiasz tak:

```bash
python -m pytest tests/ -v
```

`-v` (verbose) = pokaż każdy test z osobna (nie tylko podsumowanie).

Wynik:
```
tests/test_config.py::test_wczytuje_poprawny_json     PASSED  [ 2%]
tests/test_config.py::test_brakujacy_plik_zwraca_zera PASSED  [ 4%]
...
46 passed in 0.56s
```

---

## Trzy poziomy automatyzacji

```
┌─────────────────────────────────────────┐
│          POZIOM 3 — GUI / E2E           │  ← klika w prawdziwe okienko
│   pywinauto · powolne · kruche          │
├─────────────────────────────────────────┤
│        POZIOM 2 — Integration           │  ← testuje kilka rzeczy razem
│   prawdziwe pliki · prawdziwy config    │
├─────────────────────────────────────────┤
│          POZIOM 1 — Unit testy          │  ← testuje jedną funkcję
│   pytest · szybkie · izolowane         │  ← TUTAJ JESTEŚMY ✅
└─────────────────────────────────────────┘
```

Im wyżej tym: wolniej, trudniej napisać, trudniej utrzymać.
Im niżej tym: szybciej, łatwiej, bardziej niezawodnie.

**Zasada:** Jak najwięcej testów na dole. Jak najmniej na górze.

---

---

# POZIOM 1 — Unit testy ✅ ZROBIONE

## Co to jest unit test?

**Unit** (jednostka) = jedna funkcja, jeden fragment kodu.

Unit test sprawdza tę jedną funkcję **w izolacji** — bez prawdziwych plików,
bez internetu, bez bazy danych. Jeśli funkcja potrzebuje pliku — podajesz
jej tymczasowy plik stworzony specjalnie na potrzeby testu.

Dlatego unit testy są takie szybkie — nie ma żadnych opóźnień zewnętrznych.

## Jak zrobiliśmy izolację — fixtures

Żeby testy nie dotykały prawdziwych plików (`~/.claude/`, `config.json`),
używamy **fixtures** — funkcji przygotowujących tymczasowe środowisko.

```python
# conftest.py — fixtures automatycznie dostępne we wszystkich testach

@pytest.fixture
def katalog_claude(tmp_path):
    """tmp_path to magiczny fixture pytest — tworzy tymczasowy katalog
    który zostaje automatycznie usunięty po każdym teście."""
    projekty = tmp_path / "projects" / "test-projekt"
    projekty.mkdir(parents=True)
    return tmp_path

@pytest.fixture
def plik_jsonl(katalog_claude):
    """Zwraca funkcję która tworzy plik JSONL z podanymi wpisami."""
    def _tworz(wpisy, nazwa="test.jsonl"):
        p = katalog_claude / "projects" / "test-projekt" / nazwa
        p.write_text("\n".join(wpisy), encoding="utf-8")
        return katalog_claude
    return _tworz
```

Każdy test dostaje **świeży** tymczasowy katalog. Nie ma możliwości żeby
jeden test zabrudzić dane drugiego testu.

## Helper — wpis_jsonl()

Zamiast ręcznie pisać JSON w każdym teście, mamy helper:

```python
# helpers.py
def wpis_jsonl(model="claude-sonnet-4-6", inp=1000, out=500, cc=0, cr=0, data=None):
    """Tworzy jeden wpis JSONL w formacie jaki Claude Code zapisuje."""
    return json.dumps({
        "timestamp": f"{data or DZISIAJ}T12:00:00.000Z",
        "message": {
            "model": model,
            "usage": {
                "input_tokens": inp,
                "output_tokens": out,
                "cache_creation_input_tokens": cc,
                "cache_read_input_tokens": cr,
            },
        },
    })
```

Zamiast pisać 15 linii JSON — piszesz: `wpis_jsonl(inp=1000, out=500)`.

## Co przetestowaliśmy (46 testów)

### test_czytaj_uzycie.py — 14 testów

Testuje funkcję `czytaj_uzycie()` która czyta pliki JSONL i sumuje tokeny.

```
TestPusteŹródła (4 testy)
  ✅ pusty katalog zwraca zera
  ✅ brakujący katalog nie rzuca wyjątku
  ✅ pusty plik JSONL → zero wywołań
  ✅ plik z pustymi liniami → zero wywołań

TestFiltrowaniePoDacie (3 testy)
  ✅ wpis dzisiejszy jest liczony
  ✅ wpis wczorajszy jest pomijany
  ✅ mieszane daty — liczy tylko dzisiejsze

TestSumowaniaTokenów (4 testy)
  ✅ sumuje wejście i wyjście z wielu wpisów
  ✅ sumuje tokeny cache (create + read)
  ✅ pomija wpis gdzie wszystkie tokeny = 0
  ✅ pomija wpis bez sekcji "usage"

TestPodziałuModeli (3 testy)
  ✅ rozdziela wywołania per model
  ✅ nieznany model używa domyślnego cennika
  ✅ tokeny per model zliczane osobno
```

### test_koszty.py — 18 testów

Testuje ceny wszystkich modeli i funkcję `czytaj_wydatki_od()`.

```
TestCennikModeli (10 testów)
  ✅ claude-sonnet-4-6:  $3.00/M input,  $15.00/M output
  ✅ claude-opus-4-7:    $15.00/M input, $75.00/M output
  ✅ claude-haiku-4-5:   $0.80/M input,  $4.00/M output
  ✅ claude-haiku-4-5-20251001: tak samo jak haiku-4-5
  ✅ cache_create sonnet: $3.75/M
  ✅ cache_read sonnet:   $0.30/M
  ✅ suma wszystkich typów tokenów = poprawna

TestCzytajWydatkiOd (7 testów)
  ✅ liczy wydatki od podanej daty
  ✅ pomija wpisy sprzed daty
  ✅ sumuje wpisy z wielu dni
  ✅ niepoprawna data → zwraca 0.0
  ✅ pusty katalog → zwraca 0.0
```

### test_config.py — 11 testów

```
TestWczytajConfig (3 testy)
  ✅ poprawny JSON → zwraca słownik
  ✅ brakujący plik → zwraca {}
  ✅ błędny JSON → zwraca {}

TestZapiszTryb (4 testy)
  ✅ zapisuje tryb "api"
  ✅ zapisuje tryb "pro"
  ✅ zachowuje pozostałe klucze w pliku
  ✅ brakujący plik → nie rzuca wyjątku

TestAutoZapiszDateSalda (4 testy)
  ✅ dodaje datę gdy brak saldo_data_wpisania
  ✅ nie nadpisuje istniejącej daty
  ✅ bez saldo_api_usd → nic nie robi
  ✅ zapisuje datę do pliku config.json
```

### test_ikona.py — 7 testów

```
TestStworZIkone (7 testów)
  ✅ zwraca obiekt Image (PIL)
  ✅ rozmiar 64x64 pikseli
  ✅ tryb PRO → zielona ikona (próbka boku kółka)
  ✅ tryb API → niebieska ikona
  ✅ alarm=True → czerwona ikona
  ✅ PRO i API wyglądają różnie (różne bajty)
  ✅ alarm różni się od normalnej
```

## Wynik

```
============================= test session starts =============================
collected 46 items

tests/test_config.py         11 passed
tests/test_czytaj_uzycie.py  14 passed
tests/test_ikona.py           7 passed
tests/test_koszty.py         18 passed

============================== 46 passed in 0.56s =============================
```

## Czego nauczył mnie Poziom 1

**Refaktoryzacja pod testability** — zanim napisałem testy, musiałem zmienić
funkcje żeby przyjmowały ścieżki jako parametry. To kluczowa zasada:
*Jeśli nie możesz napisać testu — kod jest zbyt sztywny.*

**Testy znalazły bugi w samych testach** — dwa błędy odkryłem pisząc testy:
1. Helper `wpis_jsonl()` ma domyślne `inp=1000, out=500` — doliczały się
   do testów izolujących cache. Naprawa: jawne `inp=0, out=0`.
2. Piksel (32,32) to środek ikony — tam jest czarna litera, nie kolor kółka.
   Naprawa: próbkowanie boku kółka (piksel 12,32).

**`@pytest.mark.parametrize`** — zamiast 7 prawie identycznych funkcji dla
każdego modelu, jeden test ze zmiennymi danymi:

```python
@pytest.mark.parametrize("model,inp,out,oczekiwany", [
    ("claude-sonnet-4-6",         1_000_000, 0, 3.00),
    ("claude-opus-4-7",           1_000_000, 0, 15.00),
    ("claude-haiku-4-5-20251001", 1_000_000, 0, 0.80),
    # ...i tak dalej
])
def test_koszt_per_model(self, model, inp, out, oczekiwany, plik_jsonl):
    katalog = plik_jsonl([wpis_jsonl(model=model, inp=inp, out=out)])
    stats = czytaj_uzycie(claude_dir=katalog)
    assert abs(stats["koszt_usd"] - oczekiwany) < 0.0001
```

---

---

# POZIOM 2 — Integration testy ✅ ZROBIONE

## Czym różni się od unit testów?

Unit test sprawdza **jedną funkcję w izolacji**.  
Integration test sprawdza **kilka elementów razem** — jak współpracują.

```
Unit test:        czytaj_uzycie() → sprawdź wynik
                  (izolacja — sztuczne dane)

Integration test: zapisz_json(stats) + wczytaj z dzisiaj.json → sprawdź
                  (prawdziwy plik na dysku, prawdziwy przepływ danych)
```

Przykład z naszej aplikacji — pełny cykl:

```python
def test_pelny_cykl_zapis_odczyt(tmp_path):
    # ARRANGE — stwórz prawdziwe pliki JSONL
    claude_dir = tmp_path / "claude"
    (claude_dir / "projects" / "proj").mkdir(parents=True)
    (claude_dir / "projects" / "proj" / "log.jsonl").write_text(
        wpis_jsonl(inp=500_000, out=250_000), encoding="utf-8"
    )
    dzisiaj_json = tmp_path / "dzisiaj.json"

    # ACT — uruchom pełny przepływ jak w prawdziwej aplikacji
    stats = czytaj_uzycie(claude_dir=claude_dir)
    zapisz_json_do(stats, dzisiaj_json)          # zapisz do pliku
    odczytane = json.loads(dzisiaj_json.read_text())  # wczytaj z pliku

    # ASSERT — sprawdź że dane przeżyły zapis i odczyt bez zmian
    assert odczytane["tokeny_wejscia"] == 500_000
    assert odczytane["tokeny_wyjscia"] == 250_000
    assert odczytane["liczba_wywolan"] == 1
```

## Co przetestowaliśmy (18 testów)

```
TestPelnyPrzeplyw (4 testy)
  ✅ dane przeżyją zapis i odczyt (tokeny bez zmian)
  ✅ koszt USD zachowany z precyzją po serializacji
  ✅ wiele wywołań sumuje się poprawnie przez plik
  ✅ pusty wynik serializuje się do JSON bez wyjątku

TestWieleProjektow (4 testy)
  ✅ sumuje tokeny z wielu projektów (różne podkatalogi)
  ✅ sumuje z wielu sesji JSONL w jednym projekcie
  ✅ czytaj_wydatki_od() sumuje koszty z wielu projektów
  ✅ czytaj_wydatki_od() pomija wpisy sprzed daty granicznej

TestConfigZapisOdczyt (4 testy)
  ✅ zapisz_tryb('api') → wczytaj_config() zwraca 'api'
  ✅ zmiana trybu zachowuje pozostałe klucze (budzet, saldo)
  ✅ wielokrotna zmiana trybu nie psuje pliku
  ✅ plik config.json jest poprawnym JSON po każdym zapisie

TestAutoZapiszDateSalda (4 testy)
  ✅ dodaje datę gdy brak i zapisuje do pliku
  ✅ nie nadpisuje istniejącej daty w pliku
  ✅ bez saldo_api_usd nie dotyka pliku (mtime bez zmian)
  ✅ saldo i data dostępne przez wczytaj_config() po zapisie

TestKodowanieZnakow (2 testy)
  ✅ polskie znaki w JSONL są ignorowane (tylko tokeny się liczą)
  ✅ polskie znaki w config.json przeżywają zapis i odczyt
```

## Wynik

```
============================= test session starts =============================
collected 18 items

tests/test_integration.py::TestPelnyPrzeplyw::test_dane_przezyja_zapis_i_odczyt    PASSED
tests/test_integration.py::TestPelnyPrzeplyw::test_koszt_zachowany_z_precyzja      PASSED
tests/test_integration.py::TestPelnyPrzeplyw::test_wiele_wywolan_sumuje_sie_poprawnie PASSED
tests/test_integration.py::TestPelnyPrzeplyw::test_pusty_wynik_serializuje_sie_do_json PASSED
tests/test_integration.py::TestWieleProjektow::test_sumuje_tokeny_z_wielu_projektow PASSED
tests/test_integration.py::TestWieleProjektow::test_sumuje_z_wielu_sesji_w_jednym_projekcie PASSED
tests/test_integration.py::TestWieleProjektow::test_czytaj_wydatki_od_sumuje_wiele_projektow PASSED
tests/test_integration.py::TestWieleProjektow::test_czytaj_wydatki_od_pomija_stare_wpisy PASSED
tests/test_integration.py::TestConfigZapisOdczyt::test_zapisz_i_odczytaj_tryb_api  PASSED
tests/test_integration.py::TestConfigZapisOdczyt::test_zapisz_tryb_zachowuje_pozostale_klucze PASSED
tests/test_integration.py::TestConfigZapisOdczyt::test_wielokrotna_zmiana_trybu    PASSED
tests/test_integration.py::TestConfigZapisOdczyt::test_plik_config_jest_poprawnym_json_po_zapisie PASSED
tests/test_integration.py::TestAutoZapiszDateSalda::test_dodaje_date_gdy_brak_i_zapisuje_do_pliku PASSED
tests/test_integration.py::TestAutoZapiszDateSalda::test_nie_nadpisuje_istniejącej_daty_w_pliku PASSED
tests/test_integration.py::TestAutoZapiszDateSalda::test_bez_salda_nie_dotyka_pliku PASSED
tests/test_integration.py::TestAutoZapiszDateSalda::test_saldo_i_data_dostepne_po_odczycie PASSED
tests/test_integration.py::TestKodowanieZnakow::test_polskie_znaki_w_jsonl_sa_ignorowane PASSED
tests/test_integration.py::TestKodowanieZnakow::test_polskie_znaki_w_config_zachowane PASSED

============================== 18 passed in 0.36s =============================
```

## Czego nauczyłem się na Poziomie 2

**Izolacja przez tmp_path** — każdy test dostaje swój czysty katalog tymczasowy.
Nie ma możliwości żeby jeden test "zabrudzić" dane drugiego.

**Helper `_stworz_claude_dir()`** — zamiast powtarzać tworzenie struktury katalogów
w każdym teście, mamy lokalny helper który przyjmuje słownik `{projekt: [wpisy]}`.

**Testy kodowania** — polskie znaki to klasyczne źródło bugów na Windows (cp1250 vs UTF-8).
Dwa testy specjalnie to weryfikują — raz dla JSONL, raz dla config.json.

**Zmiana trybu nie powinna niszczyć danych** — test `test_zapisz_tryb_zachowuje_pozostale_klucze`
to test regresji: kiedyś przypadkowo napisałem `zapisz_tryb` tak, że nadpisywało cały plik
tylko trybem, kasując pozostałe klucze. Ten test by to wykrył natychmiast.

## Kiedy integration test jest lepszy niż unit?

Kiedy chcesz sprawdzić że **dane nie giną między krokami**.

Unit test sprawdza: "czy `czytaj_uzycie()` zwraca dobry słownik?"  
Integration test sprawdza: "czy ten słownik po zapisaniu do pliku
i wczytaniu z powrotem nadal ma te same wartości?"

Takie błędy (serializacja, kodowanie znaków, zaokrąglenia float) unit testy
nie wykrywają — bo nie dotykają pliku.

---

---

# POZIOM 3 — GUI testy (pywinauto) 📝 ZAAWANSOWANE

## Czym jest GUI test?

GUI test (Graphical User Interface) to test który **steruje prawdziwym okienkiem**
aplikacji — tak jak robi to człowiek. Klika przyciski, wpisuje tekst, czyta etykiety.

W testach webowych robił to Playwright. Dla aplikacji desktopowych Windows
jest **pywinauto** — biblioteka która komunikuje się z Windows Automation API.

## Jak to działa?

```python
from pywinauto import Application

# Uruchom aplikację
app = Application().start(r"python tray_monitor.py")

# Znajdź okienko po tytule
okno = app.window(title="Monitor Tokenów")

# Kliknij przycisk "API"
okno.child_window(title="● API", control_type="Button").click()

# Sprawdź czy panel API jest aktywny
assert okno.child_window(title="Aktualne saldo").exists()
```

## Dlaczego to trudne?

**1. Synchronizacja** — GUI jest asynchroniczne. Po kliknięciu przycisku
wynik może pojawić się za chwilę. Trzeba poczekać:

```python
okno.wait("visible", timeout=5)  # poczekaj max 5 sekund
```

**2. Identyfikacja elementów** — tkinter nie zawsze daje dobre nazwy widgetom.
Czasem trzeba szukać po pozycji, typie, indeksie — co jest kruche.

**3. Środowisko** — GUI testy działają tylko na systemie z ekranem.
Nie działają w CI/CD (Jenkins, GitHub Actions) bez specjalnej konfiguracji.

**4. Szybkość** — jeden GUI test trwa 2-5 sekund. 46 unit testów zajęło 0.56s.

## Kiedy warto?

Tylko dla **krytycznych ścieżek** których nie można przetestować inaczej:
- Czy kliknięcie PRO/API zmienia wygląd okna?
- Czy dialog salda otwiera się i zamyka?
- Czy ikona pojawia się w tray?

## Co byśmy napisali na poziomie 3

```python
# Szkielet testu GUI (pywinauto)

class TestGUIMonitora:

    @pytest.fixture(autouse=True)
    def uruchom_aplikacje(self, tmp_path):
        """Uruchamia aplikację przed każdym testem, zamyka po."""
        self.proc = subprocess.Popen(["python", "tray_monitor.py"])
        time.sleep(2)  # poczekaj na inicjalizację
        self.app = Application(backend="uia").connect(title="Monitor Tokenów")
        yield
        self.proc.terminate()

    def test_przelaczenie_na_api(self):
        okno = self.app.window(title="Monitor Tokenów")
        okno.child_window(title_re=".*API.*", control_type="Button").click()
        # sprawdź że config.json ma tryb="api"
        cfg = json.loads(Path("src/config.json").read_text())
        assert cfg["tryb"] == "api"

    def test_dialog_salda_otwiera_sie(self):
        okno = self.app.window(title="Monitor Tokenów")
        okno.child_window(title_re=".*Zaktualizuj saldo.*").click()
        dialog = self.app.window(title="Aktualizuj saldo")
        assert dialog.exists()
        dialog.close()
```

---

---

## Podsumowanie — trzy poziomy

| | Poziom 1 (Unit) | Poziom 2 (Integration) | Poziom 3 (GUI) |
|---|---|---|---|
| **Co testuje** | Jedną funkcję | Kilka funkcji razem | Całą aplikację przez UI |
| **Szybkość** | 0.56s / 46 testów | kilka sekund | kilkanaście sekund |
| **Niezawodność** | Bardzo wysoka | Wysoka | Niska (kruche) |
| **Trudność** | Niska | Średnia | Wysoka |
| **Narzędzie** | pytest | pytest | pytest + pywinauto |
| **Status** | ✅ Zrobione | 📝 Do zrobienia | 📝 Opcjonalne |

---

## Jak uruchomić testy (dla rekrutera)

```bash
# Wejdź do katalogu aplikacji
cd "D:\MOJE PROJEKTY\Monitor-Tokenow"

# Uruchom wszystkie testy
python -m pytest tests/ -v

# Oczekiwany wynik:
# 46 passed in 0.56s
```

---

*Testy napisane: maj 2026 · Autor: Daniel Bryjak*
