import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage


@allure.feature("GD03.1-Dialog")
class TestGD03_1_Dialog:

    @allure.title("GD03.1-01: チケット削除（確認ダイアログ→OK）")
    def test_gd03_1_01_delete_ticket_confirm_ok(self, admin_page: TicketListPage):
        target_id = admin_page.visible_ids()[0]
        dialog_messages = []

        def accept_confirm(dialog):
            dialog_messages.append((dialog.type, dialog.message))
            dialog.accept()

        with allure.step(f"前提: 削除対象 {target_id} が一覧に存在する"):
            expect(admin_page.row_by_id(target_id)).to_have_count(1)

        with allure.step(f"1. {target_id} の「削除」ボタンを押下する / 2. 確認ダイアログで「OK」"):
            admin_page.page.once("dialog", accept_confirm)
            admin_page.click_delete(target_id)

        with allure.step("期待: 確認ダイアログ（confirm）が表示された"):
            assert dialog_messages == [("confirm", "このチケットを削除します。よろしいですか？")]

        with allure.step("期待: 該当行が一覧から削除される"):
            expect(admin_page.row_by_id(target_id)).to_have_count(0)

        with allure.step("期待: トースト「チケットを削除しました。」が表示される"):
            admin_page.expect_toast("チケットを削除しました。")