# Rozdział 2 — Testowanie aplikacji BIOPOPROM

## Czym jest testowana aplikacja?

**BIOPOPROM** to autorska aplikacja webowa — zegar oparty na alternatywnym, 20-godzinnym systemie czasu naturalnego. Aplikacja jest w pełni zbudowana w HTML/CSS/JavaScript (tzw. SPA — Single Page Application) bez zewnętrznych frameworków.

**Cztery moduły aplikacji:**
- **Zegar** — wyświetla bieżący czas w formacie BP (20 godzin na dobę) oraz czas standardowy
- **Kalendarz** — 13-miesięczny kalendarz księżycowy (28 dni × 13 miesięcy = 364 dni)
- **Sieć** — kalkulator przeliczający czas STD↔BP, generator kart członka
- **Harmonia** — generator dźwięku 432 Hz, kalkulator złotego podziału φ, geometria 364°

## Co testujemy i dlaczego?

| Kategoria | Co sprawdzamy |
|---|---|
| **Smoke** | Czy strona się otwiera i pokazuje poprawny tytuł |
| **Nawigacja** | Czy zakładki przełączają widoki |
| **Zegar** | Czy czas jest zainicjowany i ma prawidłowy format |
| **Kalendarz** | Czy renderuje się siatka i działa nawigacja miesięcy |
| **Kalkulatory** | Czy zwracają wyniki dla poprawnych danych |
| **Interakcja** | Czy przyciski presetów zmieniają stan |

## Metodologia testowania

Testy napisane w **Playwright + Pytest** z wzorcem **Page Object Model**:

```
tests/biopoprom/
    test_biopoprom.py   ← 12 przypadków testowych

pages/
    biopoprom_page.py   ← Page Object — lokatory i akcje
```

## Przypadki testowe

| ID | Klasa | Opis | Wynik |
|---|---|---|---|
| TC-01 | TestSmoke | Strona ładuje się z tytułem "BIOPOPROM" | PASS |
| TC-02 | TestSmoke | Zegar i czas BP widoczne na starcie | PASS |
| TC-03 | TestSmoke | Nawigacja zawiera 4 zakładki | PASS |
| TC-04 | TestNavigation | Przełączanie między zakładkami | PASS |
| TC-05 | TestZegar | Czas BP i standardowy w formacie HH:MM:SS | PASS |
| TC-06 | TestZegar | Faza księżyca jest wyświetlona | PASS |
| TC-07 | TestKalendarz | Siatka kalendarza renderuje min. 28 komórek | PASS |
| TC-08 | TestKalendarz | Nawigacja poprzedni/następny miesiąc | PASS |
| TC-09 | TestSiec | Kalkulator STD→BP zwraca wynik HH:MM:SS | PASS |
| TC-10 | TestSiec | Kalkulator BP→STD zwraca wynik HH:MM:SS | PASS |
| TC-11 | TestHarmonia | Kalkulator złotego podziału zwraca wyniki | PASS |
| TC-12 | TestHarmonia | Przycisk 528 Hz aktywuje się i zmienia Hz | PASS |

**Wynik końcowy: 12/12 PASSED** ✓

## Napotkane wyzwania

### Problem 1: Emoji w etykietach zakładek
Zakładki zawierają ikony emoji (`🕐\nZEGAR`). Pierwotna asercja `== "ZEGAR"` nie działała.

**Rozwiązanie:** Zamiast porównywania dokładnego, sprawdzamy zawartość:
```python
# Błędnie:
assert "ZEGAR" in [l.strip().upper() for l in labels]

# Poprawnie:
assert "ZEGAR" in " ".join(labels).upper()
```

**Lekcja QA:** Zawartość UI może zawierać niewidoczne znaki, spacje, emoji — asercje powinny być odporne na to.

### Problem 2: Asynchroniczne ładowanie danych
Zegar inicjalizuje się przez `requestAnimationFrame`. Bez `wait_for_timeout(1200)` czas mógłby być `--:--:--`.

**Rozwiązanie:** Dodanie krótkiego oczekiwania przed asercją na czas.

**Lekcja QA:** Testy UI wymagają uwzględnienia asynchroniczności — nie każdy element jest gotowy od razu po załadowaniu strony.

## Kod — przykład testu (TC-08)

```python
def test_TC08_month_navigation(self, open_app):
    app = open_app
    app.switch_tab("kalendarz")
    app.page.wait_for_timeout(500)
    
    before = app.get_month_name()
    app.click_next_month()
    after = app.get_month_name()
    
    assert before != after, f"Miesiąc powinien się zmienić: {before} -> {after}"
    
    app.click_prev_month()
    restored = app.get_month_name()
    assert restored == before, f"Po cofnięciu miesiąc powinien być: {before}"
```

## Uruchomienie testów

```bash
cd "d:\Projekt SDA\automation"
venv\Scripts\activate
pytest tests/biopoprom/test_biopoprom.py -v
```

Raport HTML: `reports/report.html`

---
*Rozdział napisany: 2026-05-20 | 12 testów | Wynik: 12/12 PASSED*
