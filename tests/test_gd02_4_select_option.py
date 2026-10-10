import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage, COL_PRIORITY


@allure.feature("GD02.4-SelectOption")
class TestGD02_4_SelectOption:

    @allure.title("GD02.4-02: 優先度絞り込み（高）")
    def test_gd02_4_02_filter_by_priority_high(self, admin_page: TicketListPage):
        with allure.step("1. 優先度プルダウンで「高」を選択する"):
            admin_page.select_priority("高")

        with allure.step("期待: プルダウンの値が「高」になる"):
            expect(admin_page.priority_select).to_have_value("高")

        with allure.step("期待: 優先度が「高」のチケットのみ表示される（5件）"):
            expect(admin_page.rows).to_have_count(5)
            assert set(admin_page.column_values(COL_PRIORITY)) == {"高"}