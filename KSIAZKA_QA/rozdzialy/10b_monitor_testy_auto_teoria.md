# Rozdział 10b — Monitor Tokenów: Automatyzacja testów
## Teoria przed kodem

---

## Dlaczego testowanie GUI desktopowego jest trudniejsze?

Przy testach webowych mieliśmy Playwright — narzędzie które rozumie HTML, CSS, DOM.
Wpisuje tekst, klika buttony, sprawdza zawartość — i robi to niezawodnie.

Aplikacja desktopowa to inny świat. Nie ma DOM-a. Są **piksele, okna Windows, wątki systemowe**.

```
Aplikacja webowa:          Aplikacja desktopowa (tkinter):
─────────────────          ──────────────────────────────
HTML → DOM → locatory      Okno Windows → widgety → brak standardu
Playwright klika po DOM    pyautogui klika po współrzędnych XY
Stabilne i czytelne        Kruche — zmiana rozmiaru = błąd testu
```

---

## Piramida testów dla tej aplikacji

```
          /\
         /  \
        / E2E \         ← najtrudniejsze: kliknij ikonę tray, sprawdź okno
       /────────\
      /Integration\     ← średnie: czytaj prawdziwe pliki JSONL
     /────────────\
    /  Unit Tests  \    ← najłatwiejsze: przetestuj logikę bez GUI
   ────────────────────
```

**W aplikacjach desktopowych** przewraca się piramidę do góry nogami:
- Dużo unit testów → szybkie, niezawodne, łatwe
- Mało lub zero E2E → wolne, kruche, drogie w utrzymaniu

---

## Co możemy automatycznie przetestować?

### ✅ Poziom 1 — Unit testy (pytest) — ŁATWE i opłacalne

To **czysta logika biznesowa** — bez GUI, bez okienek, bez systemu tray.

| Funkcja | Co testujemy |
|---------|-------------|
| `czytaj_uzycie()` | Czy poprawnie sumuje tokeny z JSONL? |
| `czytaj_wydatki_od(data)` | Czy filtruje po dacie? Czy ignoruje stare wpisy? |
| `wczytaj_config()` | Czy radzi sobie z brakującym plikiem? |
| `stworz_ikone(tryb)` | Czy zwraca obiekt Image odpowiedniego rozmiaru? |
| Obliczenia kosztów | Czy ceny modeli są wyliczane poprawnie? |

Żadna z tych funkcji nie wymaga tkinter. Można je testować w 100% automatycznie.

---

### ⚠️ Poziom 2 — Integration testy — ŚREDNIO trudne

Testujemy współpracę między komponentami — np. czy aplikacja poprawnie czyta
prawdziwe pliki JSONL i zapisuje do `dzisiaj.json`.

Wymaga: tymczasowych katalogów z plikami (`tmp_path` fixture w pytest).

---

### ❌ Poziom 3 — GUI/E2E — TRUDNE i ryzykowne

Opcje do automatyzacji okienek tkinter:

| Narzędzie | Jak działa | Wady |
|-----------|-----------|------|
| **pyautogui** | Klika po współrzędnych XY ekranu | Kruche — zależy od rozdzielczości |
| **pywinauto** | Kontroluje okna Windows przez WinAPI | Lepsze, ale złożone w setup |
| **Windows UI Automation** | Natywny interfejs Microsoft | Najbardziej stabilne, najtrudniejsze |

**Wniosek:** Dla projektu tej skali GUI E2E to **over-engineering**. Lepiej mieć solidne unit testy niż kruche testy klikające po pikselach.

---

## Strategia: co faktycznie napiszemy

```
Poziom 1 — Unit testy (pytest)          ← TO NAPISZEMY
  ✓ czytaj_uzycie() z mockiem JSONL
  ✓ czytaj_wydatki_od() — filtrowanie dat
  ✓ obliczenia kosztów per model
  ✓ wczytaj_config() — edge cases
  ✓ stworz_ikone() — typ i rozmiar

Poziom 2 — Integration testy (pytest)   ← TO NAPISZEMY
  ✓ zapis i odczyt dzisiaj.json
  ✓ config.json — zapis trybu i salda

Poziom 3 — GUI testy (pywinauto)        ← OPCJONALNIE (osobny rozdział)
  ? otwieranie okna
  ? klikanie przycisków PRO/API
```

---

## Struktura plików testów

```
Monitor-Tokenow/
├── tray_monitor.py
├── demon.py
├── src/config.json
├── data/
└── tests/                    ← nowy katalog
    ├── __init__.py
    ├── conftest.py           ← fixtures (tmp config, tmp JSONL)
    ├── test_czytaj_uzycie.py ← testy odczytu tokenów
    ├── test_koszty.py        ← testy obliczeń cennika
    ├── test_config.py        ← testy konfiguracji
    └── test_ikona.py         ← testy generowania ikony
```

---

## Wyzwania techniczne — na co uważać

### Problem 1 — Globalne ścieżki w kodzie
```python
# W tray_monitor.py są zahardkodowane ścieżki:
CONFIG_JSON  = Path(r"D:\MOJE PROJEKTY\Monitor-Tokenow\src\config.json")
CLAUDE_DIR   = Path.home() / ".claude"
```
Testy muszą **podmienić** te ścieżki na tymczasowe — inaczej test modyfikuje prawdziwy config.

**Rozwiązanie:** `monkeypatch` w pytest albo przekazywanie ścieżek jako parametry do funkcji.

---

### Problem 2 — Funkcje czytają pliki bezpośrednio
```python
def czytaj_uzycie():
    for jsonl in CLAUDE_DIR.rglob("*.jsonl"):  # zawsze ten sam katalog!
        ...
```
Test nie może kontrolować zawartości `~/.claude/`.

**Rozwiązanie:** Refactor — przekazać `claude_dir` jako parametr z domyślną wartością.

---

### Problem 3 — Brak separacji logiki od GUI
Obecnie `czytaj_uzycie()` jest funkcją modułu — to OK.  
`_odswiez()` łączy logikę z aktualizacją widgetów — trudno testować.

**Rozwiązanie:** Zostawiamy jak jest — testujemy tylko "czyste" funkcje, pomijamy metody GUI.

---

## Kluczowe przypadki testowe (unit)

### Testy obliczania kosztów

```
GIVEN: 1 000 000 tokenów wejścia (claude-sonnet-4-6)
WHEN:  oblicz koszt
THEN:  $3.00 USD (cena $3.00/M)

GIVEN: 500 000 tokenów wyjścia (claude-sonnet-4-6)  
WHEN:  oblicz koszt
THEN:  $7.50 USD (cena $15.00/M)

GIVEN: nieznany model
WHEN:  oblicz koszt
THEN:  użyj domyślnego (claude-sonnet-4-6), nie rzucaj wyjątku
```

### Testy filtrowania JSONL

```
GIVEN: plik JSONL z 3 wpisami — 2 z dzisiaj, 1 sprzed tygodnia
WHEN:  czytaj_uzycie()
THEN:  zwróć tylko 2 wpisy (liczba_wywolan = 2)

GIVEN: plik JSONL z wpisem gdzie usage = {} (puste)
WHEN:  czytaj_uzycie()
THEN:  pomiń wpis (liczba_wywolan = 0)

GIVEN: pusty katalog ~/.claude/
WHEN:  czytaj_uzycie()
THEN:  zwróć zerowe statystyki, nie rzucaj wyjątku
```

### Testy konfiguracji

```
GIVEN: config.json nie istnieje
WHEN:  wczytaj_config()
THEN:  zwróć pusty słownik {}

GIVEN: config.json z "tryb": "pro"
WHEN:  zapisz_tryb("api")
THEN:  config.json zawiera "tryb": "api"
```

---

## Czego nauczy nas pisanie tych testów?

1. **Jak testować kod który czyta pliki** — `tmp_path`, `monkeypatch`
2. **Jak izolować testy** — każdy test zaczyna od czystego stanu
3. **Jak pisać testy parametryczne** — jeden test, wiele przypadków (`@pytest.mark.parametrize`)
4. **Jak testować edge cases** — puste pliki, błędne dane, brakujące klucze

---

*Następny krok: [Rozdział 10c — Implementacja testów automatycznych](10c_monitor_testy_auto_kod.md)*
