# PLAN PROJEKTU — Książka QA + Portfolio Automatyzacji
### Autor: Daniel Bryjak | Data startu: 2026-05-19

---

## Proponowane tytuły książki (wybierz jeden)

| # | Tytuł | Klimat |
|---|-------|--------|
| A | **"Tester 360° — Od Kliknięcia do Kodu"** | Profesjonalny, nowoczesny |
| B | **"QA w Akcji — Testowanie na Żywych Projektach"** | Praktyczny, do CV |
| C | **"Nie klikam, testuję — Przewodnik Junior QA"** | Osobisty, wyróżniający się |
| D | **"Moje Strony, Moje Testy — Od Zera do Automatyzacji"** | Autobiograficzny, szczery |

> Rekomendacja: **"Tester 360° — Od Kliknięcia do Kodu"**
> Brzmi profesjonalnie, pokazuje pełne spektrum (manual + auto) i jest chwytliwy.

---

## Struktura folderów całego projektu

```
d:\Projekt SDA\
├── automation\              ← KOD TESTÓW (już istnieje)
│   ├── pages\
│   ├── tests\
│   │   ├── store\           ← FAZA 1 (gotowe)
│   │   ├── biopoprom\       ← FAZA 2
│   │   ├── koparka\         ← FAZA 3
│   │   ├── dbcraftmode\     ← FAZA 4
│   │   └── testron\         ← FAZA 5
│   └── reports\
└── KSIAZKA_QA\              ← KSIĄŻKA (tu jesteś)
    ├── PLAN_PROJEKTU.md     ← ten plik
    ├── ksiazka.md           ← główny dokument książki
    └── rozdzialy\           ← rozdziały osobno
        ├── 00_wstep.md
        ├── 01_sklep.md
        ├── 02_biopoprom.md
        ├── 03_koparka.md
        ├── 04_dbcraftmode.md
        ├── 05_testron.md
        ├── 06_testy_przekrojowe.md
        ├── 07_podsumowanie.md
        ├── 08_jak_uruchomic.md
        └── 09_droga_trzech_etapow.md
    ├── notatki\
    │   ├── dziennik_2026.md
    │   └── README.md
    ├── skrypty\
    │   └── dodaj-notatke.ps1
    └── STRESZCZENIE_LIST_MOTYWACYJNY.md
```

---

# PLAN CHRONOLOGICZNY

---

## FAZA 0 — Fundament ✅ (częściowo gotowe)

**Cel:** Przygotowanie środowiska i struktury projektu

- [x] 0.1 Struktura folderów `automation/`
- [x] 0.2 Konfiguracja Pytest + Playwright (`conftest.py`, `pytest.ini`)
- [x] 0.3 Page Object Model — klasy bazowe
- [x] 0.4 Testy logowania dla sklepu (TC-01, TC-02, TC-03)
- [x] 0.5 Instalacja i pierwsze uruchomienie (weryfikacja że działa)
- [ ] 0.6 Ustalenie tytułu książki
- [x] 0.7 Stworzenie szablonu książki (`ksiazka.md`)
- [x] 0.8 Napisanie Rozdziału 0 — Wstęp autobiograficzny

**Efekt:** Działające środowisko + pierwsze 3 testy + otwarty dokument książki

---

## FAZA 1 — Sklep internetowy `yabko-com.e-kei.pl/2/`

**Cel:** Pełne pokrycie testami formularza logowania + nawigacja sklepu

- [x] 1.1 Uruchomienie i weryfikacja istniejących testów (TC-01..TC-04)
- [x] 1.2 Zamiana yabko (offline) na saucedemo.com
- [x] 1.3 TC-01 błędne hasło, TC-02 poprawne logowanie, TC-03 zablokowane konto, TC-04 puste pola
- [x] 1.4 Raport HTML z testów Fazy 1 — 4/4 PASSED
- [x] 1.5 Napisanie Rozdziału 1 książki

**Nowe umiejętności w rozdziale:** Selenium IDE → Playwright, POM, asercje

---

## FAZA 2 — `www.biopoprom.pl`

**Cel:** Testy smoke i UI dla strony wizytówkowej

- [x] 2.1 Analiza strony biopoprom.html — SPA z 4 zakładkami
- [x] 2.2 TC-01 smoke: tytuł "BIOPOPROM"
- [x] 2.3 TC-02 smoke: zegar i czas BP widoczne
- [x] 2.4 TC-03 smoke: 4 zakładki nawigacji
- [x] 2.5 TC-04 nawigacja: przełączanie między zakładkami
- [x] 2.6 TC-05 zegar: format HH:MM:SS, czas zainicjowany
- [x] 2.7 TC-06 zegar: faza księżyca wyświetlona
- [x] 2.8 TC-07 kalendarz: siatka z min. 28 komórkami
- [x] 2.9 TC-08 kalendarz: nawigacja poprzedni/następny miesiąc
- [x] 2.10 TC-09 kalkulator STD→BP
- [x] 2.11 TC-10 kalkulator BP→STD
- [x] 2.12 TC-11 kalkulator złotego podziału
- [x] 2.13 TC-12 przyciski Hz
- [x] 2.14 Raport HTML z testów Fazy 2 — 12/12 PASSED
- [ ] 2.15 Napisanie Rozdziału 2 książki

**Nowe umiejętności w rozdziale:** Testy smoke, testy UI, responsywność, broken images

---

## FAZA 3 — `www.koparka-kobierzyce.pl`

**Cel:** Testowanie złożonej strony firmowej z blogiem i CRM

- [x] 3.1 Analiza strony — mapa podstron (index, blog, CRM, kalkulator, analiza-dzialki)
- [x] 3.2 TC-01..03 Smoke: tytuł, logo KK, hero visible
- [x] 3.3 TC-04..05 Nawigacja: linki menu, klik Blog → /blog/
- [x] 3.4 TC-06..07 Sekcje: oferta/wykopy/realizacje/kontakt w DOM, stopka
- [x] 3.5 TC-08..10 Formularz: pola, przycisk, opcje usług
- [x] 3.6 TC-11..13 Blog: ładowanie, min. 1 artykuł, wejście w artykuł
- [x] 3.7 TC-14..16 CRM: strona logowania, błędne hasło, poprawne hasło + logout
- [x] 3.8 Raport HTML z testów Fazy 3 — **16/16 PASSED**
- [x] 3.9 Napisanie Rozdziału 3 książki

**Nowe umiejętności w rozdziale:** Testowanie CRM, formularze wieloetapowe, blog

---

## FAZA 4 — `www.dbcraftmode.pl` ✅

**Cel:** Testowanie PHP CMS z panelem admina — pełny CRUD

- [x] 4.1 Analiza panelu admina — mapa funkcji
- [x] 4.2 Test: logowanie do panelu admina (poprawne / błędne)
- [x] 4.3 Test: wylogowanie / TC-06 poprawne dane → dashboard
- [x] 4.4 Test: dashboard — sidebar widoczny, linki do Blog/Pomysły/Projekty
- [x] 4.5 Test Blog — lista wpisów ładuje się
- [x] 4.6 Test Blog — formularz dodawania z polami
- [x] 4.7 Test Blog — walidacja pustego tytułu + dodanie szkicu
- [x] 4.8 Test Pomysły — lista i formularz
- [x] 4.9 Test Pomysły — dodanie nowego pomysłu → pojawia się na liście
- [x] 4.10 Test Projekty — lista ładuje się
- [x] 4.11 Test Projekty — lista ma co najmniej 1 projekt
- [x] 4.13 Raport HTML z testów Fazy 4 — **17/17 PASSED**
- [x] 4.14 Napisanie Rozdziału 4 książki

**Nowe umiejętności w rozdziale:** CRUD testing, panel admina, CSRF, bcrypt, debug sesji

*Faza 4 ukończona: 2026-05-20 | Wynik: 17/17 PASSED*

---

## FAZA 5 — `www.TESTron.pl` 🔨

**Cel:** Testowanie aplikacji full-stack (gdy będzie dostępna online/lokalnie)

- [x] 5.0 MVP backend: API + panel + Supabase (bez Dockera) — 2026-05-21
- [x] 5.0b Pierwszy uptime test: dbcraftmode.pl HTTP 200
- [ ] 5.1 Uruchomienie aplikacji lokalnie (Docker lub npm) — **npm + Supabase zamiast Docker**
- [ ] 5.2 Analiza funkcji frontendu
- [ ] 5.3 Testy UI frontendu (Next.js dashboard)
- [ ] 5.4 Testy API (Fastify backend)
- [ ] 5.5 Testy workerów (Node.js — uptime, SSL, linki)
- [ ] 5.6 Raport HTML z testów Fazy 5
- [x] 5.7 Napisanie Rozdziału 5 książki — plan testów + architektura

**Nowe umiejętności w rozdziale:** API testing, SPA testing, TDD, testowanie wyników AI

*Status: aplikacja w toku — testy zostaną napisane gdy MVP będzie gotowe*

---

## FAZA 6 — Testy Przekrojowe (wszystkie strony) ✅

**Cel:** Zaawansowane techniki testowania ponad konkretną aplikację

- [x] 6.1 Skaner zepsutych linków — koparka + dbcraftmode (TC-13..14)
- [x] 6.2 Testy wydajności — TTFB, DOMContentLoaded, Load (TC-06..08)
- [x] 6.3 Testy SEO — tytuł, meta description, H1, viewport, lang (TC-01..05)
- [x] 6.4 Testy dostępności — alt teksty, przyciski, labele, landmark (TC-09..12)
- [x] 6.6 Screenshoty full-page każdej strony (TC-15)
- [x] 6.7 Raport HTML — 34/34 PASSED
- [x] 6.8 Napisanie Rozdziału 6 książki
- [x] Bug znaleziony: biopoprom.html brak h1-h6 (WCAG 1.3.1)

**Nowe umiejętności:** parametrize, performance.timing, page.evaluate JS, a11y, screenshoty

*Faza 6 ukończona: 2026-05-21 | Wynik: 34/34 PASSED*

---

## FAZA 7 — Finalizacja Książki ✅

**Cel:** Gotowy dokument portfolio

- [x] 7.1 Napisanie Rozdziału 0 — Wstęp
- [x] 7.2 Napisanie Rozdziału 7 — Podsumowanie umiejętności (83 testy, tabela)
- [x] 7.3 Napisanie Rozdziału 8 — Jak uruchomić projekt
- [x] 7.5 Złożenie wszystkich rozdziałów w `ksiazka.md` (spis treści)
- [x] KPK — Kompletny Przewodnik Kariery (osobny dokument)

*Faza 7 ukończona: 2026-05-21*

---

## FAZA 8 — Strona Portfolio

**Cel:** Nowa strona prezentująca Ciebie jako QA Engineer

- [ ] 8.1 Projekt wizualny strony
- [ ] 8.2 Sekcja "O mnie" — historia, certyfikat SDA
- [ ] 8.3 Sekcja "Moje projekty testowe" — każda strona osobno
- [ ] 8.4 Sekcja "Umiejętności" — lista technologii i narzędzi
- [ ] 8.5 Sekcja "Live raporty" — link do aktualnych raportów HTML
- [ ] 8.6 Integracja z GitHub (link do repozytorium z testami)
- [ ] 8.7 Wdrożenie strony

---

## Podsumowanie — co zdobędziesz po ukończeniu

| Umiejętność | Dowód w projekcie |
|---|---|
| Testy manualne | Rozdziały 1-4, TestRail screenshots |
| Selenium IDE | Plik `my store.side` |
| Playwright + Python | Folder `automation/` na GitHub |
| Page Object Model | Klasy w `automation/pages/` |
| Pytest + raporty HTML | Folder `automation/reports/` |
| CRUD testing | Faza 4 — dbcraftmode admin |
| API testing | Faza 5 — TESTron |
| Accessibility testing | Faza 6 |
| Cross-browser testing | Faza 6 |
| Dokumentacja | Książka + README |
| Portfolio online | Strona z Fazy 8 |

---

*Plan stworzony: 2026-05-19 | Aktualizuj ten plik przy każdej zmianie zakresu.*
