"""
Testy automatyczne — www.koparka-kobierzyce.pl
Strona firmowa usług koparką w Gminie Kobierzyce (projekt dla klienta)

Moduły:
  TestSmoke       — TC-01..TC-03  Podstawowe ładowanie strony
  TestNawigacja   — TC-04..TC-05  Menu i linki
  TestSekcje      — TC-06..TC-07  Widoczność kluczowych sekcji
  TestFormularz   — TC-08..TC-10  Formularz kontaktowy (walidacja)
  TestBlog        — TC-11..TC-13  Blog i artykuły
  TestCRM         — TC-14..TC-16  Panel CRM (logowanie)
"""

import pytest
from pages.koparka_page import KoparkaHomePage, KoparkaBlogPage, KoparkaCrmPage, CRM_PASSWORD

BASE_URL = "https://koparka-kobierzyce.pl"


# ──────────────────────────────────────────────
#  FIXTURES
# ──────────────────────────────────────────────

@pytest.fixture()
def home(page):
    hp = KoparkaHomePage(page)
    hp.open()
    return hp

@pytest.fixture()
def blog(page):
    bp = KoparkaBlogPage(page)
    bp.open()
    return bp

@pytest.fixture()
def crm(page):
    cp = KoparkaCrmPage(page)
    cp.open_login()
    return cp


# ──────────────────────────────────────────────
#  SMOKE
# ──────────────────────────────────────────────

class TestSmoke:

    def test_TC01_title(self, home):
        """TC-01: Tytuł strony zawiera nazwę firmy."""
        title = home.page.title()
        assert "KOPARKI Kobierzyce" in title, f"Nieoczekiwany tytuł: '{title}'"

    def test_TC02_logo_visible(self, home):
        """TC-02: Logo firmy (KK) jest widoczne."""
        assert home.page.locator(home.LOGO_CIRCLE).is_visible(), "Logo KK nie jest widoczne"
        logo_text = home.page.locator(home.LOGO_CIRCLE).inner_text()
        assert "KK" in logo_text

    def test_TC03_hero_visible(self, home):
        """TC-03: Sekcja hero z nagłówkiem jest widoczna."""
        hero = home.page.locator(home.HERO_TITLE)
        assert hero.is_visible(), "Hero title nie jest widoczny"
        text = hero.inner_text()
        assert len(text) > 10, "Hero title jest za krótki"


# ──────────────────────────────────────────────
#  NAWIGACJA
# ──────────────────────────────────────────────

class TestNawigacja:

    def test_TC04_nav_links_present(self, home):
        """TC-04: Menu zawiera kluczowe linki nawigacyjne."""
        links = home.get_nav_links()
        all_text = " ".join(links).upper()
        assert "BLOG" in all_text, f"Brak linku Blog w nawigacji: {links}"
        assert "KALKULATOR" in all_text, f"Brak linku Kalkulator: {links}"

    def test_TC05_blog_link_navigates(self, home):
        """TC-05: Klik w link Blog otwiera stronę bloga."""
        home.page.locator(".topbar-nav a", has_text="Blog").click()
        home.page.wait_for_load_state("domcontentloaded")
        assert "/blog" in home.page.url, f"Oczekiwano URL z /blog, jest: {home.page.url}"
        assert "Blog" in home.page.title(), f"Oczekiwano tytułu z 'Blog', jest: {home.page.title()}"


# ──────────────────────────────────────────────
#  SEKCJE STRONY GŁÓWNEJ
# ──────────────────────────────────────────────

class TestSekcje:

    def test_TC06_main_sections_exist(self, home):
        """TC-06: Kluczowe sekcje strony istnieją w DOM."""
        for section_id in ["oferta", "wykopy", "przylacza", "realizacje", "kontakt"]:
            count = home.page.locator(f"#{section_id}").count()
            assert count > 0, f"Sekcja #{section_id} nie istnieje w DOM"

    def test_TC07_footer_present(self, home):
        """TC-07: Stopka strony jest widoczna i zawiera nazwę firmy."""
        footer = home.page.locator("footer")
        assert footer.is_visible(), "Stopka nie jest widoczna"
        assert "KOPARKI Kobierzyce" in footer.inner_text()


# ──────────────────────────────────────────────
#  FORMULARZ KONTAKTOWY
# ──────────────────────────────────────────────

class TestFormularz:

    def test_TC08_form_fields_exist(self, home):
        """TC-08: Formularz kontaktowy zawiera pola imię, telefon, usługa."""
        home.scroll_to("kontakt")
        home.page.wait_for_timeout(500)
        assert home.page.locator(home.FIELD_NAME).count() > 0, "Brak pola 'Imię'"
        assert home.page.locator(home.FIELD_PHONE).count() > 0, "Brak pola 'Telefon'"
        assert home.page.locator(home.SELECT_SERVICE).count() > 0, "Brak listy wyboru usługi"
        assert home.page.locator(home.BTN_SUBMIT).is_visible(), "Brak przycisku Submit"

    def test_TC09_form_submit_button_text(self, home):
        """TC-09: Przycisk wysyłania formularza ma poprawny tekst."""
        home.scroll_to("kontakt")
        home.page.wait_for_timeout(500)
        btn_text = home.page.locator(home.BTN_SUBMIT).inner_text()
        assert "wycen" in btn_text.lower() or "wyślij" in btn_text.lower(), \
            f"Nieoczekiwany tekst przycisku: '{btn_text}'"

    def test_TC10_form_service_options(self, home):
        """TC-10: Lista usług zawiera wszystkie opcje."""
        home.scroll_to("kontakt")
        home.page.wait_for_timeout(500)
        options = home.page.locator(f"{home.SELECT_SERVICE} option").all_inner_texts()
        options_text = " ".join(options).lower()
        assert "fundament" in options_text, "Brak opcji 'Wykop pod fundamenty'"
        assert "szambo" in options_text, "Brak opcji 'Szambo'"
        assert "niwelacja" in options_text, "Brak opcji 'Niwelacja'"


# ──────────────────────────────────────────────
#  BLOG
# ──────────────────────────────────────────────

class TestBlog:

    def test_TC11_blog_page_loads(self, blog):
        """TC-11: Strona bloga ładuje się z poprawnym tytułem."""
        title = blog.page.title()
        assert "Blog" in title or "blog" in title.lower(), f"Nieoczekiwany tytuł bloga: '{title}'"
        assert "/blog/" in blog.page.url

    def test_TC12_blog_has_articles(self, blog):
        """TC-12: Blog zawiera co najmniej jeden artykuł."""
        count = blog.get_article_count()
        assert count >= 1, f"Blog powinien mieć min. 1 artykuł, ma: {count}"

    def test_TC13_blog_article_opens(self, blog):
        """TC-13: Kliknięcie w artykuł otwiera jego stronę."""
        initial_url = blog.page.url
        blog.open_first_article()
        assert blog.page.url != initial_url, "URL nie zmienił się po kliknięciu artykułu"
        assert len(blog.page.title()) > 0, "Tytuł artykułu jest pusty"


# ──────────────────────────────────────────────
#  CRM — PANEL ADMINA
# ──────────────────────────────────────────────

class TestCRM:

    def test_TC14_crm_login_page_loads(self, crm):
        """TC-14: Strona logowania CRM ładuje się poprawnie."""
        assert "/crm/login" in crm.page.url
        assert "Logowanie" in crm.page.title() or "CRM" in crm.page.title(), \
            f"Nieoczekiwany tytuł: '{crm.page.title()}'"
        assert crm.page.locator(crm.PWD_INPUT).is_visible(), "Pole hasła nie jest widoczne"

    def test_TC15_crm_wrong_password(self, crm):
        """TC-15: Błędne hasło → komunikat błędu, brak przekierowania."""
        crm.login("bledne_haslo_123")
        assert crm.is_error_visible(), "Oczekiwano komunikatu błędu"
        error = crm.get_error_text()
        assert len(error) > 0, "Komunikat błędu jest pusty"
        assert "/crm/login" in crm.page.url, "Nie powinno nastąpić przekierowanie po błędnym haśle"

    def test_TC16_crm_correct_password(self, crm):
        """TC-16: Poprawne hasło → przekierowanie do panelu CRM."""
        crm.login(CRM_PASSWORD)
        assert crm.is_logged_in(), \
            f"Powinno nastąpić przekierowanie po poprawnym haśle, URL: {crm.page.url}"
        assert "/crm/" in crm.page.url
        crm.logout()
        assert "/crm/login" in crm.page.url, "Po wylogowaniu powinien być redirect na login"
