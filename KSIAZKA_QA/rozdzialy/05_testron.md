# Rozdział 5 — Testowanie platformy SaaS w budowie
## `www.TESTron.pl`

---

### Szczere słowo wstępu

Ten rozdział jest inny od pozostałych. Nie ma w nim raportu "17/17 PASSED". Nie ma screenshotów z testów. Jest za to coś równie wartościowego z punktu widzenia testerskiego: **plan testów dla systemu, który jeszcze nie istnieje**.

Umiejętność zaplanowania testów *przed* napisaniem kodu to cecha doświadczonego QA, nie juniora. Rekruterzy wiedzą, że nie każdy projekt jest gotowy do testowania. Widzą, jak kandydat myśli o testowaniu — i to jest ważniejsze niż liczba "PASSED".

---

### Czym jest TESTron

TESTron to platforma SaaS do monitorowania i testowania stron internetowych z wbudowanym asystentem AI. Projekt budowany jest od podstaw — pomysł, architektura i schemat bazy danych zostały zaprojektowane, ale implementacja jest w toku.

**Wyróżnik produktu:** łączy trzy kategorie narzędzi w jedno:

| Kategoria | Istniejące narzędzia | Co TESTron robi inaczej |
|---|---|---|
| Monitoring uptime | UptimeRobot, Better Stack | ✅ (ale to tylko fundament) |
| Testy syntetyczne | Checkly, Datadog Synthetics | ✅ Playwright workers |
| Audytory jakości | Lighthouse, Screaming Frog | ✅ zintegrowane w jednym dashboardzie |
| **Raport AI** | — | ✅ **Claude generuje narrację w języku polskim** |

Zamiast trzech osobnych narzędzi i trzech tabeli z cyframi — użytkownik dostaje jeden raport napisany po polsku, z konkretnymi krokami napraw.

---

### Stack technologiczny

```
Backend:   Fastify (Node.js/TypeScript) + Drizzle ORM
Frontend:  Next.js (TypeScript)
Baza:      PostgreSQL (schema Drizzle)
Kolejka:   Redis
Workers:   Node.js — testy BASIC (uptime, SSL, linki, formularz)
           Playwright — testy PRO (Lighthouse, axe-core, a11y)
AI:        Claude API (Anthropic) — generowanie raportów
Hosting:   Cloudflare Workers / R2 (artefakty)
```

---

### Schemat bazy danych — co już istnieje

Schemat bazy (`drizzle/schema.ts`) jest zaprojektowany i gotowy. Widać w nim architekturę całego systemu:

```typescript
// Cztery główne tabele:

users       — użytkownicy platformy (plan: free | basic | pro | agency)
sites       — monitorowane strony (tier: 'basic' | 'pro')
test_runs   — wyniki testów (status: pending | running | completed | failed)
incidents   — wykryte awarie i problemy (severity: critical | warning | info)
```

Każdy `test_run` przechowuje:
- `raw_json` — surowe wyniki (JSON z Lighthouse, axe-core, własne sondy)
- `artifact_url` — link do pełnego raportu HTML w Cloudflare R2
- `score_perf`, `score_a11y`, `score_seo` — wyniki Lighthouse 0–100
- `ai_report` — narracja wygenerowana przez Claude

Schemat bazy danych to specyfikacja systemu zapisana w kodzie. Czytając go, widzę co system będzie robił — bez potrzeby uruchamiania aplikacji.

---

### Plan testów — co będę testował gdy aplikacja będzie gotowa

#### Warstwa 1: Testy API (backend)

Backend TESTrona to REST API w Fastify. Testy API to moja priorytetowa warstwa — szybkie, niezależne od UI, łatwe do utrzymania.

```python
# Przykładowy test rejestracji użytkownika (plan):
def test_register_user():
    response = requests.post(f"{API_URL}/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["plan_id"] == "free"       # nowy użytkownik = free plan
    assert "password" not in data          # hasło NIE wraca w odpowiedzi!
```

**Planowane przypadki testowe — API:**

| Endpoint | TC | Scenariusz |
|---|---|---|
| `POST /auth/register` | TC-01 | Rejestracja z poprawnymi danymi → 201 + token |
| `POST /auth/register` | TC-02 | Duplikowany email → 409 Conflict |
| `POST /auth/login` | TC-03 | Poprawne dane → 200 + JWT |
| `POST /auth/login` | TC-04 | Błędne hasło → 401 Unauthorized |
| `POST /sites` | TC-05 | Dodanie strony (auth required) → 201 |
| `POST /sites` | TC-06 | Brak tokenu → 401 |
| `POST /sites/{id}/run` | TC-07 | Uruchomienie testu → status pending |
| `GET /sites/{id}/runs` | TC-08 | Lista wyników testów → tablica JSON |
| `GET /incidents` | TC-09 | Lista incydentów → filtrowanie po severity |

---

#### Warstwa 2: Testy UI (Next.js dashboard)

Dashboard to aplikacja Next.js — SPA z wieloma stanami (niezalogowany, zalogowany, pusty stan, pełny stan). Playwright idealnie nadaje się do testów E2E tego dashboardu.

```python
# Przykładowy test dodania strony do monitoringu (plan):
def test_add_site_to_monitoring(logged_in_page):
    dash = TESTronDashboard(logged_in_page)
    dash.click_add_site()
    dash.fill_site_url("https://www.dbcraftmode.pl")
    dash.select_tier("basic")
    dash.save()

    assert dash.site_visible_in_list("dbcraftmode.pl"), \
           "Dodana strona powinna pojawić się na liście"
```

**Planowane klasy Page Object:**

```python
class TESTronLoginPage(BasePage): ...
class TESTronDashboard(BasePage): ...
class TESTronSiteDetail(BasePage): ...
class TESTronTestReport(BasePage): ...
```

---

#### Warstwa 3: Testy workerów (jednostkowe)

Workers to moduły Node.js które wykonują faktyczne testy stron. Każdy worker można testować niezależnie — nie potrzeba uruchomionego frontendu ani backendu.

```typescript
// Przykładowy test workera uptime (plan — TypeScript + Jest/Vitest):
describe("UptimeWorker", () => {
    it("powinien zwrócić status 200 dla działającej strony", async () => {
        const result = await checkUptime("https://www.dbcraftmode.pl");
        expect(result.status).toBe(200);
        expect(result.responseTimeMs).toBeLessThan(5000);
    });

    it("powinien zgłosić błąd dla nieistniejącej domeny", async () => {
        const result = await checkUptime("https://ta-strona-nie-istnieje-xyz.pl");
        expect(result.status).toBe(null);
        expect(result.error).toBeTruthy();
    });
});
```

---

#### Warstwa 4: Testy integracji AI

To najtrudniejsza warstwa do przetestowania. Claude generuje raporty na podstawie danych testowych — jak sprawdzić jakość tekstu automatycznie?

**Podejście:**
- Nie testujemy jakości narracji (to subiektywne)
- Testujemy **strukturę i kompletność** odpowiedzi:

```python
def test_ai_report_structure(test_run_data):
    report = claude_client.generate_report(test_run_data)
    assert isinstance(report, str)
    assert len(report) > 100          # raport nie jest pusty
    assert "score" in report.lower() or "wynik" in report.lower()
    # Structured Outputs — jeśli zwracamy JSON:
    report_json = json.loads(report)
    assert "summary" in report_json
    assert "recommendations" in report_json
    assert isinstance(report_json["recommendations"], list)
```

---

### Dlaczego testy pisać równolegle z kodem

TESTron jest w fazie 0. Mógłbym poczekać aż aplikacja będzie "gotowa" i dopiero wtedy pisać testy. Ale to błędne podejście.

**Właściwa kolejność:**
1. Schemat bazy → testy schematu (typy, constrainty, relacje)
2. Endpoint API → test jednostkowy tego endpointu
3. Komponent UI → test E2E tego komponentu
4. Worker → test jednostkowy workera

Takie podejście nazywa się **Test-Driven Development (TDD)** w wersji uproszczonej. Nie muszę pisać testów PRZED kodem, ale powinienem pisać je RAZEM z kodem — nie tygodnie po deploymencie.

---

### Status projektu i co dalej

| Element | Status |
|---|---|
| Specyfikacja produktu | ✅ Gotowa |
| Schemat bazy danych | ✅ Gotowy (Drizzle + PostgreSQL / Supabase) |
| Konfiguracja środowiska | ✅ Supabase + Upstash (bez Dockera na dev) |
| Backend (Fastify API) | ✅ MVP — `/health`, CRUD stron, test inline |
| Panel testowy | ✅ `http://localhost:3000/panel` |
| Workers (BASIC) | 🔨 Kolejka Upstash (wymaga poprawnego REDIS_URL) |
| Pierwszy test produkcyjny | ✅ dbcraftmode.pl → **HTTP 200** |
| Frontend (Next.js) | 🔨 W planowaniu |
| Testy Playwright w automation | ⏳ `automation/tests/testron/` |
| Wdrożenie online testron.pl | ⏳ Po MVP |

**Sesja 2026-05-21:** Uruchomiono API lokalnie; naprawiono test HTTP na starszym Windows (mechanizm jak PowerShell). Zob. `notatki/dziennik_2026.md`.

---

### Nowe umiejętności zaplanowane w tej fazie

| Umiejętność | Gdzie użyta |
|---|---|
| Testowanie REST API (requests/httpx) | Testy backendu Fastify |
| Testowanie SPA (Next.js) przez Playwright | Testy dashboardu |
| Testy jednostkowe Node.js (Vitest/Jest) | Testy workerów |
| Weryfikacja structured outputs Claude | Testy jakości raportów AI |
| Testowanie JWT auth w API | TC-06 brak tokenu → 401 |
| TDD — testy równolegle z kodem | Cały projekt TESTron |

---

*Faza 5 — w trakcie realizacji. Rozdział zostanie uzupełniony o wyniki testów gdy MVP TESTrona będzie gotowe.*
