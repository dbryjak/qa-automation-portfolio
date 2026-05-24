# KPK — Kompletny Przewodnik Kariery
## Daniel Bryjak | Junior QA Automation Engineer
### Co, gdzie i jak działać żeby dostać pierwszą pracę w QA

---

## CZĘŚĆ 1 — Twoje Portfolio w pigułce

Zanim pójdziesz na rozmowę, musisz umieć powiedzieć to jednym zdaniem:

> *"Zbudowałem 83 automatyczne testy w Pythonie + Playwright dla 5 własnych projektów webowych — sklepu demo, strony firmowej, CRM, panelu admina PHP i cross-site testów SEO/dostępności. Wszystkie przechodzą na żywo."*

To jest Twój elevator pitch. Krótko, konkretnie, z liczbami.

---

## CZĘŚĆ 2 — GitHub — zrób to TERAZ

GitHub to Twoje CV numer 2. Rekruter zajrzy tam zanim zadzwoni.

### Kroki do zrobienia:

**1. Utwórz publiczne repozytorium**
```
Nazwa: qa-automation-portfolio
Opis:  83 automated tests in Python + Playwright for 5 live web projects
```

**2. Wgraj projekt**
```bash
git init
git add automation/ KSIAZKA_QA/
git commit -m "Initial portfolio: 83 Playwright tests across 5 projects"
git remote add origin https://github.com/danielbryjak/qa-automation-portfolio.git
git push -u origin main
```

**3. Napisz README.md** (najważniejszy plik w repo)

```markdown
# QA Automation Portfolio — Daniel Bryjak

83 automated tests | Python + Pytest + Playwright | 5 live projects

## Projects Tested
| Site | Tests | Status |
|------|-------|--------|
| saucedemo.com (e-commerce demo) | 4 | ✅ PASSED |
| biopoprom.pl (SPA) | 12 | ✅ PASSED |
| koparka-kobierzyce.pl (client site) | 16 | ✅ PASSED |
| dbcraftmode.pl (PHP CMS admin) | 17 | ✅ PASSED |
| Cross-site (SEO/A11y/Performance) | 34 | ✅ PASSED |

## Quick Start
pip install -r automation/requirements.txt
playwright install chromium
pytest automation/

## Skills Demonstrated
- Page Object Model
- CRUD testing
- API (session) testing
- Accessibility (WCAG)
- Performance timing
- Cross-browser parametrize
```

**4. Dodaj screenshoty do README** — rekruter widzi je bez klonowania repo.

**5. Zielone kwadraty** — commituj regularnie, nawet małe zmiany. GitHub pokazuje aktywność.

---

## CZĘŚĆ 3 — LinkedIn — profil który przyciąga

### Nagłówek (headline) — NIE pisz "szukam pracy":
```
❌ Student | Szukam pracy w IT
✅ QA Automation Engineer | Python · Playwright · Pytest | SDA Certified
```

### Sekcja "O mnie" (About):
```
Tester oprogramowania z certyfikatem SDA, który zamiast ćwiczyć
na tutorialach — przetestował własne projekty produkcyjne.

83 automatyczne testy w Pythonie + Playwright na 5 żywych stronach:
panel admina PHP, CRM klienta, e-commerce, testy SEO i dostępności.

Szukam roli Junior QA / QA Automation Engineer gdzie będę mógł
rosnąć w kierunku testowania backendu i API.

🔗 GitHub: github.com/danielbryjak/qa-automation-portfolio
```

### Dodaj do sekcji "Projekty":
- **QA Automation Portfolio** — 83 testy, 5 stron, Python + Playwright
- **TESTron** — platforma SaaS do monitoringu stron (w budowie)
- **koparka-kobierzyce.pl** — strona klienta z CRM (web dev + QA)
- **dbcraftmode.pl** — własny CMS z panelem admina (web dev + QA)

### Umiejętności (Skills) — dodaj i poproś o potwierdzenia:
```
Python | Pytest | Playwright | Selenium | Manual Testing | WCAG |
Page Object Model | SQL | PHP | Git | TestRail | Jira | HTML/CSS
```

### Certyfikaty:
- Dodaj certyfikat SDA "Tester Oprogramowania" ze zdjęciem/PDF

---

## CZĘŚĆ 4 — CV — jedna strona, konkretnie

### Wzór sekcji "Projekty":

```
QA Automation Portfolio                                    2026
github.com/danielbryjak/qa-automation-portfolio

• 83 automated tests in Python + Pytest + Playwright across 5 projects
• Tested real production sites: PHP CMS admin panel, client CRM, e-commerce
• Implemented Page Object Model, CRUD testing, session testing
• Cross-site tests: SEO meta tags, WCAG accessibility, performance timing
• Found and documented real accessibility bug (WCAG 1.3.1 violation)
```

### Wzór sekcji "Umiejętności":
```
Testing:     Manual testing, Test case design, Bug reporting, WCAG 2.2
Automation:  Python, Pytest, Playwright, Page Object Model
Tools:       Git, TestRail, Jira, pytest-html
Web:         HTML, CSS, JavaScript, PHP (rozumienie backendu)
Databases:   SQL, MySQL, SQLite (podstawy)
```

### Ważne zasady CV:
- **Jedna strona** — rekruter poświęca 6-10 sekund
- **Liczby wszędzie** — "83 testy" brzmi lepiej niż "wiele testów"
- **Angielski lub Polski** — zdecyduj jedno, nie mieszaj
- **Wyślij jako PDF** — Word zmienia formatowanie

---

## CZĘŚĆ 5 — Gdzie aplikować

### Tytuły stanowisk których szukasz:
```
Junior QA Engineer
Junior QA Automation Engineer
Junior Software Tester
QA Tester (Python)
Test Automation Engineer (Junior)
SDET Junior (Software Development Engineer in Test)
```

### Portale pracy:
| Portal | Uwagi |
|---|---|
| **JustJoin.IT** | Największy IT job board w Polsce, filtry tech stack |
| **NoFluffJobs** | Przejrzyste oferty z widełkami wynagrodzeń |
| **Pracuj.pl** | Szerszy rynek, też korporacje |
| **LinkedIn Jobs** | Dobre do bezpośredniego kontaktu z rekruterami |
| **Indeed.pl** | Agregator, dużo ofert |
| **Bulldogjob** | Specjalizacja IT |

### Typy firm gdzie warto aplikować:
- **Software houses** — robią testy dla klientów, uczą się na projektach
- **Firmy produktowe** — wolniejsze, ale głębsze projekty
- **Korporacje z działem IT** — stabilność, procesy, mentoring
- **Startupy** — szybkie tempo, wiele ról naraz (ryzyko i szansa)

---

## CZĘŚĆ 6 — Rozmowa rekrutacyjna — co Cię zapytają

### Pytania techniczne i jak na nie odpowiadać:

**"Co to jest Page Object Model?"**
> "To wzorzec projektowy gdzie każda strona aplikacji ma swoją klasę w kodzie. Selektory CSS trzymam jako stałe w klasie, nie w teście. Jeśli strona zmieni ID przycisku — zmieniam w jednym miejscu, nie w każdym teście. W moim portfolio mam 6 takich klas: LoginPage, DBCraftBlogPage, itd."

**"Czym różni się Playwright od Selenium?"**
> "Playwright jest nowszy — ma wbudowane auto-wait (nie trzeba pisać sleep()), obsługuje wiele przeglądarek jednym API, i jest szybszy. Selenium jest bardziej dojrzałe i powszechne w starszych projektach. Zaczynałem od Selenium na kursie, ale do portfolio wybrałem Playwright bo to obecny standard."

**"Jak testujesz formularz kontaktowy na produkcji?"**
> "Nie testuję wysyłania — formularz na koparka-kobierzyce.pl wysyłałby prawdziwy email do klienta. Testuję istnienie pól, tekst przycisku i opcje w liście rozwijalnej. Wysyłanie testowałbym na środowisku staging z fałszywym adresem. To ważna zasada: automatyczne testy nie powinny generować side-effects na produkcji."

**"Opisz buga którego znalazłeś."**
> "Podczas testów przekrojowych Faza 6 odkryłem, że strona biopoprom.html nie ma żadnych tagów nagłówkowych h1-h6. To naruszenie WCAG 1.3.1 — czytniki ekranu nie mogą zrozumieć struktury treści. Napisałem raport z priorytetem Medium, opisem kroków reprodukcji i wpływem na SEO i dostępność."

**"Czym jest WCAG?"**
> "Web Content Accessibility Guidelines — standard dostępności stron dla osób z niepełnosprawnościami. W Fazie 6 testowałem kilka wymagań WCAG: alt teksty na obrazach (1.1.1), etykiety formularzy (1.3.1), elementy landmark jak nav i main. W Polsce firmy muszą spełniać WCAG dla serwisów publicznych — to rosnący obszar w QA."

**"Co byś zrobił gdyby test nagle zaczął failować na CI?"**
> "Najpierw sprawdziłbym czy to flaky test (losowo się sypie) czy prawdziwy bug. Uruchomiłbym lokalnie z --headed żeby zobaczyć co się dzieje. Sprawdziłbym logi i screenshot z raportu HTML. Jeśli bug — zgłosiłbym z krokami reprodukcji. Jeśli flaky test — zbadałbym czy to problem z timing (za szybki wait) i dodał odpowiednie wait_for."

---

## CZĘŚĆ 7 — Pierwsze 90 dni w nowej pracy

**Tydzień 1-2:**
- Poznaj projekt, stack, środowisko testowe
- Czytaj istniejące testy — nie zmieniaj, ucz się konwencji
- Pytaj o wszystko — junior ma do tego prawo

**Miesiąc 1:**
- Napraw jeden istniejący test lub dodaj jeden nowy
- Naucz się jak wygląda CI/CD w firmie (Jenkins, GitHub Actions)
- Zaproponuj jedno małe ulepszenie

**Miesiąc 2-3:**
- Weź na siebie pierwszy feature do przetestowania samodzielnie
- Naucz się Docker (jeśli jest w projekcie)
- Zacznij pisać testy API jeśli projekt ma backend

**Czego NIE robić:**
- Nie mów "w moim portfolio robiłem to inaczej" — każdy projekt jest inny
- Nie bój się mówić "nie wiem" — to lepsze niż zmyślanie
- Nie siedź cicho gdy czegoś nie rozumiesz

---

## CZĘŚĆ 8 — Widełki i negocjacje

### Orientacyjne stawki w Polsce (2025/2026):

| Rola | B2B (netto/mies.) | UoP (brutto/mies.) |
|---|---|---|
| Junior QA Manual | 4 000 – 6 000 zł | 4 500 – 6 500 zł |
| Junior QA Automation | 5 000 – 8 000 zł | 5 500 – 8 500 zł |
| Mid QA Automation | 8 000 – 14 000 zł | 8 000 – 13 000 zł |

### Jak negocjować:
- Podaj widełki, nie jedną liczbę: *"Szukam 5500-7000 zł netto B2B"*
- Sprawdź oferty na NoFluffJobs — mają obowiązek podawać widełki
- Pierwsze stanowisko — nie stawiaj wszystkiego na pieniądze, stawiaj na projekt i mentoring

---

## CZĘŚĆ 9 — Automatyzacja testów webowych krok po kroku
### Na przykładzie `www.dbcraftmode.pl`

---

### Czym jest automatyzacja testów webowych?

Automatyzacja testów webowych to zastąpienie ręcznego klikania przez testera — programem, który sam otwiera przeglądarkę, wykonuje akcje i sprawdza wyniki. Zamiast klikać "Zaloguj" 50 razy ręcznie, piszesz kod który robi to za Ciebie w 3 sekundy i robi to zawsze tak samo.

**Analogia dla rozmowy kwalifikacyjnej:**

> *"To jak makro w Excelu — zamiast wpisywać dane ręcznie, nagrywasz sekwencję. Tyle że zamiast Excela mamy przeglądarkę, a zamiast nagrywania — piszemy kod który jest dokładny, powtarzalny i można go uruchomić o każdej porze."*

---

### Od czego się zaczyna — myślenie przed kodem

Przed napisaniem pierwszej linii kodu tester zadaje sobie pytania:

**1. Co testuję?**
Logowanie do panelu admina `dbcraftmode.pl`. Panel ma formularz z e-mailem i hasłem.

**2. Jakie są scenariusze?**
- Poprawne dane → użytkownik trafia na dashboard
- Złe hasło → komunikat błędu, brak sesji
- Puste pola → walidacja formularza

**3. Jak sprawdzę że test przeszedł?**
- Po poprawnym logowaniu URL powinien zawierać `/admin/dashboard`
- Po złym haśle powinien pojawić się tekst "Nieprawidłowe dane"

**4. Jakie narzędzia?**
- Python + Pytest + Playwright
- Wzorzec Page Object Model (POM)

---

### Krok 1 — Instalacja środowiska

```bash
# Utwórz folder projektu
mkdir moje-testy
cd moje-testy

# Środowisko wirtualne (izolacja bibliotek)
python -m venv venv
venv\Scripts\activate        # Windows

# Zainstaluj biblioteki
pip install pytest playwright pytest-playwright pytest-html

# Pobierz przeglądarkę Chromium
playwright install chromium
```

**Co to jest venv?** Izolowane środowisko Pythona — biblioteki zainstalowane w projekcie nie kolidują z innymi projektami na komputerze.

---

### Krok 2 — Page Object Model (POM)

POM to wzorzec projektowy: każda strona aplikacji ma swoją **klasę** w Pythonie. Klasa zna selektory (co kliknąć) i metody (jak to zrobić). Test korzysta z metod klasy, nie z surowych selektorów.

**Bez POM — test wie za dużo:**
```python
# Kruche — jeśli ktoś zmieni id formularza, test się sypie
page.fill('#email-input', 'daniel@dbcraftmode.pl')
page.fill('#pass', 'admin123')
page.click('.btn-login')
assert '/dashboard' in page.url
```

**Z POM — test mówi CO robić, klasa wie JAK:**
```python
# Test — czytelny jak instrukcja
login = DBCraftLoginPage(page)
login.open()
login.login('daniel@dbcraftmode.pl', 'admin123')
assert login.is_logged_in()
```

**Klasa strony logowania — `pages/dbcraftmode_page.py`:**
```python
class DBCraftLoginPage(BasePage):
    URL = "https://www.dbcraftmode.pl/admin/"

    # Selektory — w jednym miejscu
    EMAIL_INPUT    = 'input[name="email"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON  = 'button[type="submit"]'
    ERROR_MESSAGE  = '.error-message'
    DASHBOARD_URL  = '/admin/dashboard'

    def open(self):
        self.page.goto(self.URL)

    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.SUBMIT_BUTTON)

    def is_logged_in(self) -> bool:
        return self.DASHBOARD_URL in self.page.url

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text()
```

**Dlaczego POM?** Jeśli programista zmieni `input[name="email"]` na `input[id="admin-email"]` — zmieniasz w jednym miejscu w klasie, a nie w każdym teście osobno.

---

### Krok 3 — Fixtures w conftest.py

Fixture to gotowy "stan" który Pytest przygotowuje przed testem. Zamiast każdy test logował się osobno — jeden fixture robi to raz i przekazuje gotową sesję.

```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,   # polskie hostingi mają niestandardowe SSL
    }

@pytest.fixture(scope="class")
def logged_in(page):
    """Zwraca stronę z aktywną sesją admina."""
    from pages.dbcraftmode_page import DBCraftLoginPage
    login = DBCraftLoginPage(page)
    login.open()
    login.login('daniel@dbcraftmode.pl', 'admin123')
    assert login.is_logged_in(), "Fixture: logowanie nie powiodło się"
    return page
```

`scope="class"` oznacza: zaloguj się raz dla całej klasy testowej, nie przed każdym testem osobno.

---

### Krok 4 — Testy

```python
# tests/dbcraftmode/test_dbcraftmode.py
import pytest
from pages.dbcraftmode_page import DBCraftLoginPage, DBCraftDashboardPage, DBCraftBlogPage

class TestLogin:

    def test_TC04_wrong_email_shows_error(self, page):
        """TC-04: Nieprawidłowy email → komunikat błędu."""
        login = DBCraftLoginPage(page)
        login.open()
        login.login('zly@email.pl', 'admin123')

        error = login.get_error_message()
        assert 'Nieprawidłowe' in error, f"Oczekiwano błędu, dostałem: '{error}'"
        assert not login.is_logged_in(), "Nie powinien być zalogowany"

    def test_TC05_wrong_password_shows_error(self, page):
        """TC-05: Złe hasło → błąd, brak sesji."""
        login = DBCraftLoginPage(page)
        login.open()
        login.login('daniel@dbcraftmode.pl', 'zlehaslo')

        assert not login.is_logged_in()

    def test_TC06_correct_login_redirects_to_dashboard(self, page):
        """TC-06: Poprawne dane → dashboard."""
        login = DBCraftLoginPage(page)
        login.open()
        login.login('daniel@dbcraftmode.pl', 'admin123')

        assert login.is_logged_in(), "Po poprawnym logowaniu powinien być dashboard"


class TestBlog:

    def test_TC09_blog_list_loads(self, logged_in):
        """TC-09: Lista wpisów bloga ładuje się."""
        blog = DBCraftBlogPage(logged_in)
        blog.open_list()
        assert blog.is_list_visible()

    def test_TC12_add_draft_post(self, logged_in):
        """TC-12: Dodanie szkicu — pojawia się na liście."""
        blog = DBCraftBlogPage(logged_in)
        blog.open_add_form()
        blog.fill_title('Test automatyczny — szkic')
        blog.fill_content('Treść testowa.')
        blog.save_as_draft()

        assert blog.is_success_message_visible()
```

---

### Krok 5 — Uruchomienie i raport

```bash
# Uruchom wszystkie testy z raportem HTML
pytest tests/ --html=reports/report.html --self-contained-html -v

# Tylko testy dbcraftmode
pytest tests/dbcraftmode/ -v

# Z widoczną przeglądarką (do debugowania)
pytest tests/dbcraftmode/ --headed -v
```

**Przykładowy wynik:**
```
tests/dbcraftmode/test_dbcraftmode.py::TestLogin::test_TC04_wrong_email_shows_error  PASSED
tests/dbcraftmode/test_dbcraftmode.py::TestLogin::test_TC05_wrong_password_shows_error PASSED
tests/dbcraftmode/test_dbcraftmode.py::TestLogin::test_TC06_correct_login_redirects_to_dashboard PASSED
tests/dbcraftmode/test_dbcraftmode.py::TestBlog::test_TC09_blog_list_loads PASSED
tests/dbcraftmode/test_dbcraftmode.py::TestBlog::test_TC12_add_draft_post PASSED

5 passed in 8.3s
```

Raport HTML otwierasz w przeglądarce — widać każdy test, czas trwania, zielony lub czerwony wynik.

---

### Krok 6 — Co zrobić gdy test nie przejdzie

Gdy test pada (`FAILED`), Playwright pokazuje:
1. **Screenshot** — jak wyglądała strona w momencie błędu
2. **Komunikat asercji** — co było oczekiwane vs co dostał test
3. **Ślad stosu** — w której linii kodu test się wyłożył

```
FAILED tests/dbcraftmode/test_dbcraftmode.py::TestLogin::test_TC06
AssertionError: Po poprawnym logowaniu powinien być dashboard
assert '/admin/dashboard' in 'https://www.dbcraftmode.pl/admin/'
```

**Diagnozo:** po kliknięciu "Zaloguj" przeglądarka wróciła na stronę logowania. Przyczyna mogła być:
- Złe dane (zły email — to był mój rzeczywisty błąd podczas projektu)
- Sesja wygasła
- Błąd CSRF tokenu
- Problem z siecią

**Debug:** dodaję `--headed` żeby zobaczyć co przeglądarka robi i `print(page.url)` po każdym kroku.

---

### Jak opowiedzieć o tym na rozmowie kwalifikacyjnej

**Pytanie: "Pokaż mi jak testowałeś dbcraftmode.pl"**

> *"Zacząłem od analizy aplikacji — zidentyfikowałem 6 modułów: logowanie, dashboard, blog, pomysły, projekty, wylogowanie. Dla każdego napisałem przypadki testowe: happy path i błędne scenariusze.*
>
> *Użyłem wzorca Page Object Model — każda strona ma klasę z selektorami. To pozwala na łatwą zmianę selektorów bez modyfikowania testów.*
>
> *Napotkałem realny bug: wszystkie testy po logowaniu padały bo miałem zły adres email w konfiguracji — stary email z setupu, nie ten z produkcyjnej bazy. Zdebuggowałem to przez `print(page.url)` po logowaniu — URL wskazywał na stronę logowania zamiast dashboardu.*
>
> *Efekt: 17 testów, 0 failed, raport HTML z wynikami."*

**Pytanie: "Dlaczego Playwright, nie Selenium?"**

> *"Playwright ma wbudowany auto-wait — nie trzeba ręcznie czekać na elementy. Jest szybszy i nowocześniejszy. Selenium jest nadal popularne w starszych projektach, ale Playwright to obecny standard dla nowych projektów."*

**Pytanie: "Co to jest Page Object Model?"**

> *"Wzorzec projektowy gdzie każda strona ma swoją klasę. Selektory są w klasie, testy korzystają z metod. Zmiana jednego selektora to edycja w jednym miejscu, nie w każdym teście. W moim projekcie mam 6 takich klas."*

---

### Schemat całego procesu (do zapamiętania)

```
1. ANALIZA          → co testuję, jakie moduły, jakie scenariusze
2. PRZYPADKI TC     → happy path + błędne dane + edge cases
3. PAGE OBJECT      → klasy stron z selektorami i metodami
4. FIXTURES         → przygotowanie stanu (zalogowanie, baza)
5. TESTY            → assert: oczekiwany wynik vs rzeczywisty
6. RAPORT           → HTML z wynikami, screenshoty przy błędach
7. DEBUG            → --headed, print(page.url), logi
```

---

## PODSUMOWANIE — Lista kontrolna przed pierwszą aplikacją

```
[ ] GitHub — publiczne repo z README, działający kod
[ ] LinkedIn — profesjonalny nagłówek, sekcja About, certyfikat SDA
[ ] CV — jedna strona, konkretne liczby, PDF
[ ] Portfolio — możesz pokazać raport HTML z działającymi testami
[ ] Elevator pitch — jedno zdanie o tym co robisz
[ ] Odpowiedzi na 5 pytań technicznych z rozdziału 6
[ ] Lista 10 firm do których aplikusjesz w tym tygodniu
```

---

> **Pamiętaj:** Pierwszy job w IT jest najtrudniejszy. Każda odmowa przybliża Cię do tej jednej odpowiedzi "tak". Masz konkretne testy na żywych stronach, certyfikat i udokumentowane projekty. To więcej niż większość juniorów wysyłających CV.
>
> **Działaj systematycznie. Nie czekaj aż będzie "gotowe". Jest gotowe.**

---

*KPK stworzony: 2026-05-21 | Daniel Bryjak — QA Automation Engineer*
