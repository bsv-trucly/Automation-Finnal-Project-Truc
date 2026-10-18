import re

import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage


@allure.feature("GD01-Navigation")
class TestGD01_Navigation:

    @allure.title("GD01_003: 遷移画面（チケット一覧）")
    def test_gd01_003_ticket_list_after_login(self, admin_page: TicketListPage):
        with allure.step("期待: チケット一覧画面が表示される"):
        ###NNTT: thay vì allure.step nằm ở trong từng testcase thì nên đưa vào folder pages để đảm bảo tính POM và có thể tái sử dụng. 
            expect(admin_page.panel).to_be_visible()

        with allure.step("期待: 「チケット一覧」タブがアクティブ"):
            expect(admin_page.nav_tab("チケット一覧")).to_have_class(re.compile(r"nav-tab--active"))
        ###NNTT: đối với expect có chứa các locator "nav-tab--active" tốt nhất nên define riêng ở file locators.py, ở folder tests nên đảm bảo chỉ chứa những testcase clear. 
        with allure.step("期待: 他のタブはアクティブではない"):
            for other in ["通知", "統計", "設定"]:
                expect(admin_page.nav_tab(other)).not_to_have_class(re.compile(r"nav-tab--active"))

        with allure.step("期待: 10件のチケットが表示される"):
            expect(admin_page.rows).to_have_count(10)