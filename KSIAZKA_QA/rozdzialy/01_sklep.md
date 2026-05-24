# Rozdział 1 — Pierwsze testy automatyczne

## `www.saucedemo.com`

---

### O projekcie

Pierwsza faza to nauka podstaw — zanim zacznę testować własne projekty, potrzebuję środowiska, gdzie mogę bezpiecznie popełniać błędy. `saucedemo.com` to publicznie dostępna aplikacja demo stworzona przez firmę Sauce Labs specjalnie do nauki i prezentacji testów automatycznych.

Dlaczego nie testowałem od razu swojej strony? Bo przy pierwszych testach popełnia się dużo błędów — zły selektor, niedziałający locator, zbyt mało czasu oczekiwania. Lepiej uczyć się na aplikacji, którą ktoś specjalnie przygotował do tego celu, niż ryzykować zaśmiecenie własnej bazy danych.

**Dostępne konta testowe na saucedemo.com:**

| Login                     | Hasło          | Co testuje               |
| ------------------------- | -------------- | ------------------------ |
| `standard_user`           | `secret_sauce` | Normalne logowanie       |
| `locked_out_user`         | `secret_sauce` | Zablokowane konto        |
| `problem_user`            | `secret_sauce` | Błędy UI (broken images) |
| `performance_glitch_user` | `secret_sauce` | Wolne ładowanie          |

To gotowa "piaskownica" — idealna na start.

---

### Dlaczego nie yabko-com.e-kei.pl?

Oryginalnie planowałem testować `yabko-com.e-kei.pl` — sklep internetowy udostępniony przez kolegę z tzw. podwórka. Pierwsze uruchomienie zwróciło błąd:

```
TargetClosedError: Page closed while waiting for locator
```

Strona była offline — kolega ją zdjął. To pierwsza ważna lekcja:

> **Lekcja:** Środowisko testowe musi być stabilne i dostępne. Jeśli testujesz cudzą infrastrukturę bez gwarancji uptime'u, twoje testy będą zawodne z przyczyn poza twoją kontrolą. `saucedemo.com` to gwarantowane środowisko — Sauce Labs utrzymuje je specjalnie dla testerów.

---

### Konfiguracja środowiska

Zanim napisałem pierwszy test, musiałem skonfigurować całe środowisko od zera.

**Problemy które napotkałem:**

**Problem 1 — greenlet i Python 3.14:**

```
error: legacy-install-failure × Encountered error while trying to install package › greenlet
```

Playwright 1.49.1 wymagał `greenlet==3.1.1` — bez kółka (wheel) dla Pythona 3.14. Rozwiązanie: zmiana z pinowanych wersji na niepinowane:

```ini
# requirements.txt — PRZED (pinowane, nie działało na Python 3.14):
playwright==1.49.1
greenlet==3.1.1

# requirements.txt — PO (niepinowane, działa):
playwright>=1.51
pytest>=8.3
pytest-playwright>=0.7
pytest-html>=4.1
```

**Problem 2 — SSL podczas pobierania przeglądarek:**

```
UNABLE_TO_VERIFY_LEAF_SIGNATURE
```

Rozwiązanie: zmienna środowiskowa `NODE_OPTIONS`:

```powershell
$env:NODE_OPTIONS="--use-system-ca"
venv/Scripts/playwright install chromium
```

**Problem 3 — TargetClosedError:**
Strona yabko offline → zmiana na saucedemo.com + dodanie `wait_until="domcontentloaded"` w `base_page.py`.

---

### Architektura — Page Object Model

POM to wzorzec projektowy: każda strona ma swoją klasę. Testy nie wiedzą jak strona jest zbudowana — tylko co można na niej zrobić.

```python
# pages/base_page.py — klasa bazowa dla wszystkich stron
class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self):
        return self.page.title()
```

```python
# pages/login_page.py — Page Object dla strony logowania
class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = "[data-test='error']"

    def login(self, username, password):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    def is_error_visible(self):
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
```

**Dlaczego POM?** Jeśli saucedemo zmieni ID przycisku z `#login-button` na `#btn-login`, zmieniam to w jednym miejscu (`login_page.py`), a nie w każdym teście osobno.

---

### Co testowałem i dlaczego

#### TC-01: Błędne hasło → komunikat błędu

```python
def test_TC01_wrong_password(self, login_page):
    """TC-01: Błędne hasło → komunikat błędu widoczny."""
    login_page.login("standard_user", "bledne_haslo")
    assert login_page.is_error_visible()
    assert "Password" in login_page.get_error_message() or \
           "password" in login_page.get_error_message()
```

Najbardziej podstawowy test bezpieczeństwa. Aplikacja MUSI pokazywać błąd przy złym haśle — i nie może mówić czy email istnieje (enumeration attack prevention).

---

#### TC-02: Poprawne logowanie → strona produktów → wylogowanie

```python
def test_TC02_valid_login_and_logout(self, login_page, page):
    """TC-02: Poprawne dane → Products page → logout."""
    login_page.login("standard_user", "secret_sauce")
    home = HomePage(page)
    assert home.is_logged_in(), "Brak strony produktów po zalogowaniu"
    assert home.get_page_title() == "Products"
    home.logout()
    assert "/inventory" not in page.url
```

Pełny flow: login → weryfikacja → logout. To "happy path" — najważniejszy scenariusz, który MUSI działać.

**Nowa technika:** Jeden test sprawdza cały przepływ (nie tylko pojedynczą akcję). Koniec testu przywraca stan aplikacji — wylogowanie czyści sesję.

---

#### TC-03: Zablokowane konto → specyficzny komunikat

```python
def test_TC03_locked_out_user(self, login_page):
    """TC-03: Konto zablokowane → komunikat o blokadzie."""
    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "locked out" in error.lower()
```

saucedemo.com ma specjalne konto testowe `locked_out_user`. To technika powszechna w QA: środowisko testowe zawiera predefiniowane "persona" dla różnych scenariuszy. Test weryfikuje nie tylko że błąd się pojawia, ale że zawiera właściwy tekst.

---

#### TC-04: Puste pola → walidacja

```python
def test_TC04_empty_fields(self, login_page):
    """TC-04: Puste pola → komunikat 'Username is required'."""
    login_page.login("", "")
    error = login_page.get_error_message()
    assert "Username is required" in error
```

Walidacja formularza jest pierwszą linią obrony. Puste pole nie powinno przejść do serwera — formularz powinien to wychwycić i pokazać użytkownikowi zrozumiały komunikat.

---

### Raport HTML

```
4 passed in 12.34s
```

| Test                               | Wynik     |
| ---------------------------------- | --------- |
| TC-01: Błędne hasło                | ✅ PASSED |
| TC-02: Poprawne logowanie + logout | ✅ PASSED |
| TC-03: Konto zablokowane           | ✅ PASSED |
| TC-04: Puste pola                  | ✅ PASSED |

Raport HTML generuje się automatycznie po każdym uruchomieniu do folderu `automation/reports/report.html`. Zawiera screenshoty nieudanych testów, czas wykonania i metadane projektu.

---

### Nowe umiejętności zdobyte w tej fazie

| Umiejętność                                             | Gdzie użyta                            |
| ------------------------------------------------------- | -------------------------------------- |
| Konfiguracja środowiska (venv, pip, playwright install) | Setup projektu                         |
| Page Object Model                                       | `login_page.py`, `home_page.py`        |
| Selektory CSS i data-test atrybuty                      | `#login-button`, `[data-test='error']` |
| Asercje w pytest                                        | Każdy test                             |
| `wait_until="domcontentloaded"`                         | Stabilność testów                      |
| pytest-html raporty                                     | `reports/report.html`                  |
| Rozwiązywanie problemów z zależnościami                 | greenlet + Python 3.14                 |

---

### Pliki z testami

`automation/tests/store/test_login.py` — 4 przypadki testowe.

`automation/pages/login_page.py` — Page Object logowania saucedemo.

`automation/pages/home_page.py` — Page Object strony głównej po zalogowaniu.

---

_Faza 1 ukończona | Wynik: 4/4 PASSED_
