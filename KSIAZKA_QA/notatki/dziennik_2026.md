# Dziennik pracy QA — 2026

Automatycznie dopisywany przez `dodaj-notatke.ps1`.

## 2026-05-21 20:35 — TESTron: pierwszy działający test produkcyjny

**Projekt / faza:** TESTron Faza 0 (www.TESTron.pl — scaffold SaaS)

**Co zrobiłem:**
- Uruchomienie API bez Dockera (Supabase + Upstash w `.env`).
- Panel testowy `http://localhost:3000/panel` — dodawanie stron, test uptime.
- Naprawa testu HTTP na starszym Windows (mechanizm jak PowerShell).
- Potwierdzenie **HTTP 200** dla `https://www.dbcraftmode.pl/`.

**Manual → Auto → Platforma:** Ręczne „klikanie” stron przerodziło się w 83 testy Playwright; dziś buduję **platformę**, która ma te same kontrole robić automatycznie dla moich stron i przyszłych klientów.

**Wynik / liczby:** dbcraftmode.pl — HTTP 200 w panelu TESTron; wcześniej 83/83 PASSED w automation.

**Problem / nauka:** Node `fetch` dawał HTTP 0 mimo że strona działa — rozwiązanie: test przez wbudowany https / PowerShell.

**Jutro:** Upstash (poprawny REDIS_URL), kolejne kroki TESTron lub notatka po sesji.

---

## 2026-05-22 — (szablon na dziś)

**Projekt / faza:**

**Co zrobiłem:**
-

**Manual → Auto → Platforma:**

**Wynik / liczby:**

---
