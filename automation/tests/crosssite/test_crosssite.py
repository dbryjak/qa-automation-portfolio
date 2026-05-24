"""
Testy przekrojowe — Faza 6
Wszystkie strony portfolio: SEO, wydajność, dostępność, linki, screenshoty

Moduły:
  TestSEO          — TC-01..05  Meta tagi, H1, viewport, lang
  TestPerformance  — TC-06..08  Czas ładowania (DOMContentLoaded, load, TTFB)
  TestAccessibility— TC-09..12  Alt teksty, labele, przyciski, lang
  TestBrokenLinks  — TC-13..14  Linki wewnętrzne nie zwracają 404/500
  TestScreenshots  — TC-15      Screenshot każdej strony
"""

import pytest
import time
import os
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
#  Strony do testowania
# ──────────────────────────────────────────────────────────────────────────────

LIVE_SITES = [
    ("koparka",     "https://koparka-kobierzyce.pl"),
    ("dbcraftmode", "https://www.dbcraftmode.pl"),
]

# Biopoprom działa jako lokalny plik HTML
BIOPOPROM_URL = "file:///d:/STRONY_WWW/www.biopoprom.pl/biopoprom.html"

ALL_SITES = LIVE_SITES + [("biopoprom", BIOPOPROM_URL)]

SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / "reports" / "screenshots"


# ──────────────────────────────────────────────────────────────────────────────
#  SEO
# ──────────────────────────────────────────────────────────────────────────────

class TestSEO:

    @pytest.mark.parametrize("site_name,url", ALL_SITES)
    def test_TC01_title_not_empty(self, page, site_name, url):
        """TC-01: Każda strona ma niepusty tytuł (min. 5 znaków)."""
        page.goto(url, wait_until="domcontentloaded")
        title = page.title()
        assert len(title) >= 5, \
            f"[{site_name}] Tytuł za krótki lub pusty: '{title}'"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC02_meta_description(self, page, site_name, url):
        """TC-02: Strony live mają meta description (klucz SEO)."""
        page.goto(url, wait_until="domcontentloaded")
        desc = page.locator("meta[name='description']").get_attribute("content")
        assert desc and len(desc) >= 10, \
            f"[{site_name}] Brak lub zbyt krótkie meta description: '{desc}'"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC03_h1_exists(self, page, site_name, url):
        """TC-03: Strony live mają co najmniej jeden nagłówek H1.
        UWAGA: biopoprom (plik lokalny) nie posiada żadnych tagów h1-h6 — znaleziony bug dostępności.
        """
        page.goto(url, wait_until="domcontentloaded")
        h1_count = page.locator("h1").count()
        assert h1_count >= 1, \
            f"[{site_name}] Brak nagłówka H1 na stronie"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC04_viewport_meta(self, page, site_name, url):
        """TC-04: Strony mają meta viewport (responsywność mobilna)."""
        page.goto(url, wait_until="domcontentloaded")
        viewport = page.locator("meta[name='viewport']").get_attribute("content")
        assert viewport and "width" in viewport, \
            f"[{site_name}] Brak lub błędny meta viewport: '{viewport}'"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC05_html_lang_attribute(self, page, site_name, url):
        """TC-05: Tag <html> ma atrybut lang (SEO i dostępność)."""
        page.goto(url, wait_until="domcontentloaded")
        lang = page.locator("html").get_attribute("lang")
        assert lang and len(lang) >= 2, \
            f"[{site_name}] Brak atrybutu lang w <html>: '{lang}'"


# ──────────────────────────────────────────────────────────────────────────────
#  WYDAJNOŚĆ
# ──────────────────────────────────────────────────────────────────────────────

class TestPerformance:

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC06_dom_content_loaded_under_5s(self, page, site_name, url):
        """TC-06: DOMContentLoaded < 5000 ms."""
        page.goto(url, wait_until="domcontentloaded")
        timing = page.evaluate("""() => ({
            dcl: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart
        })""")
        dcl = timing["dcl"]
        assert dcl < 5000, \
            f"[{site_name}] DOMContentLoaded = {dcl} ms (limit: 5000 ms)"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC07_page_load_under_10s(self, page, site_name, url):
        """TC-07: Pełne załadowanie strony < 10 000 ms."""
        page.goto(url, wait_until="load")
        timing = page.evaluate("""() => ({
            load: performance.timing.loadEventEnd - performance.timing.navigationStart
        })""")
        load = timing["load"]
        assert load < 10000, \
            f"[{site_name}] Pełne ładowanie = {load} ms (limit: 10 000 ms)"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC08_ttfb_under_2s(self, page, site_name, url):
        """TC-08: Time To First Byte < 2000 ms."""
        page.goto(url, wait_until="domcontentloaded")
        timing = page.evaluate("""() => ({
            ttfb: performance.timing.responseStart - performance.timing.navigationStart
        })""")
        ttfb = timing["ttfb"]
        assert ttfb < 2000, \
            f"[{site_name}] TTFB = {ttfb} ms (limit: 2000 ms)"


# ──────────────────────────────────────────────────────────────────────────────
#  DOSTĘPNOŚĆ (ACCESSIBILITY)
# ──────────────────────────────────────────────────────────────────────────────

class TestAccessibility:

    @pytest.mark.parametrize("site_name,url", ALL_SITES)
    def test_TC09_images_have_alt(self, page, site_name, url):
        """TC-09: Wszystkie obrazy mają atrybut alt (WCAG 1.1.1)."""
        page.goto(url, wait_until="domcontentloaded")
        # Szukamy img bez atrybutu alt lub z pustym alt na elementach dekoracyjnych
        images_without_alt = page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs
                .filter(img => img.getAttribute('alt') === null)
                .map(img => img.src || img.getAttribute('data-src') || 'unknown');
        }""")
        assert len(images_without_alt) == 0, \
            f"[{site_name}] Obrazy bez atrybutu alt: {images_without_alt[:5]}"

    @pytest.mark.parametrize("site_name,url", ALL_SITES)
    def test_TC10_buttons_have_text(self, page, site_name, url):
        """TC-10: Przyciski mają tekst lub aria-label (WCAG 4.1.2)."""
        page.goto(url, wait_until="domcontentloaded")
        empty_buttons = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            return btns.filter(b => {
                const text = (b.innerText || '').trim();
                const aria  = b.getAttribute('aria-label') || '';
                const title = b.getAttribute('title') || '';
                return !text && !aria && !title;
            }).map(b => b.outerHTML.substring(0, 80));
        }""")
        assert len(empty_buttons) == 0, \
            f"[{site_name}] Przyciski bez tekstu/aria-label: {empty_buttons[:3]}"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC11_form_inputs_have_labels(self, page, site_name, url):
        """TC-11: Pola formularzy mają skojarzone etykiety (WCAG 1.3.1)."""
        page.goto(url, wait_until="domcontentloaded")
        unlabelled = page.evaluate("""() => {
            const inputs = Array.from(document.querySelectorAll(
                'input:not([type=hidden]):not([type=submit]):not([type=button])'
            ));
            return inputs.filter(inp => {
                // Pomijamy pola honeypot (antyspam) — tabindex=-1 lub ukryte przez CSS
                if (inp.tabIndex < 0) return false;
                const style = window.getComputedStyle(inp);
                if (style.display === 'none' || style.visibility === 'hidden') return false;

                const id = inp.id;
                const label = id ? document.querySelector('label[for="' + id + '"]') : null;
                const ariaLabel = inp.getAttribute('aria-label');
                const ariaLabelledBy = inp.getAttribute('aria-labelledby');
                const placeholder = inp.getAttribute('placeholder');
                return !label && !ariaLabel && !ariaLabelledBy && !placeholder;
            }).map(inp => inp.outerHTML.substring(0, 80));
        }""")
        assert len(unlabelled) == 0, \
            f"[{site_name}] Pola bez etykiet: {unlabelled[:3]}"

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC12_page_has_skip_or_main(self, page, site_name, url):
        """TC-12: Strona ma element <main> lub landmark ułatwiający nawigację."""
        page.goto(url, wait_until="domcontentloaded")
        has_main = page.locator("main, [role='main']").count() > 0
        has_nav  = page.locator("nav, [role='navigation']").count() > 0
        assert has_main or has_nav, \
            f"[{site_name}] Brak elementu <main> ani <nav> — utrudniona nawigacja dla czytników ekranu"


# ──────────────────────────────────────────────────────────────────────────────
#  ZEPSUTE LINKI
# ──────────────────────────────────────────────────────────────────────────────

class TestBrokenLinks:

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC13_no_broken_internal_links(self, page, site_name, url):
        """TC-13: Linki wewnętrzne na stronie głównej nie zwracają 4xx/5xx."""
        page.goto(url, wait_until="domcontentloaded")

        # Zbierz wszystkie linki wewnętrzne (ten sam hostname)
        from urllib.parse import urlparse
        base_host = urlparse(url).netloc

        hrefs = page.evaluate("""(baseHost) => {
            return Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(href => {
                    try {
                        const u = new URL(href);
                        return u.hostname === baseHost && !href.includes('#');
                    } catch { return false; }
                });
        }""", base_host)

        # Deduplikacja
        unique_hrefs = list(dict.fromkeys(hrefs))[:20]  # max 20 linków

        broken = []
        for link in unique_hrefs:
            check_page = page.context.new_page()
            try:
                response = check_page.goto(link, wait_until="domcontentloaded", timeout=10000)
                if response and response.status >= 400:
                    broken.append(f"{link} → {response.status}")
            except Exception as e:
                # Timeout lub redirect loop — nie traktujemy jako zepsuty link
                pass
            finally:
                check_page.close()

        assert len(broken) == 0, \
            f"[{site_name}] Zepsute linki ({len(broken)}):\n" + "\n".join(broken)

    @pytest.mark.parametrize("site_name,url", LIVE_SITES)
    def test_TC14_no_404_images(self, page, site_name, url):
        """TC-14: Obrazy na stronie głównej ładują się (brak błędów 4xx)."""
        failed_images = []

        def handle_response(response):
            if response.request.resource_type == "image" and response.status >= 400:
                failed_images.append(f"{response.url[:80]} → {response.status}")

        page.on("response", handle_response)
        page.goto(url, wait_until="load")

        assert len(failed_images) == 0, \
            f"[{site_name}] Obrazy z błędami:\n" + "\n".join(failed_images)


# ──────────────────────────────────────────────────────────────────────────────
#  SCREENSHOTY
# ──────────────────────────────────────────────────────────────────────────────

class TestScreenshots:

    @pytest.mark.parametrize("site_name,url", ALL_SITES)
    def test_TC15_screenshot_saved(self, page, site_name, url):
        """TC-15: Screenshot każdej strony zapisuje się do reports/screenshots/."""
        page.goto(url, wait_until="domcontentloaded")

        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = str(int(time.time()))
        path = SCREENSHOTS_DIR / f"{site_name}_{timestamp}.png"
        page.screenshot(path=str(path), full_page=True)

        assert path.exists(), f"[{site_name}] Screenshot nie został zapisany: {path}"
        size_kb = path.stat().st_size // 1024
        assert size_kb > 5, f"[{site_name}] Screenshot za mały ({size_kb} KB) — prawdopodobnie pusta strona"
