# Rozdział 0 — Wstęp
## Moja droga do testowania oprogramowania

---

### Skąd się tu wziąłem

Nie zaczynałem jako programista. Przez lata pracowałem w zupełnie innej branży — ale technologia zawsze była gdzieś obok. Strony internetowe robiłem z ciekawości, dla siebie, potem dla znajomych, a w końcu dla pierwszego klienta. Koparka-kobierzyce.pl, dbcraftmode.pl — to nie są projekty zrobione na kursie. To projekty, za które ktoś zapłacił albo z których korzystam na co dzień.

W pewnym momencie zadałem sobie pytanie: "Robię strony, ale skąd wiem, że działają poprawnie?" Klikałem ręcznie. Sprawdzałem formularz. Patrzyłem czy tytuł się ładuje. To **było** testowanie — tylko że nieświadome i nieustrukturyzowane.

Kurs SDA "Tester Oprogramowania" był odpowiedzią na to pytanie.

---

### Kurs SDA — co mi dał

SDA (Software Development Academy) to intensywny kurs, który przeszedł mnie przez cały cykl życia testowania oprogramowania:

- Testowanie manualne — typy testów, przypadki testowe, raporty bugów
- TestRail — zarządzanie przypadkami testowymi
- Jira — śledzenie bugów w profesjonalnym środowisku
- SQL — podstawy zapytań do bazy danych
- Podstawy automatyzacji — pierwsze kroki z narzędziami do testów

Po kursie trzymałem w ręku certyfikat. Ale certyfikat to dopiero punkt wyjścia. Rekruterzy chcą widzieć **projekty**, nie tylko dyplomy.

---

### Dlaczego ta książka

Postanowiłem zbudować coś, czego większość juniorów nie ma: **udokumentowane portfolio automatyzacji na żywych projektach**.

Nie na tutorialowych appkach. Nie na środowiskach ćwiczebnych. Na prawdziwych stronach — takich, które działają produkcyjnie, mają prawdziwych użytkowników i gdzie znaleziony błąd ma realną wartość.

Ta książka to dokumentacja tej drogi. Każdy rozdział to jedna strona, jeden zestaw testów, jedna lekcja.

---

### Stack technologiczny projektu

```
Python 3.14
Pytest 9.0
Playwright 1.60 (pytest-playwright)
pytest-html — raporty HTML
Page Object Model — wzorzec projektowy
```

Dlaczego Playwright, a nie Selenium?

Playwright to nowoczesna alternatywa — szybszy, stabilniejszy, z wbudowaną obsługą async i auto-wait. W 2024/2025 roku jest standardem w nowych projektach testowych. Pracodawcy to wiedzą.

---

### Struktura projektu

```
d:\Projekt SDA\
├── automation\
│   ├── pages\          ← Page Object classes
│   ├── tests\
│   │   ├── store\      ← Faza 1: saucedemo.com
│   │   ├── biopoprom\  ← Faza 2: biopoprom.pl
│   │   ├── koparka\    ← Faza 3: koparka-kobierzyce.pl
│   │   ├── dbcraftmode\ ← Faza 4: dbcraftmode.pl
│   │   └── testron\    ← Faza 5: TESTron.pl
│   └── reports\        ← raporty HTML
└── KSIAZKA_QA\         ← ta książka
```

Każda faza to osobny folder z testami i osobna klasa Page Object. Kod jest czytelny, modulowy i gotowy do pokazania rekruterowi.

---

### Co znajdziesz w tej książce

| Rozdział | Strona | Czego się nauczysz |
|---|---|---|
| 1 | saucedemo.com | POM, pierwsze testy logowania, asercje |
| 2 | biopoprom.pl | Testy smoke, UI, SPA z zakładkami |
| 3 | koparka-kobierzyce.pl | CRM, formularz, blog, sesje |
| 4 | dbcraftmode.pl | CRUD, panel admina, CSRF, debugowanie |
| 5 | TESTron.pl | Full-stack, API |
| 6 | Wszystkie strony | SEO, dostępność, wydajność, cross-browser |

---

*"Nie klikam — testuję."*

*— Daniel Bryjak, QA Automation Engineer*
