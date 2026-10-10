from playwright.sync_api import Page, Locator

from pages.base_page import BasePage

# Thứ tự cột trong bảng (bắt đầu từ 0)
COL_ID, COL_SUBJECT, COL_PRIORITY, COL_STATUS, COL_ASSIGNEE, COL_CREATED = 1, 2, 3, 4, 5, 6


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

        # ---- Bảng ----
        self.rows = page.locator("#ticket_tbody tr[data-id]")
        # <th> 作成日 bị Chromium nhận role "cell" (không phải columnheader) → dùng id
        self.created_header = page.locator("#th_created")
        self.sort_icon = page.locator("#sort_icon")
        self.created_help_icon = self.created_header.locator(".tooltip-wrap")
        self.created_tooltip = self.created_header.locator(".tooltip-content")
        # input thật (opacity:0) – check() trực tiếp vào đây, không click .cb-box        # ← mới
        self.select_all_checkbox = page.get_by_role("checkbox", name="全て選択")          # ← mới

        # ---- Thanh thao tác hàng loạt ----                                            # ← mới
        self.bulk_action_bar = page.locator("#bulk_action_bar")                          # ← mới
        self.selected_count = page.locator("#selected_count")                            # ← mới

        # ---- iframe 埋め込みプレビュー ----                                           # ← mới
        self.preview_frame = page.frame_locator("#preview_iframe")
        self.frame_status_select = self.preview_frame.get_by_role("combobox")
        self.frame_apply_button = self.preview_frame.get_by_role("button", name="適用")
        self.frame_result = self.preview_frame.locator("#frame_result")

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

    # ---------- Bộ lọc ----------
    def select_priority(self, priority: str) -> None:
        """priority: '' (全て) / 高 / 中 / 低"""
        self.priority_select.select_option(priority)

    # ---------- Sort / Tooltip ----------
    def click_created_header(self) -> None:
        self.created_header.click()

    def hover_created_help_icon(self) -> None:
        self.created_help_icon.hover()

    # ---------- Đọc dữ liệu bảng ----------
    def column_values(self, col_index: int) -> list[str]:
        """Lấy text của 1 cột ở tất cả các hàng đang hiển thị"""
        cells = self.rows.locator(f"td:nth-child({col_index + 1})")
        return [text.strip() for text in cells.all_inner_texts()]

    def visible_ids(self) -> list[str]:
        """Danh sách ID ticket đang hiển thị, ví dụ ['T-1001', 'T-1002', ...]"""
        return self.column_values(COL_ID)

    def row_by_id(self, ticket_id: str) -> Locator:
        """Hàng của 1 ticket cụ thể (mỗi <tr> có data-id = ID ticket)"""
        return self.page.locator(f"#ticket_tbody tr[data-id='{ticket_id}']")

    # ---------- Checkbox ----------                                                     # ← mới
    def row_checkbox(self, ticket_id: str) -> Locator:                                   # ← mới
        """Checkbox của 1 hàng – aria-label dạng 'T-1001を選択'"""
        return self.page.get_by_role("checkbox", name=f"{ticket_id}を選択")

    def check_select_all(self) -> None:                                                  # ← mới
        self.select_all_checkbox.check()

        # ---------- Thao tác trên hàng ----------
    def click_detail(self, ticket_id: str) -> None:                                      # ← mới
        self.row_by_id(ticket_id).get_by_role("button", name="詳細", exact=True).click()

    def click_delete(self, ticket_id: str) -> None:
        self.row_by_id(ticket_id).get_by_role("button", name="削除", exact=True).click()

    # ---------- Thao tác trên hàng ----------
    def click_delete(self, ticket_id: str) -> None:
        self.row_by_id(ticket_id).get_by_role("button", name="削除", exact=True).click()

            # ---------- iframe ----------                                                       # ← mới
    def apply_status_in_preview(self, status: str) -> None:
        self.frame_status_select.select_option(status)
        self.frame_apply_button.click()