from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        error = self.page.locator(self.ERROR_MESSAGE)
        error.wait_for(state="visible", timeout=5000)
        return error.inner_text().strip()

    def is_error_visible(self) -> bool:
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
