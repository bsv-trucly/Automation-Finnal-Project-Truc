import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage, COL_SUBJECT, COL_ASSIGNEE

KEYWORD = "ログイン"
###NNTT: đối với các keyword data test để dễ tracking quản lý nên gom lại để ở test_data thay vì trong riêng lẻ từng file testcase. 


@allure.feature("GD02.6-Keyboard")
class TestGD02_6_Keyboard:

    @allure.title("GD02.6-02: キーワード検索（Enterキー）")
    def test_gd02_6_02_search_by_enter_key(self, admin_page: TicketListPage):
        total = admin_page.total_count()

        with allure.step(f"比較用: 「検索」ボタンで「{KEYWORD}」を検索した結果を記録"):
            admin_page.search_by_button(KEYWORD)
            expect(admin_page.rows).not_to_have_count(total)
            ids_by_button = admin_page.visible_ids()

        with allure.step("検索条件をクリアして全件表示に戻す"):
            admin_page.search_by_button("")
            expect(admin_page.pagination_summary).to_contain_text(f"{total}件中")

        with allure.step(f"1. 検索欄に「{KEYWORD}」と入力する / 2. Enterキーを押下する"):
            admin_page.search_by_enter(KEYWORD)

        with allure.step("期待: 「検索」ボタン押下時と同じ結果が表示される"):
            expect(admin_page.rows).to_have_count(len(ids_by_button))
            ids_by_enter = admin_page.visible_ids()
            assert ids_by_enter == ids_by_button, f"結果が異なる: ボタン={ids_by_button} / Enter={ids_by_enter}"

        with allure.step(f"補足: 表示された全行の件名または担当者に「{KEYWORD}」が含まれる"):
            subjects = admin_page.column_values(COL_SUBJECT)
            assignees = admin_page.column_values(COL_ASSIGNEE)
            for subject, assignee in zip(subjects, assignees):
                assert KEYWORD in subject + assignee, f"「{KEYWORD}」を含まない行: {subject} / {assignee}"