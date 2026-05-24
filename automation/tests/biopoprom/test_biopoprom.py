"""
Testy automatyczne — www.biopoprom.pl
Aplikacja: Zegar BIOPOPROM (20-godzinny system czasu naturalnego)

Struktura testów:
  TC-01  Smoke: ładowanie strony i tytuł
  TC-02  Smoke: widoczność zegara i czasu
  TC-03  Smoke: widoczność nawigacji (4 zakładki)
  TC-04  Nawigacja: przełączanie zakładek
  TC-05  Zegar: czas BP i standardowy są wyświetlone
  TC-06  Zegar: faza księżyca jest wyświetlona
  TC-07  Kalendarz: siatka kalendarza się renderuje
  TC-08  Kalendarz: nawigacja poprzedni/następny miesiąc
  TC-09  Sieć: kalkulator STD→BP
  TC-10  Sieć: kalkulator BP→STD
  TC-11  Harmonia: kalkulator złotego podziału
  TC-12  Harmonia: przycisk 432 Hz zmienia aktywny preset
"""

import pytest
import re
from pages.biopoprom_page import BiopopromPage

BIOPOPROM_MONTHS = [
    "LÓD", "ODWILŻ", "KIEŁEK", "PĄK", "KWIAT", "ŁĄKA",
    "ZENIT", "ŻAR", "PLON", "MGŁA", "LIŚĆ", "MRÓZ", "CISZA"
]


@pytest.fixture(autouse=True)
def open_app(page):
    app = BiopopromPage(page)
    app.open()
    yield app


class TestSmoke:

    def test_TC01_page_loads(self, page):
        """TC-01: Strona ładuje się z poprawnym tytułem."""
        assert page.title() == "BIOPOPROM", f"Nieoczekiwany tytuł: {page.title()}"

    def test_TC02_clock_visible(self, open_app):
        """TC-02: Zegar i czas BP są widoczne na starcie."""
        app = open_app
        assert page_locator_visible(app, app.CLOCK_CANVAS), "Zegar nie jest widoczny"
        assert page_locator_visible(app, app.BP_TIME), "Czas BP nie jest widoczny"
        assert page_locator_visible(app, app.REAL_TIME), "Czas standardowy nie jest widoczny"

    def test_TC03_navigation_tabs(self, open_app):
        """TC-03: Nawigacja zawiera 4 zakładki."""
        labels = open_app.get_tab_labels()
        assert len(labels) == 4, f"Oczekiwano 4 zakładek, znaleziono: {len(labels)}"
        all_text = " ".join(labels).upper()
        assert "ZEGAR" in all_text
        assert "KALENDARZ" in all_text
        assert "HARMONIA" in all_text


class TestNavigation:

    def test_TC04_tab_switching(self, open_app):
        """TC-04: Przełączanie między zakładkami aktywuje właściwe sekcje."""
        app = open_app

        # Start: aktywna jest sekcja Zegar
        assert app.is_section_active("zegar"), "Sekcja Zegar powinna być aktywna na starcie"
        assert not app.is_section_active("kalendarz")

        # Klik Kalendarz
        app.switch_tab("kalendarz")
        assert app.is_section_active("kalendarz"), "Sekcja Kalendarz powinna być aktywna"
        assert not app.is_section_active("zegar")

        # Klik Siec
        app.switch_tab("siec")
        assert app.is_section_active("siec"), "Sekcja Siec powinna byc aktywna"

        # Klik Harmonia
        app.switch_tab("harmonia")
        assert app.is_section_active("harmonia"), "Sekcja Harmonia powinna byc aktywna"

        # Powrot do Zegar
        app.switch_tab("zegar")
        assert app.is_section_active("zegar"), "Powrot do Zegar - sekcja powinna byc aktywna"


class TestZegar:

    def test_TC05_time_displayed(self, open_app):
        """TC-05: Czas BP i standardowy mają format HH:MM:SS i nie są puste."""
        app = open_app
        app.page.wait_for_timeout(1200)
        bp = app.get_bp_time()
        real = app.get_real_time()
        time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        assert time_pattern.match(bp), f"Czas BP ma niepoprawny format: '{bp}'"
        assert time_pattern.match(real), f"Czas standardowy ma niepoprawny format: '{real}'"
        assert bp != "--:--:--", "Czas BP nie został zainicjowany"

    def test_TC06_moon_phase(self, open_app):
        """TC-06: Faza księżyca jest wyświetlona i niepusta."""
        app = open_app
        app.page.wait_for_timeout(1000)
        phase = app.get_moon_phase()
        assert phase and phase != "—", f"Faza ksiezycowa jest pusta: '{phase}'"
        known_phases = ["Nów", "Pełnia", "Sierp", "Kwadra", "Garbaty"]
        assert any(p in phase for p in known_phases), f"Nieznana faza: '{phase}'"


class TestKalendarz:

    def test_TC07_calendar_renders(self, open_app):
        """TC-07: Po przejściu na Kalendarz renderuje się siatka z komórkami."""
        app = open_app
        app.switch_tab("kalendarz")
        app.page.wait_for_timeout(500)
        month_name = app.get_month_name()
        assert month_name, "Nazwa miesiaca jest pusta"
        assert any(m in month_name for m in BIOPOPROM_MONTHS), f"Nieznana nazwa miesiaca: '{month_name}'"
        days = app.page.locator(".cal-d").all()
        assert len(days) >= 28, f"Siatka powinna miec min. 28 komorek, ma: {len(days)}"

    def test_TC08_month_navigation(self, open_app):
        """TC-08: Przyciski poprzedni/następny zmieniają wyświetlany miesiąc."""
        app = open_app
        app.switch_tab("kalendarz")
        app.page.wait_for_timeout(500)
        before = app.get_month_name()
        app.click_next_month()
        after = app.get_month_name()
        assert before != after, f"Nazwa miesiaca powinna sie zmienic po kliknieciu Nastepny: {before} -> {after}"
        app.click_prev_month()
        restored = app.get_month_name()
        assert restored == before, f"Po cofnieciu miesiąc powinien wrócić do: {before}, jest: {restored}"


class TestSiec:

    def test_TC09_calculator_std_to_bp(self, open_app):
        """TC-09: Kalkulator STD→BP zwraca wynik dla poprawnego wejścia."""
        app = open_app
        app.switch_tab("siec")
        app.page.wait_for_timeout(600)
        result = app.calculate_std_to_bp("12:00")
        assert result and result != "—", f"Kalkulator nie zwrocil wyniku: '{result}'"
        time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        assert time_pattern.match(result), f"Wynik ma niepoprawny format: '{result}'"

    def test_TC10_calculator_bp_to_std(self, open_app):
        """TC-10: Kalkulator BP→STD zwraca wynik dla poprawnego wejścia."""
        app = open_app
        app.switch_tab("siec")
        app.page.wait_for_timeout(600)
        result = app.calculate_bp_to_std("10:00")
        assert result and result != "—", f"Kalkulator nie zwrocil wyniku: '{result}'"
        time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        assert time_pattern.match(result), f"Wynik ma niepoprawny format: '{result}'"


class TestHarmonia:

    def test_TC11_golden_ratio_calculator(self, open_app):
        """TC-11: Kalkulator złotego podziału zwraca wyniki dla podanego wzrostu."""
        app = open_app
        app.switch_tab("harmonia")
        app.page.wait_for_timeout(800)
        results = app.calculate_phi(175)
        assert results, "Kalkulator zlotego podzialu nie zwrocil wynikow"
        assert "cm" in results, f"Wyniki powinny zawierac jednostke 'cm': '{results}'"
        assert "1.618" in results or "phi" in results.lower() or "JN" in results or "Proporcja" in results, \
            "Wyniki powinny zawierac proporcje phi"

    def test_TC12_hz_preset_buttons(self, open_app):
        """TC-12: Kliknięcie przycisku 528 Hz aktywuje go i zmienia częstotliwość."""
        app = open_app
        app.switch_tab("harmonia")
        app.page.wait_for_timeout(800)

        btn_528 = app.page.locator(".preset-btn", has_text="528 Hz")
        btn_528.click()
        app.page.wait_for_timeout(300)

        assert "active" in (btn_528.get_attribute("class") or ""), "Przycisk 528 Hz powinien byc aktywny"
        hz_text = app.page.locator(app.HZ_NUM).inner_text()
        assert "528" in hz_text, f"Wyswietlana czestotliwosc powinna byc 528 Hz, jest: '{hz_text}'"


# ---------- helper ----------
def page_locator_visible(app, selector: str) -> bool:
    return app.page.locator(selector).is_visible()
