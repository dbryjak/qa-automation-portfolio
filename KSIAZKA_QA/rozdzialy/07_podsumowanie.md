# Rozdział 7 — Podsumowanie
## Czego się nauczyłem i co potrafię

---

### Łączne wyniki testów

| Faza | Strona | Testy | Wynik | Czas |
|---|---|---|---|---|
| 1 | saucedemo.com | 4 | ✅ 4/4 | ~12s |
| 2 | biopoprom.pl | 12 | ✅ 12/12 | ~30s |
| 3 | koparka-kobierzyce.pl | 16 | ✅ 16/16 | ~44s |
| 4 | dbcraftmode.pl | 17 | ✅ 17/17 | ~61s |
| 6 | Wszystkie strony | 34 | ✅ 34/34 | ~54s |
| **RAZEM** | **5 projektów** | **83** | **✅ 83/83** | **~3 min** |

83 testy automatyczne. 0 failed. Na żywych, produkcyjnych stronach.

---

### Tabela kompetencji — co potrafię

#### Narzędzia i technologie

| Narzędzie | Poziom | Gdzie używane |
|---|---|---|
| Python 3 | ⭐⭐⭐ Średni | Wszystkie testy |
| Pytest | ⭐⭐⭐ Średni | Framework testowy, fixtures, parametrize |
| Playwright | ⭐⭐⭐ Średni | Automatyzacja przeglądarki |
| HTML/CSS/JS | ⭐⭐⭐ Średni | Selektory, DOM, JavaScript w testach |
| Git | ⭐⭐ Podstawowy | Wersjonowanie projektu |
| SQL | ⭐⭐ Podstawowy | Rozumienie backendu (MySQL, SQLite) |
| Page Object Model | ⭐⭐⭐ Średni | Architektura wszystkich testów |
| TestRail | ⭐⭐ Podstawowy | Kurs SDA |
| Jira | ⭐⭐ Podstawowy | Kurs SDA |

#### Typy testów które napisałem

| Typ testu | Przykład | Gdzie |
|---|---|---|
| Smoke tests | Strona się ładuje, title poprawny | Fazy 1-4 |
| Testy logowania | Błędne hasło → error, poprawne → dashboard | Fazy 1, 3, 4 |
| Testy formularzy | Pola, walidacja, submit | Fazy 3, 4 |
| Testy nawigacji | Linki, przekierowania, URL | Fazy 2, 3 |
| CRUD testing | Dodaj wpis → pojawia się na liście | Faza 4 |
| Testy sesji | Login → sesja → logout | Fazy 3, 4 |
| Testy SEO | Tytuł, meta, H1, viewport, lang | Faza 6 |
| Testy wydajności | TTFB, DCL, Load timing | Faza 6 |
| Testy dostępności | Alt, labels, ARIA landmarks | Faza 6 |
| Testy linków | Broken links, broken images | Faza 6 |
| Screenshoty | Full-page dokumentacja | Faza 6 |

#### Techniki programistyczne

| Technika | Opis | Gdzie |
|---|---|---|
| Page Object Model | Klasy per strona, selektory jako stałe | Wszystkie fazy |
| Fixtures | `@pytest.fixture` dla setup/teardown | Wszystkie fazy |
| `parametrize` | Jeden test × N stron/danych | Faza 6 |
| `page.evaluate()` | JavaScript w kontekście przeglądarki | Faza 6 |
| `page.on("response")` | Nasłuchiwanie na zasoby sieciowe | Faza 6 |
| Timestamp unique data | `UNIQUE = str(int(time.time()))` | Faza 4 |
| `wait_until="domcontentloaded"` | Stabilne czekanie na ładowanie | Wszystkie |
| `performance.timing` API | Pomiar wydajności przez JS | Faza 6 |

---

### Bugs znalezione podczas testowania

Automatyczne testy nie są tylko "zielonymi checkboxami" — są też **narzędziem znajdowania bugów**. W tym projekcie znalazłem:

| Bug | Strona | Opis | Severity |
|---|---|---|---|
| Brak h1-h6 | biopoprom.pl | Żadne tagi nagłówkowe — WCAG 1.3.1 | Medium |
| project-add.php 404 | dbcraftmode.pl | Plik nie wdrożony na serwer | Low |
| Email admina niezgodny | dbcraftmode.pl | setup_admin.php ≠ produkcja | Info |

---

### Co wyróżnia ten projekt spośród typowych portfolio junior QA

**Typowe portfolio junior QA:**
- Testy na środowisku ćwiczebnym (Selenium-waiter, DemoQA)
- Copy-paste z tutoriala
- Brak kontekstu biznesowego

**To portfolio:**
- Testy na **produkcyjnych stronach klienta i własnych projektach**
- Samodzielna konfiguracja środowiska (Python 3.14, SSL fixes, dependency hell)
- **Rzeczywiście znalezione bugi** (nie wymyślone)
- **Page Object Model** zamiast selektorów bezpośrednio w testach
- Dokumentacja każdej techniki w formie książki
- Rozumienie backendu (PHP, MySQL, CSRF, bcrypt, sesje)

---

### Co jeszcze chcę się nauczyć

Szczerość w rozmowie rekrutacyjnej jest zaletą, nie wadą:

| Obszar | Status |
|---|---|
| API testing (requests/httpx) | Zaplanowane w Fazie 5 |
| CI/CD (GitHub Actions) | Następny krok |
| Docker (środowisko testowe) | Następny krok |
| Testy mobilne (Playwright mobile) | Do nauki |
| TypeScript (dla projektów Node.js) | Do nauki |
| axe-core (pełne testy WCAG) | Do nauki |

---

*Projekt ukończony: 2026-05-21*
*83 testy automatyczne | 5 stron | 6 modułów testowych | 0 failed*
