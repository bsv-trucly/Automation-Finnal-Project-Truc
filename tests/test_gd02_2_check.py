import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage


@allure.feature("GD02.2-Check")
class TestGD02_2_Check:

    @allure.title("GD02.2-001: 全選択チェックボックス")
    def test_gd02_2_001_select_all(self, admin_page: TicketListPage):
        row_count = admin_page.rows.count()

        with allure.step("前提: 全選択はOFF、一括操作バーは非表示"):
            expect(admin_page.select_all_checkbox).not_to_be_checked()
            expect(admin_page.bulk_action_bar).to_be_hidden()

        with allure.step("1. テーブルヘッダーの全選択チェックボックスを押下する"):
            admin_page.check_select_all()

        with allure.step(f"期待: 表示中の全行（{row_count}件）のチェックボックスがチェックされる"):
            for ticket_id in admin_page.visible_ids():
                expect(admin_page.row_checkbox(ticket_id)).to_be_checked()

        with allure.step("期待: 一括操作バーが表示される"):
            expect(admin_page.bulk_action_bar).to_be_visible()
            expect(admin_page.selected_count).to_have_text(f"{row_count}件選択中")