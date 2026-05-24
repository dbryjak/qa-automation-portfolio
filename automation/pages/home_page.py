from pages.base_page import BasePage

BASE_URL = "https://www.saucedemo.com"


class HomePage(BasePage):
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    PAGE_TITLE = ".title"

    def open(self):
        self.navigate(BASE_URL)

    def logout(self):
        self.page.locator(self.MENU_BUTTON).click()
        self.page.locator(self.LOGOUT_LINK).wait_for(state="visible")
        self.page.locator(self.LOGOUT_LINK).click()

    def is_logged_in(self) -> bool:
        return self.page.locator(self.PAGE_TITLE).is_visible()

    def get_page_title(self) -> str:
        return self.page.locator(self.PAGE_TITLE).inner_text()
