import time

import allure
from playwright.sync_api import expect

from pages.notification_page import NotificationPage
from pages.ticket_list_page import TicketListPage


@allure.feature("GD02.1-Click")
class TestGD02_1_Click:

    @allure.title("GD02.1-01: 検索結果0件→作成導線（get-or-create）")
    def test_gd02_1_01_get_or_create(self, admin_page: TicketListPage):
        notif = NotificationPage(admin_page.page)
        # Tiêu đề kèm thời gian → mỗi lần chạy là một tiêu đề chưa tồn tại
        title = f"自動テスト通知_{int(time.time())}"

        with allure.step("前提: 通知一覧画面を表示"):
            notif.open_tab("通知")
            expect(notif.panel).to_be_visible()

        with allure.step("1. 存在しないキーワードで検索する"):
            notif.search(title)
            expect(notif.rows).to_have_count(0)
            expect(notif.empty_message).to_contain_text("検索条件に一致する通知が見つかりません")

        with allure.step("2. メッセージの下の「＋通知を作成する」を押下する"):
            notif.create_button_in_empty.click()

        with allure.step("期待: 通知作成モーダルが開く"):
            expect(notif.modal).to_be_visible()
            expect(notif.title_input).to_be_empty()

        with allure.step("補足: get-or-create を ensure_notification_exists() で実行"):
            notif.cancel_button.click()
            created_first = notif.ensure_notification_exists(title, "自動テストで作成した通知です")
            notif.expect_toast("通知を作成しました。")
            created_second = notif.ensure_notification_exists(title, "自動テストで作成した通知です")

        with allure.step("期待: 1回目は作成、2回目は既存なので作成しない（重複なし）"):
            assert created_first is True
            assert created_second is False
            expect(notif.row_by_title(title)).to_have_count(1)