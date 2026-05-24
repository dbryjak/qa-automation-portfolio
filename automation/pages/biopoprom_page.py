from pages.base_page import BasePage

LOCAL_URL = "file:///d:/STRONY_WWW/www.biopoprom.pl/biopoprom.html"
LIVE_URL  = "https://www.biopoprom.pl"


class BiopopromPage(BasePage):
    # Nawigacja
    TAB_ZEGAR     = "#tab-zegar"
    TAB_KALENDARZ = "#tab-kalendarz"
    TAB_SIEC      = "#tab-siec"
    TAB_HARMONIA  = "#tab-harmonia"

    # Sekcje (strony)
    PAGE_ZEGAR     = "#page-zegar"
    PAGE_KALENDARZ = "#page-kalendarz"
    PAGE_SIEC      = "#page-siec"
    PAGE_HARMONIA  = "#page-harmonia"

    # Zegar
    CLOCK_CANVAS = "#clockCanvas"
    BP_TIME      = "#bpTime"
    REAL_TIME    = "#realTime"
    MOON_PHASE   = "#moonPhaseName"
    MOON_NEXT    = "#moonNextEvent"

    # Kalendarz
    CALENDAR_AREA = "#calendarArea"
    MONTH_NAME    = "#calMonthName"
    BTN_PREV      = "#btnPrev"
    BTN_NEXT      = "#btnNext"
    OVERVIEW_GRID = "#overviewGrid"

    # Siec — kalkulator
    STD_INPUT  = "#stdIn"
    STD_RESULT = "#stdResult"
    BP_INPUT   = "#bpIn"
    BP_RESULT  = "#bpResult"
    HERO_TIME  = "#heroTime"

    # Harmonia
    BTN_PLAY      = "#btnPlay"
    HZ_NUM        = "#hzNum"
    WZROST_INPUT  = "#wzrostInput"
    PHI_RESULTS   = "#phiResults"
    CI_DEG        = "#ciDeg"

    def open(self):
        self.navigate(LOCAL_URL)
        self.page.wait_for_load_state("networkidle")

    def switch_tab(self, name: str):
        self.page.locator(f"#tab-{name}").click()
        self.page.wait_for_timeout(400)

    def is_section_active(self, name: str) -> bool:
        return "active" in (self.page.locator(f"#page-{name}").get_attribute("class") or "")

    def get_tab_labels(self) -> list[str]:
        return self.page.locator(".btab").all_inner_texts()

    def get_bp_time(self) -> str:
        return self.page.locator(self.BP_TIME).inner_text()

    def get_real_time(self) -> str:
        return self.page.locator(self.REAL_TIME).inner_text()

    def get_moon_phase(self) -> str:
        return self.page.locator(self.MOON_PHASE).inner_text()

    def get_month_name(self) -> str:
        return self.page.locator(self.MONTH_NAME).inner_text()

    def click_prev_month(self):
        self.page.locator(self.BTN_PREV).click()
        self.page.wait_for_timeout(300)

    def click_next_month(self):
        self.page.locator(self.BTN_NEXT).click()
        self.page.wait_for_timeout(300)

    def calculate_std_to_bp(self, time_str: str) -> str:
        self.page.fill(self.STD_INPUT, time_str)
        self.page.locator(self.STD_INPUT).dispatch_event("input")
        self.page.wait_for_timeout(200)
        return self.page.locator(self.STD_RESULT).inner_text()

    def calculate_bp_to_std(self, time_str: str) -> str:
        self.page.fill(self.BP_INPUT, time_str)
        self.page.locator(self.BP_INPUT).dispatch_event("input")
        self.page.wait_for_timeout(200)
        return self.page.locator(self.BP_RESULT).inner_text()

    def calculate_phi(self, height_cm: int) -> str:
        self.page.fill(self.WZROST_INPUT, str(height_cm))
        self.page.locator("button", has_text="Oblicz").click()
        self.page.wait_for_timeout(300)
        return self.page.locator(self.PHI_RESULTS).inner_text()
