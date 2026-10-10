import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage


@allure.feature("GD03.3-TabWindow")
class TestGD03_3_TabWindow:

    @allure.title("GD03.3-01: 別ウィンドウで開く")
    def test_gd03_3_01_open_print_preview_window(self, admin_page: TicketListPage):
        total = admin_page.total_count()

        with allure.step("1. 「印刷プレビューを開く（新しいウィンドウ）」ボタンを押下する"):
            with admin_page.page.expect_popup() as popup_info:
                admin_page.print_preview_button.click()
            popup = popup_info.value

        with allure.step("期待: 新しいポップアップウィンドウが開く"):
            expect(popup.get_by_role("heading", name="印刷プレビュー")).to_be_visible()

        with allure.step(f"期待: 印刷プレビュー内容（対象チケット数：{total}件）が表示される"):
            expect(popup.get_by_text("対象チケット数：")).to_have_text(f"対象チケット数：{total}件")

        popup.close()