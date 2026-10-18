import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.ticket_list_page import TicketListPage
from test_data.accounts import ADMIN


@allure.feature("GD02.3-Fill")
class TestGD02_3_Fill:

    @allure.title("GD02.3-007: 正常系ログイン")
    def test_gd02_3_007_valid_login(self, login_page: LoginPage):
        with allure.step("前提: ログイン画面を表示中（ログインボタンは非活性）"):
            expect(login_page.login_section).to_be_visible()
            expect(login_page.login_button).to_be_disabled()

        with allure.step(f"1. IDに「{ADMIN['id']}」を入力する"):
            login_page.id_input.fill(ADMIN["id"])
            expect(login_page.id_input).to_have_value(ADMIN["id"])

        with allure.step("2. パスワードに「admin123」を入力する"):
            login_page.password_input.fill(ADMIN["password"])
            expect(login_page.password_input).to_have_value(ADMIN["password"])

        with allure.step("3. 「ログイン」ボタンを押下する"):
            expect(login_page.login_button).to_be_enabled()
            login_page.login_button.click()
            ###NNTT: việc login thành công để truy cập vào màn hình được tái sử dụng ở nhiều testcase do đó nên define riêng thành @pytest.fixture (access_to_login_page)để tái sử dụng. 

        ticket_list = TicketListPage(login_page.page)

        with allure.step("期待: チケット一覧画面に遷移する"):
            expect(login_page.login_section).to_be_hidden()
            expect(ticket_list.panel).to_be_visible()

        with allure.step("期待: ヘッダーにログインユーザー名が表示される"):
            expect(ticket_list.header_username).to_have_text(ADMIN["name"])