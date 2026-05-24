from pages.base_page import BasePage
import time

BASE_URL     = "https://www.dbcraftmode.pl"
ADMIN_EMAIL  = "daniel@dbcraftmode.pl"
ADMIN_PASS   = "admin123"          # zmień jeśli hasło produkcyjne inne


class DBCraftLoginPage(BasePage):
    URL           = f"{BASE_URL}/admin/"
    EMAIL_INPUT   = "input[name='email']"
    PASS_INPUT    = "input[name='password']"
    BTN_SUBMIT    = "button.btn-login"
    ERROR_BOX     = ".error-box"
    LOGO_ICON     = ".login-logo-icon"

    def open(self):
        self.navigate(self.URL)

    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASS_INPUT, password)
        self.page.locator(self.BTN_SUBMIT).click()
        self.page.wait_for_load_state("domcontentloaded")

    def is_error_visible(self) -> bool:
        return self.page.locator(self.ERROR_BOX).is_visible()

    def get_error_text(self) -> str:
        return self.page.locator(self.ERROR_BOX).inner_text().strip()

    def is_logged_in(self) -> bool:
        return "dashboard" in self.page.url or "/admin/" in self.page.url and "index" not in self.page.url


class DBCraftDashboard(BasePage):
    URL           = f"{BASE_URL}/admin/dashboard.php"
    SIDEBAR       = ".sidebar"
    SIDEBAR_LINKS = ".sidebar-link"
    STATS_CARDS   = ".stat-card, .stats-grid, .dash-stat"
    FLASH_MSG     = ".flash, .flash-success, .alert-success"

    def open(self):
        self.navigate(self.URL)

    def get_sidebar_links(self) -> list[str]:
        return self.page.locator(self.SIDEBAR_LINKS).all_inner_texts()

    def is_sidebar_visible(self) -> bool:
        return self.page.locator(self.SIDEBAR).is_visible()


class DBCraftBlogPage(BasePage):
    LIST_URL     = f"{BASE_URL}/admin/blog.php"
    ADD_URL      = f"{BASE_URL}/admin/blog-add.php"

    # Lista wpisów
    TABLE_ROWS   = "table tbody tr, .blog-row, .post-row"
    BTN_ADD_NEW  = "a[href*='blog-add']"

    # Formularz dodawania
    TITLE_INPUT   = "input[name='title']"
    CONTENT_AREA  = "textarea[name='content'], #content"
    STATUS_SELECT = "select[name='status']"
    BTN_SAVE      = "button[type='submit']"
    ERROR_LIST    = ".error-list, .errors, .alert-danger"
    FLASH_SUCCESS = ".flash, .flash-success"

    def open_list(self):
        self.navigate(self.LIST_URL)

    def open_add_form(self):
        self.navigate(self.ADD_URL)

    def fill_post(self, title: str, content: str, status: str = "draft"):
        self.page.fill(self.TITLE_INPUT, title)
        # content może być textarea lub rich editor
        if self.page.locator("textarea[name='content']").count() > 0:
            self.page.fill("textarea[name='content']", content)
        else:
            # rich editor — wpisz tekst przez evaluate
            self.page.evaluate(
                "document.querySelector('#content, [name=\"content\"]').value = arguments[0]",
                content
            )
        if self.page.locator(self.STATUS_SELECT).count() > 0:
            self.page.select_option(self.STATUS_SELECT, value=status)

    def save_post(self):
        self.page.locator(self.BTN_SAVE).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def post_exists_in_list(self, title: str) -> bool:
        self.open_list()
        return self.page.locator(f"text={title}").count() > 0


class DBCraftIdeasPage(BasePage):
    LIST_URL     = f"{BASE_URL}/admin/ideas.php"
    ADD_URL      = f"{BASE_URL}/admin/idea-add.php"

    TITLE_INPUT   = "input[name='title']"
    CONCEPT_AREA  = "textarea[name='concept']"
    BTN_SAVE      = "button[type='submit']"

    def open_list(self):
        self.navigate(self.LIST_URL)

    def open_add_form(self):
        self.navigate(self.ADD_URL)

    def fill_idea(self, title: str, concept: str):
        self.page.fill(self.TITLE_INPUT, title)
        self.page.fill(self.CONCEPT_AREA, concept)

    def save_idea(self):
        self.page.locator(self.BTN_SAVE).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def idea_exists_in_list(self, title: str) -> bool:
        self.open_list()
        return self.page.locator(f"text={title}").count() > 0


class DBCraftProjectsPage(BasePage):
    LIST_URL    = f"{BASE_URL}/admin/projects.php"
    ADD_URL     = f"{BASE_URL}/admin/project-add.php"

    TABLE_ROWS  = "table tbody tr, .project-row"
    BTN_ADD_NEW = "a[href*='project-add']"

    def open_list(self):
        self.navigate(self.LIST_URL)

    def get_project_count(self) -> int:
        return self.page.locator(self.TABLE_ROWS).count()
