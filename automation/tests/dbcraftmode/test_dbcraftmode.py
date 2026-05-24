"""
Testy automatyczne — www.dbcraftmode.pl
Panel administracyjny PHP CMS (portfolio Daniela Bryjaka)

Moduły:
  TestLoginSmoke   — TC-01..03  Strona logowania
  TestLogin        — TC-04..06  Logowanie (błędne / poprawne / wylogowanie)
  TestDashboard    — TC-07..08  Panel główny po zalogowaniu
  TestBlog         — TC-09..12  Lista i dodawanie wpisów bloga
  TestIdeas        — TC-13..15  Lista i dodawanie pomysłów
  TestProjects     — TC-16..17  Lista projektów
"""

import pytest
import time
from pages.dbcraftmode_page import (
    DBCraftLoginPage, DBCraftDashboard,
    DBCraftBlogPage, DBCraftIdeasPage, DBCraftProjectsPage,
    ADMIN_EMAIL, ADMIN_PASS, BASE_URL
)

UNIQUE = str(int(time.time()))   # unikalny suffix — zapobiega kolizjom w bazie


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def do_login(page):
    login = DBCraftLoginPage(page)
    login.open()
    login.login(ADMIN_EMAIL, ADMIN_PASS)
    return login


# ──────────────────────────────────────────────
#  FIXTURES
# ──────────────────────────────────────────────

@pytest.fixture()
def login_page(page):
    lp = DBCraftLoginPage(page)
    lp.open()
    return lp

@pytest.fixture()
def logged_in(page):
    do_login(page)
    return page


# ──────────────────────────────────────────────
#  SMOKE — STRONA LOGOWANIA
# ──────────────────────────────────────────────

class TestLoginSmoke:

    def test_TC01_login_page_loads(self, login_page):
        """TC-01: Strona logowania ładuje się z tytułem i formularzem."""
        assert "Logowanie" in login_page.page.title() or "Admin" in login_page.page.title(), \
            f"Nieoczekiwany tytuł: '{login_page.page.title()}'"

    def test_TC02_login_form_fields(self, login_page):
        """TC-02: Formularz logowania ma pola email i hasło."""
        assert login_page.page.locator(login_page.EMAIL_INPUT).is_visible(), "Brak pola email"
        assert login_page.page.locator(login_page.PASS_INPUT).is_visible(), "Brak pola hasła"
        assert login_page.page.locator(login_page.BTN_SUBMIT).is_visible(), "Brak przycisku logowania"

    def test_TC03_logo_visible(self, login_page):
        """TC-03: Logo 'DB' jest widoczne na stronie logowania."""
        logo = login_page.page.locator(login_page.LOGO_ICON)
        assert logo.is_visible(), "Logo DB nie jest widoczne"
        assert "DB" in logo.inner_text()


# ──────────────────────────────────────────────
#  LOGOWANIE
# ──────────────────────────────────────────────

class TestLogin:

    def test_TC04_wrong_email_format(self, login_page):
        """TC-04: Nieprawidłowy format e-mail → błąd walidacji."""
        login_page.login("to-nie-jest-email", "jakiesthaslo")
        assert login_page.is_error_visible(), "Oczekiwano komunikatu błędu dla złego formatu email"
        assert len(login_page.get_error_text()) > 0

    def test_TC05_wrong_password(self, login_page):
        """TC-05: Poprawny email, błędne hasło → komunikat błędu."""
        login_page.login(ADMIN_EMAIL, "zle_haslo_9999")
        assert login_page.is_error_visible(), "Oczekiwano komunikatu błędu"
        error = login_page.get_error_text()
        assert "hasło" in error.lower() or "email" in error.lower() or len(error) > 0

    def test_TC06_correct_login_and_dashboard(self, login_page):
        """TC-06: Poprawne dane → przekierowanie na dashboard."""
        login_page.login(ADMIN_EMAIL, ADMIN_PASS)
        assert "dashboard" in login_page.page.url or \
               ("/admin/" in login_page.page.url and "index" not in login_page.page.url), \
               f"Oczekiwano dashboard, jest: {login_page.page.url}"


# ──────────────────────────────────────────────
#  DASHBOARD
# ──────────────────────────────────────────────

class TestDashboard:

    def test_TC07_sidebar_visible(self, logged_in):
        """TC-07: Sidebar z nawigacją jest widoczny po zalogowaniu."""
        dash = DBCraftDashboard(logged_in)
        dash.open()
        assert dash.is_sidebar_visible(), "Sidebar nie jest widoczny"

    def test_TC08_sidebar_has_key_links(self, logged_in):
        """TC-08: Sidebar zawiera linki do Blog, Pomysły, Projekty."""
        dash = DBCraftDashboard(logged_in)
        dash.open()
        links_text = " ".join(dash.get_sidebar_links()).lower()
        assert "blog" in links_text, f"Brak 'Blog' w sidebaru: {links_text[:200]}"
        assert "projekt" in links_text or "pomysł" in links_text or "idea" in links_text, \
            f"Brak linków do projektów/pomysłów: {links_text[:200]}"


# ──────────────────────────────────────────────
#  BLOG
# ──────────────────────────────────────────────

class TestBlog:

    def test_TC09_blog_list_loads(self, logged_in):
        """TC-09: Strona listy wpisów bloga ładuje się."""
        blog = DBCraftBlogPage(logged_in)
        blog.open_list()
        assert "blog" in blog.page.url.lower() or "Blog" in blog.page.title()

    def test_TC10_blog_add_form_loads(self, logged_in):
        """TC-10: Formularz dodawania wpisu bloga ładuje się z polami."""
        blog = DBCraftBlogPage(logged_in)
        blog.open_add_form()
        assert blog.page.locator(blog.TITLE_INPUT).is_visible(), "Brak pola Tytuł w formularzu bloga"
        assert blog.page.locator(blog.BTN_SAVE).first.is_visible(), "Brak przycisku Zapisz"

    def test_TC11_blog_add_empty_title_fails(self, logged_in):
        """TC-11: Próba zapisu wpisu bez tytułu → błąd walidacji."""
        blog = DBCraftBlogPage(logged_in)
        blog.open_add_form()
        blog.save_post()
        # Po zapisie bez tytułu powinniśmy zostać na formularzu (walidacja server-side)
        assert "blog-add" in blog.page.url or blog.page.locator(blog.ERROR_LIST).count() > 0 or \
               blog.page.locator(".error").count() > 0, \
               "Oczekiwano błędu walidacji lub pozostania na formularzu"

    def test_TC12_blog_add_draft_post(self, logged_in):
        """TC-12: Dodanie wpisu jako szkic → pojawia się na liście."""
        title = f"TEST AUTOMATYCZNY — wpis {UNIQUE}"
        blog = DBCraftBlogPage(logged_in)
        blog.open_add_form()
        blog.fill_post(title=title, content="Treść testowa dodana automatycznie przez Playwright.", status="draft")
        blog.save_post()
        # Po zapisie → redirect na listę lub flash success
        saved = blog.post_exists_in_list(title)
        assert saved, f"Wpis '{title}' nie pojawił się na liście bloga"


# ──────────────────────────────────────────────
#  POMYSŁY (IDEAS)
# ──────────────────────────────────────────────

class TestIdeas:

    def test_TC13_ideas_list_loads(self, logged_in):
        """TC-13: Strona listy pomysłów ładuje się."""
        ideas = DBCraftIdeasPage(logged_in)
        ideas.open_list()
        assert "idea" in ideas.page.url.lower() or "pomys" in ideas.page.title().lower() or \
               ideas.page.locator("h1, h2").count() > 0

    def test_TC14_ideas_add_form_loads(self, logged_in):
        """TC-14: Formularz dodawania pomysłu ładuje się z polami."""
        ideas = DBCraftIdeasPage(logged_in)
        ideas.open_add_form()
        assert ideas.page.locator(ideas.TITLE_INPUT).is_visible(), "Brak pola Tytuł w formularzu pomysłu"
        assert ideas.page.locator(ideas.CONCEPT_AREA).is_visible(), "Brak pola Koncept"

    def test_TC15_ideas_add_new(self, logged_in):
        """TC-15: Dodanie nowego pomysłu → pojawia się na liście."""
        title = f"Pomysł testowy {UNIQUE}"
        ideas = DBCraftIdeasPage(logged_in)
        ideas.open_add_form()
        ideas.fill_idea(title=title, concept="Automatyczny test dodawania pomysłu przez Playwright.")
        ideas.save_idea()
        saved = ideas.idea_exists_in_list(title)
        assert saved, f"Pomysł '{title}' nie pojawił się na liście"


# ──────────────────────────────────────────────
#  PROJEKTY
# ──────────────────────────────────────────────

class TestProjects:

    def test_TC16_projects_list_loads(self, logged_in):
        """TC-16: Strona listy projektów ładuje się."""
        projects = DBCraftProjectsPage(logged_in)
        projects.open_list()
        assert "project" in projects.page.url.lower() or \
               "projekt" in projects.page.title().lower() or \
               projects.page.locator("h1, h2").count() > 0

    def test_TC17_projects_list_has_content(self, logged_in):
        """TC-17: Lista projektów zawiera co najmniej jeden projekt."""
        projects = DBCraftProjectsPage(logged_in)
        projects.open_list()
        count = projects.get_project_count()
        assert count > 0, f"Lista projektów jest pusta (znaleziono: {count})"
