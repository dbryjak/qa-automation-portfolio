# Rozdział 3 — Testowanie strony firmowej klienta
## `www.koparka-kobierzyce.pl`

---

### O projekcie

Strona `koparka-kobierzyce.pl` to komercyjny projekt wykonany dla klienta — firmy świadczącej usługi koparką w Gminie Kobierzyce na Dolnym Śląsku. To nie jest środowisko ćwiczebne. To prawdziwa, działająca strona wizytówkowa z własnym systemem CRM, blogiem i narzędziami dla użytkowników.

**Stack technologiczny strony:**
- Frontend: czysty HTML/CSS/JS (brak frameworków)
- Backend: PHP 8 (formularz kontaktowy, CRM)
- Baza danych: SQLite (crm.db)
- Hosting: serwer współdzielony z .htaccess
- GA4: integracja z Google Analytics

**Mapa podstron przetestowanych:**

| Podstrona | URL | Co testowałem |
|---|---|---|
| Strona główna | `/` | Smoke, nawigacja, sekcje, formularz |
| Blog | `/blog/` | Ładowanie, artykuły, nawigacja do artykułu |
| Panel CRM | `/crm/login.php` | Logowanie, błędne hasło, sesja, logout |

---

### Dlaczego to ważne dla portfolio?

Testowanie strony klienta ma zupełnie inny ciężar niż testowanie środowiska ćwiczebnego. Każdy znaleziony błąd ma realną wartość biznesową — może oznaczać straconego klienta lub błędne zapytanie w CRM. To pokazuje, że potrafię pracować na produkcyjnym kodzie.

---

### Co testowałem i dlaczego

#### Moduł 1: Smoke Tests (TC-01 do TC-03)

Pierwsze testy jakie zawsze piszę dla nowej strony. Odpowiadają na pytanie: **"Czy strona w ogóle działa?"**

```python
def test_TC01_title(self, home):
    title = home.page.title()
    assert "KOPARKI Kobierzyce" in title
```

Sprawdzam:
- Tytuł strony — czy zawiera nazwę firmy (kluczowe dla SEO i identyfikacji)
- Logo — czy element `.logo-circle` z tekstem "KK" jest widoczny
- Hero section — czy główny nagłówek jest widoczny i niepusty

**Dlaczego to ważne:** Jeśli te testy padną, coś się stało z deploymentem lub konfiguracją serwera. To pierwsze "czujniki alarmowe".

---

#### Moduł 2: Nawigacja (TC-04 do TC-05)

```python
def test_TC05_blog_link_navigates(self, home):
    home.page.locator(".topbar-nav a", has_text="Blog").click()
    assert "/blog" in home.page.url
```

Sprawdzam:
- Czy menu zawiera linki do Bloga i Kalkulatora
- Czy klik w "Blog" faktycznie przenosi na `/blog/` (nie ma literówki w href)

**Nowa technika:** `locator(selector, has_text="...")` — szukam elementu po selektorze CSS ORAZ zawartości tekstu jednocześnie. To precyzyjniejsze niż sam CSS i bardziej odporne na zmiany layoutu.

---

#### Moduł 3: Sekcje strony (TC-06 do TC-07)

Strona główna to long-scroll — wszystkie treści są na jednej stronie w sekcjach `#oferta`, `#wykopy`, `#realizacje`, itd. Sprawdzam, że każda sekcja istnieje w DOM:

```python
for section_id in ["oferta", "wykopy", "przylacza", "realizacje", "kontakt"]:
    count = home.page.locator(f"#{section_id}").count()
    assert count > 0
```

**Nowa technika:** Pętla testowa — jeden test sprawdza wiele elementów naraz. Efektywne gdy mamy powtarzalne elementy (sekcje, karty, linki).

---

#### Moduł 4: Formularz kontaktowy (TC-08 do TC-10)

Formularz to kluczowy element strony — przez niego przychodzą zapytania od klientów. Sprawdzam:

1. Czy pola `Imię`, `Telefon`, `Wybór usługi` istnieją
2. Czy przycisk ma właściwy tekst (`wycen` lub `wyślij`)
3. Czy lista rozwijana zawiera wszystkie usługi (fundamenty, szambo, niwelacja)

```python
options = home.page.locator(f"{home.SELECT_SERVICE} option").all_inner_texts()
assert "fundament" in " ".join(options).lower()
```

**Dlaczego nie testuję wysyłania?** Formularz wysyła email do klienta. Automatyczne testy nie powinny generować prawdziwych wiadomości na produkcji — to naruszyłoby zaufanie klienta. W realnym projekcie testujemy wysyłanie na środowisku testowym (staging) z fałszywym adresem e-mail.

---

#### Moduł 5: Blog (TC-11 do TC-13)

```python
def test_TC12_blog_has_articles(self, blog):
    count = blog.get_article_count()
    assert count >= 1
```

Sprawdzam:
- Czy strona bloga ładuje się z poprawnym tytułem
- Czy jest co najmniej 1 artykuł (`.blog-card`)
- Czy klik w link artykułu zmienia URL i ładuje treść

**Nowa technika:** `fixture` dla każdego modułu — `@pytest.fixture() def blog(page)`. Każdy moduł testowy ma własny fixture który otwiera właściwą stronę. Testy są od siebie niezależne.

---

#### Moduł 6: Panel CRM (TC-14 do TC-16)

To najbardziej zaawansowany moduł tej fazy. CRM to panel administracyjny dla klienta — przechowuje zapytania od potencjalnych klientów.

**TC-14 — Strona logowania istnieje:**
```python
assert "/crm/login" in crm.page.url
assert crm.page.locator(crm.PWD_INPUT).is_visible()
```

**TC-15 — Błędne hasło → komunikat błędu:**
```python
crm.login("bledne_haslo_123")
assert crm.is_error_visible()
assert "/crm/login" in crm.page.url  # brak przekierowania
```

**TC-16 — Poprawne hasło → sesja + wylogowanie:**
```python
crm.login(CRM_PASSWORD)
assert crm.is_logged_in()   # URL zmienił się na /crm/
crm.logout()
assert "/crm/login" in crm.page.url
```

**Ważna uwaga bezpieczeństwa:** Hasło do CRM przechowuję w pliku konfiguracyjnym `pages/koparka_page.py`, a nie bezpośrednio w teście. W projekcie produkcyjnym użyłbym zmiennych środowiskowych `.env` — nigdy nie wrzucamy haseł do repozytorium Git.

---

### Wyniki testów

```
16 passed in 44.12s
```

| Moduł | Testy | Wynik |
|---|---|---|
| Smoke | TC-01..03 | ✅ PASSED |
| Nawigacja | TC-04..05 | ✅ PASSED |
| Sekcje | TC-06..07 | ✅ PASSED |
| Formularz | TC-08..10 | ✅ PASSED |
| Blog | TC-11..13 | ✅ PASSED |
| CRM | TC-14..16 | ✅ PASSED |

---

### Nowe umiejętności zdobyte w tej fazie

| Umiejętność | Gdzie użyta |
|---|---|
| `locator(has_text=...)` | TC-05 nawigacja bloga |
| Pętla testowa po wielu elementach | TC-06 sekcje strony |
| `select_option()` — listy rozwijane | Formularz kontaktowy |
| Testowanie sesji i przekierowań | TC-16 CRM login/logout |
| Fixtures per moduł | Izolacja testów blog/CRM |
| Bezpieczeństwo haseł w testach | CRM — hasło w config, nie w teście |

---

### Plik z testami

`automation/tests/koparka/test_koparka.py` — 16 przypadków testowych, 6 klas, 1 plik.

`automation/pages/koparka_page.py` — 3 klasy Page Object: `KoparkaHomePage`, `KoparkaBlogPage`, `KoparkaCrmPage`.

---

*Faza 3 ukończona: 2026-05-20 | Wynik: 16/16 PASSED*
