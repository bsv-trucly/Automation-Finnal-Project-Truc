import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage


@allure.feature("GD02.5-Hover")
class TestGD02_5_Hover:

    @allure.title("GD02.5-001: ツールチップ表示")
    def test_gd02_5_001_created_tooltip(self, admin_page: TicketListPage):
        with allure.step("前提: ツールチップは非表示"):
            expect(admin_page.created_tooltip).to_be_hidden()

        with allure.step("1. 「作成日」列見出し横のヘルプアイコン（?）にカーソルを合わせる"):
            admin_page.hover_created_help_icon()

        with allure.step("期待: 説明テキストが表示される"):
            expect(admin_page.created_tooltip).to_be_visible()
            expect(admin_page.created_tooltip).to_have_text("チケットが作成された日付を表示します")