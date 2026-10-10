from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class TicketListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.panel = page.locator("#panel_tickets")

        self.header = page.locator("#app_header")
        self.user_menu_button = page.locator("#user_menu_activator")
        self.new_ticket_button = page.get_by_role("button", name="新規チケット作成")
        self.search_input = page.get_by_role("textbox", name="件名または担当者で検索")
        self.search_button = self.panel.get_by_role("button", name="検索", exact=True)
        self.priority_select = page.get_by_role("combobox", name="優先度で絞り込み")
        self.table_wrap = self.panel.locator(".table-wrap")

        # ---- Phân trang ----
        self.pagination_summary = page.locator("#pagination_summary_top")             

        # ---- Link mở cửa sổ / tab mới ----
        self.print_preview_button = page.get_by_role(                               
            "button", name="印刷プレビューを開く（新しいウィンドウ）")

    def key_elements(self) -> dict[str, Locator]:
        """Các phần tử UI quan trọng cần kiểm tra layout"""
        return {
            "ヘッダー": self.header,
            "ユーザーメニュー": self.user_menu_button,
            "新規チケット作成": self.new_ticket_button,
            "検索欄": self.search_input,
            "検索ボタン": self.search_button,
            "優先度プルダウン": self.priority_select,
            "テーブル": self.table_wrap,
        }

    def total_count(self) -> int:                                                     
        """Tổng số ticket, đọc từ dòng "12件中 1 - 10件目" """
        summary = self.pagination_summary.inner_text()
        return int(summary.split("件中")[0])