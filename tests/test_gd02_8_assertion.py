import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage


@allure.feature("GD02.8-Assertion")
class TestGD02_8_Assertion:

    @allure.title("GD02.8-04: 異常系ログイン")
    def test_gd02_8_04_invalid_login(self, login_page: LoginPage):
        with allure.step("1. IDに「admin」を入力する"):
            login_page.id_input.fill("admin")

        with allure.step("2. パスワードに「wrongpass」を入力する"):
            login_page.password_input.fill("wrongpass")
            ###NNTT: nên tạo và tái sử dụng hàm @pytest.fixture (access_to_login_page) , đối với data input này nên define ở file test_data.py 
        with allure.step("3. 「ログイン」ボタンを押下する"):
            login_page.login_button.click()

        with allure.step("期待: エラーメッセージが表示される"):
            expect(login_page.error_message).to_be_visible()
            expect(login_page.error_message).to_have_text("IDまたはパスワードが正しくありません。")

        with allure.step("期待: 画面遷移しない（ログイン画面のまま）"):
            expect(login_page.login_section).to_be_visible()
            expect(login_page.main_section).to_be_hidden()