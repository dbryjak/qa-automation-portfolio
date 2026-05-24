from pages.base_page import BasePage

BASE_URL     = "https://koparka-kobierzyce.pl"
CRM_PASSWORD = "koparki2026"   # z crm/config.php — zmień jeśli hasło produkcyjne jest inne


class KoparkaHomePage(BasePage):
    TITLE_EXPECTED  = "KOPARKI Kobierzyce"
    LOGO_CIRCLE     = ".logo-circle"
    NAV             = ".topbar-nav"
    NAV_LINKS       = ".topbar-nav a"
    BTN_CTA         = ".topbar-cta"
    HERO_TITLE      = ".hero-title"
    SECTION_OFERTA  = "#oferta"
    SECTION_WYKOPY  = "#wykopy"
    SECTION_KONTAKT = "#kontakt"
    CONTACT_FORM    = "#contactForm"
    FIELD_NAME      = "input[name='name']"
    FIELD_PHONE     = "input[name='phone']"
    SELECT_SERVICE  = "select[name='service']"
    BTN_SUBMIT      = "#submitBtn"
    FOOTER          = "footer"
    SECTIONS = ["oferta", "wykopy", "przylacza", "szambo", "realizacje", "kontakt"]

    def open(self):
        self.navigate(BASE_URL)

    def scroll_to(self, section_id: str):
        self.page.evaluate(f"document.getElementById('{section_id}').scrollIntoView()")
        self.page.wait_for_timeout(400)

    def get_nav_links(self) -> list[str]:
        return self.page.locator(self.NAV_LINKS).all_inner_texts()

    def fill_contact_form(self, name: str, phone: str, service: str = ""):
        self.scroll_to("kontakt")
        self.page.wait_for_timeout(500)
        if name:
            self.page.fill(self.FIELD_NAME, name)
        if phone:
            self.page.fill(self.FIELD_PHONE, phone)
        if service:
            self.page.select_option(self.SELECT_SERVICE, label=service)

    def submit_contact_form(self):
        self.page.locator(self.BTN_SUBMIT).click()

    def is_section_visible(self, section_id: str) -> bool:
        return self.page.locator(f"#{section_id}").is_visible()


class KoparkaBlogPage(BasePage):
    BLOG_URL       = f"{BASE_URL}/blog/"
    BLOG_CARDS     = ".blog-card"
    BLOG_CARD_LINK = ".blog-card-link"
    BREADCRUMB     = ".breadcrumb"
    PAGE_H1        = ".page-h1"

    def open(self):
        self.navigate(self.BLOG_URL)

    def get_article_count(self) -> int:
        return self.page.locator(self.BLOG_CARDS).count()

    def open_first_article(self):
        self.page.locator(self.BLOG_CARD_LINK).first.click()
        self.page.wait_for_load_state("domcontentloaded")


class KoparkaCrmPage(BasePage):
    CRM_LOGIN_URL = f"{BASE_URL}/crm/login.php"
    CRM_PANEL_URL = f"{BASE_URL}/crm/"

    PWD_INPUT   = "input[name='password']"
    BTN_LOGIN   = "button[type='submit']"
    ERROR_MSG   = ".error"
    PAGE_TITLE  = "h1"

    def open_login(self):
        self.navigate(self.CRM_LOGIN_URL)

    def login(self, password: str):
        self.page.fill(self.PWD_INPUT, password)
        self.page.locator(self.BTN_LOGIN).click()
        self.page.wait_for_load_state("domcontentloaded")

    def is_error_visible(self) -> bool:
        return self.page.locator(self.ERROR_MSG).is_visible()

    def get_error_text(self) -> str:
        return self.page.locator(self.ERROR_MSG).inner_text()

    def is_logged_in(self) -> bool:
        return "/crm/login" not in self.page.url

    def logout(self):
        self.page.goto(f"{BASE_URL}/crm/?logout=1")
        self.page.wait_for_load_state("domcontentloaded")
