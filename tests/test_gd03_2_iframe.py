import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage, COL_STATUS


@allure.feature("GD03.2-Iframe")
class TestGD03_2_Iframe:

    @allure.title("GD03.2-01: iframe内操作")
    def test_gd03_2_01_apply_status_in_iframe(self, admin_page: TicketListPage):
        statuses_before = admin_page.column_values(COL_STATUS)

        with allure.step("前提: iframe内の結果メッセージは空"):
            expect(admin_page.frame_result).to_have_text("")

        with allure.step("1. 埋め込みプレビュー内のプルダウンで「対応中」を選択する"):
            admin_page.frame_status_select.select_option("対応中")

        with allure.step("2. 埋め込みプレビュー内の「適用」ボタンを押下する"):
            admin_page.frame_apply_button.click()

        with allure.step("期待: iframe内に結果メッセージが表示される"):
            expect(admin_page.frame_result).to_have_text(
                "プレビューを 対応中 に更新しました（画面外には反映されません）"
            )

        with allure.step("期待: 親ページの一覧には影響しない"):
            statuses_after = admin_page.column_values(COL_STATUS)
            assert statuses_after == statuses_before, f"一覧が変わった: {statuses_before} → {statuses_after}"