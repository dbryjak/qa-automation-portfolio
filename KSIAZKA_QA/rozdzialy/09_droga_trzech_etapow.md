# Rozdział 9 — Od kliknięcia do platformy SaaS
## Manual → Automatyzacja → TESTron (dla siebie i klientów)

---

### Jedna historia, trzy etapy

| Etap | Co robiłem | Gdzie to widać |
|------|------------|----------------|
| **1. Manual** | Kurs SDA, TestRail, Jira, przypadki testowe, „czy formularz działa?” | Certyfikat, notatki z kursu, świadome testowanie własnych stron |
| **2. Automatyzacja** | Python + Pytest + Playwright, POM, raporty HTML | `d:\Projekt SDA\automation\` — **83 testy**, 4 strony produkcyjne |
| **3. Platforma** | TESTron — monitoring i testy stron w jednym miejscu + AI (plan) | `D:\STRONY_WWW\www.TESTron.pl` — API, panel, Supabase |

To **nie są trzy osobne hobby**. To jedna ścieżka: od „sprawdzam ręcznie” do „system sprawdza za mnie i za klienta”.

---

### Etap 1 — Testowanie manualne (fundament)

Zanim napisałem linijkę kodu testowego, nauczyłem się:
- typów testów (smoke, regresja, exploratory),
- pisania przypadków testowych,
- raportowania bugów,
- pracy w TestRail i Jira.

**Na moich stronach** robiłem to intuicyjnie: czy menu działa, czy admin się loguje, czy wpis bloga się zapisuje. Kurs nadał temu **nazwy i proces**.

---

### Etap 2 — Automatyzacja (dowód dla rekrutera)

Gdy powtarzalne scenariusze zżerały czas, przeniosłem je do kodu:

```
saucedemo.com     →  4 testy   (logowanie, POM)
biopoprom.pl      → 12 testów  (SPA, smoke)
koparka-kobierzyce.pl → 16 testów (CRM, blog, formularz)
dbcraftmode.pl    → 17 testów  (CRUD, panel admina)
cross-site        → 34 testy   (SEO, wydajność, a11y)
────────────────────────────────────────────
RAZEM             → 83 testy, 0 failed
```

Ta sama strona **dbcraftmode.pl**, którą wcześniej „klikałem”, dziś jest pokryta testami E2E — to most między etapem 1 a 2.

---

### Etap 3 — TESTron (produkt zawodowy)

TESTron to krok dalej: zamiast uruchamiać testy **ręcznie z linii poleceń** dla każdej strony, buduję **serwis**, w którym:

1. **Ja** dodaję swoje strony (np. dbcraftmode.pl).
2. **Klient** (w przyszłości) dodaje swoje domeny.
3. System **regularnie** sprawdza uptime (później: SSL, linki, Lighthouse, raport AI).
4. Wyniki są w **bazie** (Supabase) i w **panelu** — nie tylko w pliku HTML z pytest.

**Stan na 2026-05-21 (Faza 0):**
- ✅ Schemat bazy (users, sites, test_runs, incidents)
- ✅ API Fastify + panel `/panel`
- ✅ Supabase + Upstash zamiast Dockera
- ✅ Pierwszy test uptime: **HTTP 200** dla dbcraftmode.pl
- ⏳ Kolejka Redis (Upstash — do poprawy URL)
- ⏳ Frontend Next.js, auth, testy Playwright w `automation/tests/testron/`

---

### Dlaczego to ma sens w CV i na rozmowie

> *„Nie uczę się QA na sucho — testuję własne produkcyjne projekty. Najpierw manualnie i na kursie, potem 83 automatyczne testy Playwright, a teraz buduję platformę SaaS, która ma te same kontrole oferować klientom.”*

To pokazuje:
- **myślenie procesowe** (SDA),
- **umiejętność automatyzacji** (portfolio),
- **myślenie produktowe** (TESTron — nie tylko skrypty).

---

### Notatki dzienne

Postęp tego etapu zapisuję w `notatki/dziennik_2026.md` (skrypt `skrypty/dodaj-notatke.ps1`).

---

*Rozdział 9 — żywy dokument; uzupełniany wraz z rozwojem TESTron.*
