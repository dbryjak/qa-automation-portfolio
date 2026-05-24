# Rozdział 8 — Jak Uruchomić Projekt
## Instrukcja dla Rekrutera i Współpracownika

---

### Wymagania wstępne

| Narzędzie | Wersja | Jak sprawdzić |
|---|---|---|
| Python | 3.10+ | `python --version` |
| pip | dowolna | `pip --version` |
| Git | dowolna | `git --version` |

System operacyjny: Windows 10/11, macOS, Linux (działa na wszystkich).

---

### Instalacja — krok po kroku

**1. Sklonuj repozytorium**
```bash
git clone https://github.com/danielbryjak/qa-portfolio.git
cd qa-portfolio/automation
```

**2. Utwórz wirtualne środowisko Python**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

**3. Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

**4. Pobierz przeglądarkę Chromium**
```bash
playwright install chromium
```

> **Uwaga dla Windows firmowych:** Jeśli pojawi się błąd SSL (`UNABLE_TO_VERIFY_LEAF_SIGNATURE`), uruchom:
> ```powershell
> $env:NODE_OPTIONS="--use-system-ca"
> venv\Scripts\playwright install chromium
> ```

---

### Uruchomienie testów

**Wszystkie testy — pełny raport HTML:**
```bash
pytest
```
Raport pojawi się w `reports/report.html` — otwórz w przeglądarce.

**Konkretna faza:**
```bash
pytest tests/store/           # Faza 1 — saucedemo.com
pytest tests/biopoprom/       # Faza 2 — biopoprom.pl
pytest tests/koparka/         # Faza 3 — koparka-kobierzyce.pl
pytest tests/dbcraftmode/     # Faza 4 — dbcraftmode.pl (wymaga internetu)
pytest tests/crosssite/       # Faza 6 — testy przekrojowe
```

**Tryb wizualny (widoczna przeglądarka):**
```bash
pytest --headed --slowmo=500
```

**Konkretny test:**
```bash
pytest tests/koparka/test_koparka.py::TestCRM::test_TC16_correct_login
```

---

### Struktura projektu

```
automation/
├── conftest.py              ← konfiguracja globalna (viewport, SSL)
├── pytest.ini               ← konfiguracja pytest (raport HTML, ścieżki)
├── requirements.txt         ← zależności Python
│
├── pages/                   ← Page Object Model — klasy stron
│   ├── base_page.py         ← BasePage (navigate, get_title)
│   ├── home_page.py         ← saucedemo — strona po zalogowaniu
│   ├── login_page.py        ← saucedemo — logowanie
│   ├── biopoprom_page.py    ← biopoprom.pl
│   ├── koparka_page.py      ← koparka-kobierzyce.pl
│   ├── dbcraftmode_page.py  ← dbcraftmode.pl (admin panel)
│   └── [testron_page.py]    ← TESTron (w budowie)
│
├── tests/                   ← przypadki testowe
│   ├── store/               ← Faza 1
│   ├── biopoprom/           ← Faza 2
│   ├── koparka/             ← Faza 3
│   ├── dbcraftmode/         ← Faza 4
│   └── crosssite/           ← Faza 6
│
└── reports/
    ├── report.html          ← raport HTML (generowany automatycznie)
    └── screenshots/         ← screenshoty stron (Faza 6)
```

---

### Co zobaczysz po uruchomieniu

Po `pytest` w terminalu:
```
============================= test session starts ==============================
collected 83 items

tests/store/test_login.py::TestLogin::test_TC01... PASSED
tests/store/test_login.py::TestLogin::test_TC02... PASSED
...
========================= 83 passed in 3m 42s ==================================
```

W `reports/report.html`:
- Lista wszystkich testów z czasem wykonania
- Metadata projektu (autor, framework)
- Screenshoty przy nieudanych testach (automatyczne)

---

### Częste problemy

| Problem | Przyczyna | Rozwiązanie |
|---|---|---|
| `ModuleNotFoundError: playwright` | Nie aktywowano venv | `venv\Scripts\activate` |
| `Error: Executable doesn't exist` | Nie pobrano przeglądarki | `playwright install chromium` |
| `SSL UNABLE_TO_VERIFY` | Firmowy proxy/antywirus | `$env:NODE_OPTIONS="--use-system-ca"` |
| Testy dbcraftmode FAIL | Brak internetu | Wymagane połączenie z siecią |
| Testy biopoprom FAIL | Plik lokalny nie istnieje | Sprawdź ścieżkę w `biopoprom_page.py` |

---

*Czas uruchomienia wszystkich 83 testów: ~3-4 minuty (zależy od połączenia internetowego)*
