"""
Testy formularza logowania — sklep Saucedemo (www.saucedemo.com)

Saucedemo to sklep demo stworzony specjalnie do prezentacji automatyzacji testów.
Zawiera wbudowane konta testowe symulujące różne scenariusze:

  TC-01  Logowanie — błędne hasło          → komunikat błędu
  TC-02  Logowanie — prawidłowe dane       → panel sklepu
  TC-03  Logowanie — zablokowane konto     → komunikat o blokadzie
  TC-04  Logowanie — puste pola            → walidacja formularza
"""

import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USER = "locked_out_user"
WRONG_PASSWORD = "wrong_password_123"


@pytest.fixture(autouse=True)
def open_store(page):
    home = HomePage(page)
    home.open()
    yield page


class TestLogin:

    def test_TC01_wrong_password(self, page):
        """TC-01: Błędne hasło → komunikat błędu, brak zalogowania."""
        login = LoginPage(page)
        login.login(VALID_USER, WRONG_PASSWORD)

        assert login.is_error_visible(), "Oczekiwano komunikatu błędu"
        assert "Epic sadface" in login.get_error_message(), "Niepoprawna treść komunikatu błędu"

        home = HomePage(page)
        assert not home.is_logged_in(), "Użytkownik nie powinien być zalogowany"

    def test_TC02_valid_login(self, page):
        """TC-02: Prawidłowe dane → zalogowanie i wylogowanie."""
        login = LoginPage(page)
        login.login(VALID_USER, VALID_PASSWORD)

        home = HomePage(page)
        assert home.is_logged_in(), "Użytkownik powinien być zalogowany"
        assert home.get_page_title() == "Products", f"Oczekiwano tytułu 'Products', got: {home.get_page_title()}"

        home.logout()
        assert not home.is_logged_in(), "Użytkownik powinien być wylogowany"

    def test_TC03_locked_account(self, page):
        """TC-03: Zablokowane konto → komunikat o blokadzie."""
        login = LoginPage(page)
        login.login(LOCKED_USER, VALID_PASSWORD)

        assert login.is_error_visible(), "Oczekiwano komunikatu o blokadzie"
        error = login.get_error_message()
        assert "locked out" in error.lower(), f"Oczekiwano info o blokadzie konta, got: {error}"

    def test_TC04_empty_fields(self, page):
        """TC-04: Puste pola → walidacja formularza."""
        login = LoginPage(page)
        login.login("", "")

        assert login.is_error_visible(), "Oczekiwano komunikatu walidacji"
        error = login.get_error_message()
        assert "Username is required" in error, f"Oczekiwano walidacji pola, got: {error}"
