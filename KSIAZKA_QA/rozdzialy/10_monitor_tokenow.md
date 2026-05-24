# Rozdział 10 — Monitor Tokenów Claude
## Testowanie aplikacji desktopowej (Python + tkinter + pystray)

**Typ aplikacji:** Desktop GUI — Windows System Tray  
**Stack:** Python 3.14 · tkinter · pystray · Pillow  
**Typ testów:** Manualny exploratory + regresja  
**Znalezione bugi:** 5  
**Status:** ✅ Wszystkie naprawione

---

## 10.1 Opis aplikacji

Monitor Tokenów to autorska aplikacja desktopowa napisana od zera, która:
- siedzi przy zegarku systemowym Windows (System Tray)
- po kliknięciu pokazuje okienko z danymi o zużyciu tokenów AI
- czyta pliki JSONL z katalogu `~/.claude/` (lokalne logi Claude Code)
- oblicza koszty w czasie rzeczywistym wg cennika Anthropic
- obsługuje dwa tryby: **PRO** (abonament $20/mies.) i **API** (kredyty pay-per-use)

**Dlaczego to trudniejsze niż testowanie stron www?**  
Aplikacje desktopowe nie mają DevTools, nie ma Playwright który by kliknął za nas. Każdy test jest ręczny. Trzeba obserwować zachowanie okienek, pasków zadań, ikon systemowych, plików konfiguracyjnych.

---

## 10.2 Plan testów

### Obszary ryzyka (Risk-Based Testing)

| Obszar | Ryzyko | Priorytet |
|--------|--------|-----------|
| Uruchamianie aplikacji | Może nie działać na innym systemie | Wysoki |
| Zachowanie ikony tray | Brak standardu Windows — zależy od wersji OS | Wysoki |
| Przyciski okienka (X, _, PRO/API) | Nieoczekiwane zachowanie w GUI | Wysoki |
| Odczyt plików JSONL | Błędy parsowania, brakujące pliki | Średni |
| Obliczanie kosztów | Błędy matematyczne, złe ceny modeli | Średni |
| Plik config.json | Błędy odczytu, złe wartości | Średni |
| Widoczność w pasku zadań | Okienko tray nie powinno się tam pojawiać | Niski |

### Zakres testów

- ✅ Smoke tests (czy w ogóle działa)
- ✅ Testy funkcjonalne (każdy przycisk, każde pole)
- ✅ Testy konfiguracji (różne wartości w config.json)
- ✅ Testy regresji (po każdej poprawce)
- ❌ Testy automatyczne (GUI desktopowe — poza zakresem tej wersji)

---

## 10.3 Przypadki testowe

### TC-01 — Uruchomienie aplikacji

| | |
|---|---|
| **ID** | TC-01 |
| **Tytuł** | Aplikacja uruchamia się bez okna konsoli |
| **Warunek wstępny** | Python 3.14, pystray, Pillow zainstalowane |
| **Kroki** | 1. Dwuklik na `START_TRAY.vbs` |
| **Oczekiwany wynik** | Ikona pojawia się przy zegarku, żadne okno konsoli/CMD nie jest widoczne |
| **Wynik** | ✅ PASS (po poprawce — patrz BUG-02) |

---

### TC-02 — Otwieranie okienka

| | |
|---|---|
| **ID** | TC-02 |
| **Tytuł** | Kliknięcie ikony tray otwiera okienko z danymi |
| **Kroki** | 1. Uruchom aplikację → 2. Kliknij ikonę przy zegarku |
| **Oczekiwany wynik** | Okienko otwiera się, zawiera dane tokenów i przycisk PRO/API |
| **Wynik** | ✅ PASS |

---

### TC-03 — Zamknięcie przyciskiem X

| | |
|---|---|
| **ID** | TC-03 |
| **Tytuł** | Przycisk X ukrywa okienko, nie wyłącza aplikacji |
| **Kroki** | 1. Otwórz okienko → 2. Kliknij X |
| **Oczekiwany wynik** | Okienko znika, ikona przy zegarku pozostaje aktywna |
| **Wynik** | ✅ PASS (po poprawce — patrz BUG-03) |

---

### TC-04 — Widoczność w pasku zadań

| | |
|---|---|
| **ID** | TC-04 |
| **Tytuł** | Okienko NIE pojawia się w pasku zadań Windows |
| **Kroki** | 1. Otwórz okienko → 2. Sprawdź pasek zadań na dole ekranu |
| **Oczekiwany wynik** | Pasek zadań jest czysty — okienko widać tylko jako ikonę tray |
| **Wynik** | ✅ PASS (`-toolwindow` attribute) |

---

### TC-05 — Przełączanie trybów PRO / API

| | |
|---|---|
| **ID** | TC-05 |
| **Tytuł** | Przyciski PRO i API przełączają tryb i zapisują do config.json |
| **Kroki** | 1. Otwórz okienko → 2. Kliknij "API" → 3. Zamknij i otwórz config.json |
| **Oczekiwany wynik** | Panel API podświetlony, w config.json `"tryb": "api"` |
| **Wynik** | ✅ PASS |

---

### TC-06 — Zakończenie przez menu tray

| | |
|---|---|
| **ID** | TC-06 |
| **Tytuł** | Opcja "Zakończ" w menu tray kończy cały proces |
| **Kroki** | 1. Prawy klik na ikonę → 2. Kliknij "Zakończ" → 3. Sprawdź Task Manager |
| **Oczekiwany wynik** | Ikona znika, żaden proces python/pythonw nie jest widoczny |
| **Wynik** | ✅ PASS (po poprawce — patrz BUG-01) |

---

### TC-07 — Czytelność czcionek

| | |
|---|---|
| **ID** | TC-07 |
| **Tytuł** | Tekst w okienku jest czytelny na ciemnym tle |
| **Kroki** | 1. Otwórz okienko → 2. Oceń kontrast etykiet i wartości |
| **Oczekiwany wynik** | Etykiety: szary (#a0a0c0), wartości: biały (#e0e0f0), wyróżnione: cyan |
| **Wynik** | ✅ PASS (po poprawce — patrz BUG-04) |

---

### TC-08 — Aktualizacja salda API

| | |
|---|---|
| **ID** | TC-08 |
| **Tytuł** | Dialog "Zaktualizuj saldo" poprawnie zapisuje kwotę i datę |
| **Kroki** | 1. Otwórz okienko → 2. Kliknij "↺ Zaktualizuj saldo po doładowaniu" → 3. Wpisz `5.00` → 4. Kliknij Zapisz → 5. Sprawdź config.json |
| **Oczekiwany wynik** | W config.json: `"saldo_api_usd": 5.0`, `"saldo_data_wpisania": "<dzisiaj>"` |
| **Wynik** | ✅ PASS |

---

### TC-09 — Walidacja w dialogu salda

| | |
|---|---|
| **ID** | TC-09 |
| **Tytuł** | Dialog odrzuca niepoprawne wartości salda |
| **Kroki** | 1. Otwórz dialog → 2. Wpisz `abc` → 3. Kliknij Zapisz |
| **Oczekiwany wynik** | Komunikat błędu "⚠ Wpisz poprawną kwotę", dialog nie zamknięty |
| **Wynik** | ✅ PASS |

---

### TC-10 — Odczyt danych z JSONL

| | |
|---|---|
| **ID** | TC-10 |
| **Tytuł** | Liczba wywołań i tokeny są zgodne z zawartością plików JSONL |
| **Kroki** | 1. Otwórz okienko → 2. Odczytaj "Wywołania API" i "Tokeny łącznie" → 3. Porównaj z ręcznym liczeniem wpisów w `~/.claude/**/*.jsonl` z dzisiejszą datą |
| **Oczekiwany wynik** | Wartości zgodne (±0, bez zaokrągleń) |
| **Wynik** | ✅ PASS |

---

## 10.4 Raporty błędów (Bug Reports)

### BUG-01 — "Zakończ" nie kończy procesu

| | |
|---|---|
| **ID** | BUG-01 |
| **Tytuł** | Opcja "Zakończ" w menu tray nie zamyka aplikacji |
| **Środowisko** | Windows 10, Python 3.14, pystray |
| **Kroki do reprodukcji** | 1. Uruchom tray_monitor.py → 2. Prawy klik na ikonę → 3. Kliknij "Zakończ" |
| **Wynik rzeczywisty** | Ikona znika, ale proces `pythonw.exe` nadal widoczny w Task Manager |
| **Wynik oczekiwany** | Proces całkowicie zakończony |
| **Przyczyna** | `icon.stop()` zatrzymuje pystray, ale `tkinter.mainloop()` na głównym wątku nadal działa — aplikacja zawisła niewidocznie |
| **Naprawa** | Dodano `root.after(0, root.destroy)` po `icon.stop()` — schedules destroy w wątku tkinter |
| **Priorytet** | Wysoki |
| **Status** | ✅ Naprawiony |

```python
# PRZED (bug):
def _zakoncz(self, icon=None, item=None):
    self.icon.stop()

# PO (fix):
def _zakoncz(self, icon=None, item=None):
    self.icon.stop()
    if self.okno.root and self.okno.root.winfo_exists():
        self.okno.root.after(0, self.okno.root.destroy)
```

---

### BUG-02 — Okno CMD widoczne przy starcie

| | |
|---|---|
| **ID** | BUG-02 |
| **Tytuł** | Przy uruchomieniu START_TRAY.bat pojawia się okno konsoli CMD |
| **Środowisko** | Windows 10 |
| **Kroki do reprodukcji** | Dwuklik na `START_TRAY.bat` |
| **Wynik rzeczywisty** | Czarne okno CMD (`C:\Windows\system32\cmd.exe`) pojawia się na chwilę |
| **Wynik oczekiwany** | Aplikacja tray uruchamia się całkowicie po cichu |
| **Przyczyna** | Plik `.bat` zawsze otwiera `cmd.exe` jako hosta — nawet jeśli sam skrypt nie produkuje output |
| **Naprawa** | Zastąpiono `.bat` skryptem `.vbs` z `oShell.Run ..., 0, False` (parametr `0` = ukryte okno) |
| **Priorytet** | Średni (UX) |
| **Status** | ✅ Naprawiony |

```vbscript
' START_TRAY.vbs — uruchamia pythonw bez żadnego okna
Set oShell = CreateObject("WScript.Shell")
oShell.Environment("Process")("PYTHONUTF8") = "1"
oShell.Run "C:\Python314\pythonw.exe ""...\tray_monitor.py""", 0, False
```

---

### BUG-03 — Przycisk X zamykał aplikację zamiast ukrywać

| | |
|---|---|
| **ID** | BUG-03 |
| **Tytuł** | Kliknięcie X niszczyło okienko i wyłączało aplikację |
| **Kroki do reprodukcji** | Otwórz okienko → kliknij X |
| **Wynik rzeczywisty** | Okienko i cała aplikacja zakończona |
| **Wynik oczekiwany** | Okienko chowa się, ikona tray pozostaje |
| **Przyczyna** | Domyślne zachowanie `tkinter.Tk()` przy zamknięciu to `destroy()` |
| **Naprawa** | `root.protocol("WM_DELETE_WINDOW", self.ukryj)` — przechwycenie zdarzenia zamknięcia + `root.withdraw()` zamiast destroy |
| **Priorytet** | Wysoki |
| **Status** | ✅ Naprawiony |

---

### BUG-04 — Słaby kontrast czcionek

| | |
|---|---|
| **ID** | BUG-04 |
| **Tytuł** | Etykiety w okienku słabo widoczne na ciemnym tle |
| **Kroki do reprodukcji** | Otwórz okienko, przeczytaj etykiety "Wywołania API", "Tokeny wejście" |
| **Wynik rzeczywisty** | Tekst ledwo czytelny — zbyt ciemny szary na czarnym tle |
| **Wynik oczekiwany** | Wyraźny kontrast, tekst dobrze czytelny |
| **Przyczyna** | Zbyt zbliżone kolory tekstu i tła |
| **Naprawa** | Jasny kolor tekstu `#e0e0f0`, etykiety `#a0a0c0`, rozmiar czcionki 10-11pt (Segoe UI) |
| **Priorytet** | Średni (UX/dostępność) |
| **Status** | ✅ Naprawiony |

---

### BUG-05 — Okienko widoczne w pasku zadań

| | |
|---|---|
| **ID** | BUG-05 |
| **Tytuł** | Okienko monitora pojawiało się w pasku zadań Windows |
| **Kroki do reprodukcji** | Otwórz okienko, sprawdź pasek zadań |
| **Wynik rzeczywisty** | Okienko widoczne na pasku — jak zwykła aplikacja |
| **Wynik oczekiwany** | Brak wpisu w pasku zadań — aplikacja tray żyje tylko przy zegarku |
| **Przyczyna** | Domyślne okno `tkinter.Tk()` zawsze trafia do paska zadań |
| **Naprawa** | `root.attributes("-toolwindow", True)` — flaga Windows Tool Window usuwa wpis z paska i przycisk minimalizacji |
| **Priorytet** | Niski |
| **Status** | ✅ Naprawiony |

---

## 10.5 Czego się nauczyłem

**Testowanie desktopowe vs. webowe:**

| | Testowanie web | Testowanie desktop |
|---|---|---|
| Narzędzia auto | Playwright, Selenium | pyautogui, sikuli (tu: brak) |
| Dostęp do DOM | DevTools, locatory | Brak — tylko API tkinter |
| Wielowątkowość | Rzadko problem | Kluczowy problem (główny wątek GUI) |
| Konfiguracja | URL, cookies | Pliki config, zmienne środowiskowe |
| Raportowanie błędów | Screenshot + URL | Screenshot + opis stanu systemu |

**Kluczowa lekcja:** W GUI desktopowym szczególnie ważna jest izolacja wątków. Tkinter wymaga, żeby wszystkie operacje na widgetach wykonywały się na głównym wątku. Wywołanie `root.destroy()` z wątku pystray bez `root.after()` powoduje błąd trudny do zdebugowania.

**Technika root cause analysis:**  
Dla BUG-01 ślad był nieoczywisty — aplikacja "niby działała" (okno znikało, ikona znikała), ale proces żył. Dopiero `Get-WmiObject Win32_Process` ujawnił ukryte procesy Python. To pokazuje jak ważne jest sprawdzanie stanu systemu, nie tylko UI.

---

## 10.6 Regresja — checklist przed każdym wdrożeniem

```
□ START_TRAY.vbs uruchamia się bez okna CMD
□ Ikona pojawia się przy zegarku (zielona = PRO, niebieska = API)
□ Klik ikony → okienko widoczne
□ X → okienko znika, ikona zostaje
□ Okienko NIE ma wpisu w pasku zadań
□ Przycisk PRO → podświetlony panel PRO, config.json tryb="pro"
□ Przycisk API → podświetlony panel API, config.json tryb="api"
□ Dialog salda: poprawna kwota → zapisuje, błędna → komunikat błędu
□ "Zakończ" → żaden pythonw.exe w Task Manager
□ Tokeny odświeżają się co 30 sekund
```

---

*Aplikacja napisana i przetestowana: maj 2026*  
*Autor testów: Daniel Bryjak*
