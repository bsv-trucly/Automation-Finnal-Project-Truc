from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_section = page.locator("#login_section")
        self.main_section = page.locator("#main_section")
        self.id_input = page.get_by_label("ID", exact=True)
        self.password_input = page.get_by_label("パスワード", exact=True)
        self.login_button = page.get_by_role("button", name="ログイン", exact=True)
        self.error_message = page.locator("#login_error")

    def open(self) -> None:
        self.page.goto("bai_tap_17082026.html")

    def login(self, user_id: str, password: str) -> None:
        self.id_input.fill(user_id)
        self.password_input.fill(password)
        self.login_button.click()