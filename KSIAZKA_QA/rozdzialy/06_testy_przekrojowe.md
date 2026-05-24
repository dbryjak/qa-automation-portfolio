# Rozdział 6 — Testy Przekrojowe
## SEO, Wydajność, Dostępność, Zepsute Linki

---

### Co to są testy przekrojowe?

Poprzednie rozdziały testowały konkretne funkcje konkretnej strony — logowanie, formularz, blog. Testy przekrojowe działają inaczej: **ten sam zestaw testów uruchamiamy na każdej stronie z portfolio**.

To podejście ma kilka zalet:
- **Spójność** — każda strona spełnia te same standardy jakości
- **Efektywność** — piszemy test raz, uruchamiamy na N stronach
- **Wykrywanie wzorców** — widzimy które problemy powtarzają się na wielu stronach

---

### Technika: `@pytest.mark.parametrize`

Kluczowa technika tej fazy — parametryzacja testów:

```python
LIVE_SITES = [
    ("koparka",     "https://koparka-kobierzyce.pl"),
    ("dbcraftmode", "https://www.dbcraftmode.pl"),
]

@pytest.mark.parametrize("site_name,url", LIVE_SITES)
def test_TC01_title_not_empty(self, page, site_name, url):
    page.goto(url, wait_until="domcontentloaded")
    title = page.title()
    assert len(title) >= 5, f"[{site_name}] Tytuł za krótki: '{title}'"
```

Zamiast dwóch osobnych testów dla dwóch stron — jeden test, dwa uruchomienia. Pytest automatycznie generuje nazwy przypadków:
```
test_TC01_title_not_empty[chromium-koparka-https://koparka-kobierzyce.pl]  PASSED
test_TC01_title_not_empty[chromium-dbcraftmode-https://www.dbcraftmode.pl] PASSED
```

Dodanie trzeciej strony = jedna linijka w `LIVE_SITES`. Test się nie zmienia.

---

### Moduł 1: SEO (TC-01..05)

SEO to nie tylko Google — to fundamenty dobrze zbudowanej strony.

**TC-01 — Tytuł strony:**
```python
title = page.title()
assert len(title) >= 5
```
Każda strona MUSI mieć tytuł. Brak tytułu = niewidoczność w Google + zła dostępność.

**TC-02 — Meta description:**
```python
desc = page.locator("meta[name='description']").get_attribute("content")
assert desc and len(desc) >= 10
```
Meta description pojawia się pod tytułem w wynikach wyszukiwania. Brak = Google generuje własny, często nieodpowiedni.

**TC-03 — Nagłówek H1:**
```python
h1_count = page.locator("h1").count()
assert h1_count >= 1
```
Jedna strona = jeden H1. To hierarchia treści, którą czytają zarówno Google jak i czytniki ekranu.

**TC-04 — Meta viewport:**
```python
viewport = page.locator("meta[name='viewport']").get_attribute("content")
assert viewport and "width" in viewport
```
Bez `<meta name="viewport" content="width=device-width">` strona na telefonie wygląda jak zdezoomowana wersja desktopowa.

**TC-05 — Atrybut lang:**
```python
lang = page.locator("html").get_attribute("lang")
assert lang and len(lang) >= 2
```
`<html lang="pl">` mówi czytnikowi ekranu w jakim języku czytać tekst. Bez tego — błędna wymowa przez technologie asystywne.

---

### Moduł 2: Wydajność (TC-06..08)

Playwright daje dostęp do `performance.timing` — natywnego API przeglądarki mierzącego każdy etap ładowania strony.

```python
timing = page.evaluate("""() => ({
    dcl:  performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
    load: performance.timing.loadEventEnd            - performance.timing.navigationStart,
    ttfb: performance.timing.responseStart           - performance.timing.navigationStart,
})""")
```

**Trzy mierniki:**

| Metryka | Co mierzy | Limit |
|---|---|---|
| TTFB | Time To First Byte — czas odpowiedzi serwera | < 2 000 ms |
| DOMContentLoaded | Strona sparsowana, DOM gotowy | < 5 000 ms |
| Load | Wszystko załadowane (obrazy, CSS, JS) | < 10 000 ms |

**Wyniki naszych stron:**

Obie strony zmieściły się w limitach — koparka-kobierzyce.pl i dbcraftmode.pl działają sprawnie na polskim współdzielonym hostingu.

---

### Moduł 3: Dostępność — Accessibility (TC-09..12)

Dostępność (a11y — od "accessibility", 11 liter pomiędzy a i y) to projektowanie stron tak, żeby mogły z nich korzystać osoby z niepełnosprawnościami. Reguluje to standard WCAG 2.2.

**TC-09 — Alt teksty obrazów (WCAG 1.1.1):**

```python
images_without_alt = page.evaluate("""() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    return imgs
        .filter(img => img.getAttribute('alt') === null)
        .map(img => img.src);
}""")
assert len(images_without_alt) == 0
```

`alt=""` jest OK dla obrazów dekoracyjnych. `alt` brak całkowicie = błąd WCAG. Czytnik ekranu przeczyta wtedy nazwę pliku: *"obraz: foto-klient-2023-final-v3.jpg"*.

**TC-10 — Przyciski z tekstem (WCAG 4.1.2):**

Przycisk bez tekstu (`<button><svg>...</svg></button>`) jest niewidoczny dla czytnika ekranu. Test szuka przycisków bez `innerText`, `aria-label` ani `title`.

**TC-11 — Etykiety formularzy:**

Sprytna obsługa pól honeypot (antyspamowych):

```python
# Honeypot — celowo ukryte pole bez etykiety — pomijamy je
if (inp.tabIndex < 0) return false;
const style = window.getComputedStyle(inp);
if (style.display === 'none' || style.visibility === 'hidden') return false;
```

Na obu stronach formularz zawiera ukryte pole `name="website"` z `tabindex="-1"` — to pułapka na boty. Prawdziwy użytkownik go nie widzi i nie wypełnia. Bot, który wypełnia wszystkie pola, zdradza się. Test poprawnie je ignoruje.

**TC-12 — Elementy landmark:**

```python
has_main = page.locator("main, [role='main']").count() > 0
has_nav  = page.locator("nav, [role='navigation']").count() > 0
assert has_main or has_nav
```

Elementy landmark (`<main>`, `<nav>`, `<header>`) pozwalają użytkownikowi czytnika ekranu przeskakiwać między sekcjami strony zamiast słuchać wszystkiego od początku.

---

### Znaleziony Bug: biopoprom.pl — brak struktury nagłówków

**To jest prawdziwe znalezisko testowe.** Podczas pisania TC-03 odkryłem, że `biopoprom.html` nie zawiera żadnych tagów nagłówkowych (h1-h6). Zero.

```python
# Test wykazał:
h1_count = page.locator("h1, h2, h3, h4, h5, h6").count()
# → 0
```

**Skutki:**
- Czytnik ekranu nie może zrozumieć struktury treści
- Google nie wie co jest najważniejsze na stronie
- WCAG 1.3.1 naruszony

**Raport buga (tak jak napisałbym w Jira):**

```
TYTUŁ: Brak tagów nagłówkowych h1-h6 na stronie biopoprom.html
PRIORYTET: Medium
KOMPONENT: Frontend / HTML Structure
KROKI:
  1. Otwórz biopoprom.html
  2. Uruchom w DevTools: document.querySelectorAll('h1,h2,h3,h4,h5,h6').length
OCZEKIWANE: co najmniej 1 tag nagłówkowy
RZECZYWISTE: 0
WPŁYW: dostępność (WCAG 1.3.1), SEO
```

---

### Moduł 4: Zepsute Linki (TC-13..14)

**TC-13 — Linki wewnętrzne:**

```python
# Zbierz linki z tego samego hostname
hrefs = page.evaluate("""(baseHost) => {
    return Array.from(document.querySelectorAll('a[href]'))
        .map(a => a.href)
        .filter(href => new URL(href).hostname === baseHost);
}""", base_host)

# Sprawdź każdy przez nawigację w nowej karcie
for link in unique_hrefs[:20]:
    check_page = page.context.new_page()
    response = check_page.goto(link, wait_until="domcontentloaded")
    if response and response.status >= 400:
        broken.append(f"{link} → {response.status}")
    check_page.close()
```

**Dlaczego nowa karta, nie `page.request.get()`?**

`page.request.get()` to osobny klient HTTP — nie używa certyfikatów SSL z kontekstu przeglądarki. Polskie serwery współdzielone mają często niestandardowe łańcuchy SSL. Nawigacja przez `new_page()` korzysta z pełnego silnika Chromium, który radzi sobie z tym poprawnie.

**TC-14 — Obrazy:** Nasłuchujemy na odpowiedzi sieciowe i filtrujemy obrazy z kodem ≥ 400:

```python
def handle_response(response):
    if response.request.resource_type == "image" and response.status >= 400:
        failed_images.append(f"{response.url} → {response.status}")

page.on("response", handle_response)
page.goto(url, wait_until="load")
```

---

### Moduł 5: Screenshoty (TC-15)

```python
path = SCREENSHOTS_DIR / f"{site_name}_{timestamp}.png"
page.screenshot(path=str(path), full_page=True)

assert path.exists()
assert path.stat().st_size // 1024 > 5  # > 5 KB = nie pusta strona
```

`full_page=True` robi screenshot całej długości strony, nie tylko widocznego fragmentu. Screenshots to dokumentacja — pokazują jak strona wyglądała w momencie uruchomienia testów.

---

### Wyniki

```
34 passed in 54.27s
```

| Moduł | Testy | Wynik |
|---|---|---|
| SEO | TC-01..05 (×2-3 strony) | ✅ PASSED |
| Wydajność | TC-06..08 (×2 strony) | ✅ PASSED |
| Dostępność | TC-09..12 (×2-3 strony) | ✅ PASSED |
| Zepsute linki | TC-13..14 (×2 strony) | ✅ PASSED |
| Screenshoty | TC-15 (×3 strony) | ✅ PASSED |

**Bonus — znaleziony bug:** biopoprom.html nie ma żadnych tagów nagłówkowych (WCAG 1.3.1 naruszony).

---

### Nowe umiejętności zdobyte w tej fazie

| Umiejętność | Gdzie użyta |
|---|---|
| `@pytest.mark.parametrize` | Jeden test dla wielu stron |
| `performance.timing` API | Pomiar TTFB, DCL, Load |
| `page.evaluate()` z JavaScript | Analiza DOM (alt, labels, headings) |
| Wykrywanie honeypot fields | TC-11 — tabindex i getComputedStyle |
| `page.on("response", handler)` | Monitorowanie zasobów sieciowych |
| `page.context.new_page()` | Sprawdzanie linków bez SSL issues |
| Raportowanie bugów (WCAG) | Znalezisko biopoprom — brak h1-h6 |
| `full_page=True` screenshoty | Dokumentacja wizualna |

---

### Pliki z testami

`automation/tests/crosssite/test_crosssite.py` — 15 przypadków testowych × 2-3 strony = 34 uruchomienia.

`automation/reports/screenshots/` — screenshoty każdej strony z timestampem.

---

*Faza 6 ukończona: 2026-05-21 | Wynik: 34/34 PASSED | Bug znaleziony: biopoprom brak h1-h6*
