# Rozdział 11 — Nauka własna: testuję swoją stronę manualnie

> **Jak korzystać z tego rozdziału:**  
> Otwórz www.danielbryjak.pl na telefonie lub komputerze, wróć tutaj  
> i wykonuj testy jeden po drugim. Możesz zacząć od dowolnego miejsca.  
> Przy każdym angielskim terminie znajdziesz: jak czytać + co oznacza.

---

## CZĘŚĆ 1 — Słownik testera (angielski od A do Z)

> Ucz się tych słów — padną na każdej rozmowie kwalifikacyjnej.

| Termin | Wymowa | Co to jest | Do czego służy |
|---|---|---|---|
| **Test case** | *"test kejs"* | Przypadek testowy | Jeden scenariusz: co klikam, co wpisuję, czego oczekuję |
| **TC** | *"ti-si"* | Skrót od Test Case | Identyfikator przypadku testowego, np. TC-001 |
| **PASS** | *"pas"* | Zaliczony | Test przeszedł — wynik zgodny z oczekiwanym |
| **FAIL** | *"fejl"* | Niezaliczony | Test nie przeszedł — coś działa inaczej niż powinno |
| **BLOCKED** | *"blokt"* | Zablokowany | Nie można wykonać testu, bo coś innego nie działa |
| **Bug** | *"bag"* | Błąd w aplikacji | Coś działa inaczej niż powinno |
| **Bug report** | *"bag riport"* | Raport błędu | Dokument opisujący znaleziony błąd — co, gdzie, jak powtórzyć |
| **Test plan** | *"test plan"* | Plan testów | Dokument: co testujemy, w jakiej kolejności, co pomijamy |
| **Smoke test** | *"smołk test"* | Test dymny | Szybkie sprawdzenie czy aplikacja w ogóle działa (5–15 min) |
| **Regression test** | *"rigreszen test"* | Test regresji | Sprawdzenie czy nowe zmiany nie zepsuły starych funkcji |
| **Exploratory test** | *"eksploratory test"* | Test eksploracyjny | Testowanie bez scenariusza — klikasz i szukasz problemów |
| **UAT** | *"ju-ej-ti"* | User Acceptance Testing | Testowanie przez prawdziwego użytkownika / klienta |
| **E2E** | *"i-tu-i"* | End-to-End | Test całego procesu od początku do końca |
| **UI** | *"ju-aj"* | User Interface | Interfejs użytkownika — jak strona wygląda |
| **UX** | *"ju-eks"* | User Experience | Doświadczenie użytkownika — jak strona się używa |
| **CTA** | *"si-ti-ej"* | Call To Action | Przycisk zachęcający do działania, np. "Napisz do mnie" |
| **Header** | *"heder"* | Nagłówek | Górna część strony (menu, logo) |
| **Footer** | *"futer"* | Stopka | Dolna część strony (copyright, linki) |
| **Hero section** | *"hiro sekszyn"* | Sekcja główna | Pierwsza duża sekcja na stronie — tytuł, CTA |
| **DevTools** | *"dev tuls"* | Narzędzia deweloperskie | Wbudowane w przeglądarkę — otwierasz przez F12 |
| **Responsive** | *"risponsyw"* | Responsywny | Strona dostosowuje się do różnych rozmiarów ekranu |
| **Viewport** | *"wjupport"* | Obszar widoku | Widoczna część strony — zmienia się na telefonie i PC |
| **Repository** | *"ripozytory"* | Repozytorium | Miejsce przechowywania kodu — np. na GitHub |
| **GitHub** | *"gyt-hab"* | GitHub | Serwis do przechowywania i udostępniania kodu |
| **Priority** | *"prajoryti"* | Priorytet | Ważność błędu: Critical / High / Medium / Low |
| **Critical** | *"krytikol"* | Krytyczny | Aplikacja nie działa — blokuje wszystkich użytkowników |
| **High** | *"haj"* | Wysoki | Ważna funkcja nie działa, ale jest obejście |
| **Medium** | *"midium"* | Średni | Utrudnia pracę, ale nie blokuje |
| **Low** | *"lo"* | Niski | Drobiazg, literówka, kosmetyczny błąd |
| **Environment** | *"enwajrynment"* | Środowisko | Gdzie testujesz: Chrome/Windows/iPhone itd. |
| **Expected result** | *"ikspektid rizalt"* | Oczekiwany wynik | Co POWINNO się stać po wykonaniu kroku |
| **Actual result** | *"akczual rizalt"* | Rzeczywisty wynik | Co SIĘ STAŁO w rzeczywistości |
| **Reproduction steps** | *"riprodakszyn steps"* | Kroki do reprodukcji | Jak powtórzyć błąd krok po kroku |
| **Test suite** | *"test sjut"* | Zestaw testów | Kolekcja powiązanych przypadków testowych |
| **Checklist** | *"czeklyst"* | Lista kontrolna | Uproszczona lista rzeczy do sprawdzenia |

---

## CZĘŚĆ 2 — Plan testowy dla danielbryjak.pl

> **Test plan** (*"test plan"*) — zanim zaczniesz klikać, tester zawsze odpowiada na 3 pytania.

### Co testujemy?
Stronę portfolio **www.danielbryjak.pl** — stronę QA Engineera Daniela Bryjaka.

### Co sprawdzamy?
- Nawigacja (czy menu działa)
- Linki (czy prowadzą we właściwe miejsca)
- Animacje (czy liczniki się kręcą)
- Responsywność (*"risponsywność"*) — czy strona wygląda dobrze na telefonie
- Sekcja kontakt (email, GitHub, LinkedIn)

### Co pomijamy (na teraz)?
- Testy wydajnościowe (*"performans testyng"*) — jak szybko się ładuje
- Testy bezpieczeństwa (*"sikjurity testyng"*)
- SEO (*"es-i-o"* = Search Engine Optimization = jak strona jest widoczna w Google)

---

## CZĘŚĆ 3 — Przypadki testowe (Test Cases)

> Dla każdego testu wpisz **wynik** i **status** (PASS / FAIL / BLOCKED).  
> Kolumna "Mój wynik" jest pusta — uzupełniasz ją sam podczas testowania.

---

### TC-001 | Nawigacja — link "O mnie"

| Pole | Wartość |
|---|---|
| **ID** | TC-001 |
| **Nazwa** | Nawigacja — link "O mnie" |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij "O mnie" w górnym menu (header) |
| **Oczekiwany wynik** | Strona płynnie przewija się do sekcji "O mnie" |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-002 | Nawigacja — link "Projekty"

| Pole | Wartość |
|---|---|
| **ID** | TC-002 |
| **Nazwa** | Nawigacja — link "Projekty" |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij "Projekty" w górnym menu |
| **Oczekiwany wynik** | Strona przewija się do sekcji z kartami projektów |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-003 | Nawigacja — link "Umiejętności"

| Pole | Wartość |
|---|---|
| **ID** | TC-003 |
| **Nazwa** | Nawigacja — link "Umiejętności" |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij "Umiejętności" w górnym menu |
| **Oczekiwany wynik** | Strona przewija się do sekcji z listą umiejętności |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-004 | Nawigacja — link "Kontakt"

| Pole | Wartość |
|---|---|
| **ID** | TC-004 |
| **Nazwa** | Nawigacja — link "Kontakt" |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij "Kontakt" w górnym menu |
| **Oczekiwany wynik** | Strona przewija się do sekcji z danymi kontaktowymi |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-005 | Animacja liczników

| Pole | Wartość |
|---|---|
| **ID** | TC-005 |
| **Nazwa** | Animacja liczników w sekcji hero |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Załaduj stronę od nowa (Ctrl+R lub F5) |
| **Krok 2** | Obserwuj liczby w sekcji hero (147, 6, PASS) |
| **Oczekiwany wynik** | Liczniki animują się od 0 do wartości docelowej (147, 6) |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-006 | Przycisk CTA — "Zobacz jak testuję"

| Pole | Wartość |
|---|---|
| **ID** | TC-006 |
| **Nazwa** | Przycisk CTA (*"si-ti-ej"*) w sekcji hero |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij zielony przycisk "Zobacz jak testuję prawdziwe aplikacje" |
| **Oczekiwany wynik** | Strona przewija się do sekcji z projektami |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-007 | Link GitHub w sekcji hero

| Pole | Wartość |
|---|---|
| **ID** | TC-007 |
| **Nazwa** | Link GitHub — sekcja główna |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Kliknij przycisk "GitHub" obok przycisku CTA |
| **Oczekiwany wynik** | Otwiera się profil GitHub: github.com/dbryjak (w nowej karcie) |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-008 | Link e-mail w sekcji kontakt

| Pole | Wartość |
|---|---|
| **ID** | TC-008 |
| **Nazwa** | Link e-mail w sekcji Kontakt |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Przewiń do sekcji "Kontakt" |
| **Krok 2** | Kliknij przycisk z adresem e-mail |
| **Oczekiwany wynik** | Otwiera się klient poczty (Outlook, Gmail) z wypełnionym adresem |
| **Uwaga** | Jeśli nie masz klienta poczty — to nie jest błąd strony, to ustawienie systemu |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-009 | Link LinkedIn w sekcji kontakt

| Pole | Wartość |
|---|---|
| **ID** | TC-009 |
| **Nazwa** | Link LinkedIn (*"linked-in"*) w sekcji Kontakt |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce |
| **Krok 1** | Przewiń do sekcji "Kontakt" |
| **Krok 2** | Kliknij przycisk "LinkedIn" |
| **Oczekiwany wynik** | Otwiera się profil LinkedIn Daniela Bryjaka (w nowej karcie) |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

### TC-010 | Responsywność mobilna

| Pole | Wartość |
|---|---|
| **ID** | TC-010 |
| **Nazwa** | Responsywność (*"risponsywność"*) — widok mobilny |
| **Warunek wstępny** | Strona danielbryjak.pl otwarta w przeglądarce Chrome na komputerze |
| **Krok 1** | Naciśnij **F12** — otworzy się DevTools (*"dev tuls"* = narzędzia deweloperskie) |
| **Krok 2** | Kliknij ikonę telefonu w górnym pasku DevTools (Toggle device toolbar) |
| **Krok 3** | Z listy urządzeń wybierz **iPhone 12** |
| **Krok 4** | Przejrzyj całą stronę od góry do dołu |
| **Oczekiwany wynik** | Strona wygląda poprawnie — menu czytelne, teksty nie wychodzą poza ekran, przyciski klikalne |
| **Mój wynik** | *(wpisz co zobaczysz)* |
| **Status** | PASS / FAIL / BLOCKED |

---

## CZĘŚĆ 4 — Szablon raportu błędu (Bug Report)

> Kiedy znajdziesz **FAIL** — opisz go tym szablonem.  
> To dokument, który wysyłasz programiście. Musi być precyzyjny.

```
TYTUŁ:           [krótki opis — np. "Link LinkedIn otwiera złą stronę"]

ŚRODOWISKO:      Chrome 124 / Windows 10 / desktop
(environment)    LUB: Safari / iPhone 14 / mobile

KROKI DO REPRODUKCJI:
(reproduction    1. Otwórz www.danielbryjak.pl
steps)           2. Przewiń do sekcji "Kontakt"
                 3. Kliknij przycisk "LinkedIn"

OCZEKIWANY WYNIK:
(expected        Otwiera się profil linkedin.com/in/daniel-bryjak-3361a724b/
result)

RZECZYWISTY WYNIK:
(actual          Otwiera się strona linkedin.com/in/daniel-bryjak/ (błędna)
result)

PRIORYTET:       Wysoki (High)
(priority)       [Krytyczny / Wysoki / Średni / Niski]

ZAŁĄCZNIK:       screenshot.png (zrzut ekranu błędu)
```

---

## CZĘŚĆ 5 — Moje wyniki testów

> Wypełnij po wykonaniu testów. Wróć tutaj za miesiąc i sprawdź ponownie.

| ID | Nazwa | Status | Data | Uwagi |
|---|---|---|---|---|
| TC-001 | Nawigacja — O mnie | | | |
| TC-002 | Nawigacja — Projekty | | | |
| TC-003 | Nawigacja — Umiejętności | | | |
| TC-004 | Nawigacja — Kontakt | | | |
| TC-005 | Animacja liczników | | | |
| TC-006 | Przycisk CTA | | | |
| TC-007 | Link GitHub | | | |
| TC-008 | Link e-mail | | | |
| TC-009 | Link LinkedIn | | | |
| TC-010 | Responsywność mobilna | | | |

**Wynik sesji:** ___/10 PASS | ___/10 FAIL | Data: ________

---

## CZĘŚĆ 6 — Co dalej? (następne lekcje)

> Wróć tutaj gdy skończysz TC-001 do TC-010. Dodamy kolejne.

- [ ] **Lekcja 2** — Testowanie formularzy i pól tekstowych
- [ ] **Lekcja 3** — Testowanie na różnych przeglądarkach (cross-browser)
- [ ] **Lekcja 4** — Podstawy TestRail — zarządzanie przypadkami testowymi
- [ ] **Lekcja 5** — Symulacja rozmowy kwalifikacyjnej — bronisz swojego portfolio

---

*Rozdział żywy — aktualizowany na bieżąco.*
