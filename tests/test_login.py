import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage


@allure.feature("ログイン画面")
class Testログイン画面:

    @allure.title("ログイン画面-004: 異常系ログイン")
    def test_login_004_invalid_password(self, login_page: LoginPage):
        with allure.step("1-3. admin / wrongpass でログイン"):
            login_page.login("admin", "wrongpass")

        with allure.step("期待: エラーメッセージが表示され、画面遷移しない"):
            expect(login_page.error_message).to_have_text("IDまたはパスワードが正しくありません。")
            expect(login_page.login_section).to_be_visible()
            expect(login_page.main_section).to_be_hidden()