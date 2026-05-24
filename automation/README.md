# QA Automation Portfolio — Daniel Bryjak

**83 automated tests** | Python 3.14 · Pytest 9.0 · Playwright 1.60 | **5 live projects** | 0 failed

> Built as part of completing the SDA "Tester Oprogramowania" certification course.
> All tests run against real, live websites — not mocks or sandboxes.

---

## Projects Tested

| Site | Type | Tests | Status |
|------|------|-------|--------|
| [saucedemo.com](https://www.saucedemo.com) | E-commerce demo | 4 | ✅ PASSED |
| [biopoprom.pl](https://www.biopoprom.pl) | SPA (Single Page App) | 12 | ✅ PASSED |
| [koparka-kobierzyce.pl](https://koparka-kobierzyce.pl) | Client site + CRM | 16 | ✅ PASSED |
| [dbcraftmode.pl](https://www.dbcraftmode.pl) | PHP CMS + admin panel | 17 | ✅ PASSED |
| Cross-site (SEO / A11y / Performance) | All sites combined | 34 | ✅ PASSED |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/dbryjak/qa-automation-portfolio.git
cd qa-automation-portfolio/automation

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Run all tests
pytest tests/ --html=reports/report.html --self-contained-html -v

# 5. Open report
start reports/report.html   # Windows
# open reports/report.html  # Mac
```

> Full step-by-step instructions (including troubleshooting) in [KSIAZKA_QA/rozdzialy/08_jak_uruchomic.md](KSIAZKA_QA/rozdzialy/08_jak_uruchomic.md)

---

## Project Structure

```
automation/
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # BasePage — shared methods
│   ├── login_page.py        # saucedemo.com login
│   ├── home_page.py         # saucedemo.com home
│   ├── biopoprom_page.py    # biopoprom.pl SPA
│   ├── koparka_page.py      # koparka-kobierzyce.pl
│   └── dbcraftmode_page.py  # dbcraftmode.pl admin panel
├── tests/
│   ├── store/               # Phase 1 — e-commerce login (4 tests)
│   ├── biopoprom/           # Phase 2 — SPA tabs, clock, calendar (12 tests)
│   ├── koparka/             # Phase 3 — CRM, contact form, blog (16 tests)
│   ├── dbcraftmode/         # Phase 4 — PHP admin CRUD (17 tests)
│   └── crosssite/           # Phase 6 — SEO, performance, a11y (34 tests)
├── reports/                 # HTML test reports + full-page screenshots
├── conftest.py              # Pytest fixtures (browser context, base URLs)
├── pytest.ini               # Pytest configuration
└── requirements.txt         # Dependencies
```

---

## Skills Demonstrated

| Category | Details |
|----------|---------|
| **Test design** | Black-box, boundary values, equivalence partitioning |
| **Page Object Model** | 6 page classes, BasePage inheritance |
| **CRUD testing** | Create/Read blog posts, ideas, projects in PHP admin |
| **Session testing** | Login/logout, cookie handling, auth state |
| **API awareness** | HTTP status codes, response monitoring via `page.on("response")` |
| **Accessibility (WCAG)** | Alt texts (1.1.1), headings (1.3.1), labels (4.1.2), landmarks |
| **Performance** | TTFB, DOMContentLoaded, Load via `performance.timing` JS API |
| **SEO** | Title, meta description, H1, viewport, lang attribute |
| **Broken link detection** | Internal links + image 4xx via browser context |
| **Cross-site parametrize** | `@pytest.mark.parametrize` across multiple sites |
| **Screenshots** | Full-page PNG via `page.screenshot(full_page=True)` |
| **Reporting** | pytest-html with self-contained HTML reports |

---

## Real Bug Found

During Phase 6 cross-site testing, an accessibility violation was discovered:

> **biopoprom.pl — missing heading structure (WCAG 1.3.1)**
> The page has no `<h1>`–`<h6>` tags. Screen readers cannot navigate content structure.
> Impact: accessibility + SEO. Severity: Medium.

---

## Documentation

Full project documentation in Polish in [`KSIAZKA_QA/`](KSIAZKA_QA/):

- [Rozdział 1 — saucedemo.com](KSIAZKA_QA/rozdzialy/01_sklep.md) — First tests, POM, environment setup
- [Rozdział 4 — dbcraftmode.pl](KSIAZKA_QA/rozdzialy/04_dbcraftmode.md) — CRUD, CSRF, debug of wrong admin email
- [Rozdział 6 — Cross-site tests](KSIAZKA_QA/rozdzialy/06_testy_przekrojowe.md) — SEO, A11y, Performance, broken links
- [Rozdział 7 — Summary](KSIAZKA_QA/rozdzialy/07_podsumowanie.md) — Competency table, 83 tests overview
- [KPK — Career Guide](KSIAZKA_QA/KPK_Kompletny_Przewodnik_Kariery.md) — Interview prep, CV template, salary ranges

---

## Tech Stack

```
Language:   Python 3.14
Framework:  Pytest 9.0.3
Browser:    Playwright 1.60 (pytest-playwright 0.8.0)
Reports:    pytest-html
Browser:    Chromium (headless)
OS tested:  Windows 10
```

---

*"Nie klikam — testuję."*

**Daniel Bryjak** · SDA Certified Tester
