from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class NotificationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.panel = page.locator("#panel_notifications")
        self.search_input = page.get_by_role("textbox", name="タイトルまたは内容で検索")
        self.search_button = self.panel.get_by_role("button", name="検索", exact=True)
        self.rows = page.locator("#notification_tbody tr[data-id]")
        self.empty_message = page.locator("#notification_tbody td div")
        self.create_button_in_empty = page.get_by_role("button", name="＋通知を作成する", exact=True)

        # ---- Modal tạo mới ----
        self.modal = page.get_by_role("dialog", name="通知を作成")
        self.title_input = self.modal.get_by_label("タイトル")
        self.content_input = self.modal.get_by_label("内容")
        self.submit_button = self.modal.get_by_role("button", name="作成する")
        self.cancel_button = self.modal.get_by_role("button", name="キャンセル")

    def search(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        self.search_button.click()

    def row_by_title(self, title: str) -> Locator:
        # Chỉ so khớp ô タイトル (cột 2), tránh khớp nhầm với ô 内容
        return self.rows.filter(has=self.page.locator("td:nth-child(2)", has_text=title))

    def create_notification(self, title: str, content: str) -> None:
        self.title_input.fill(title)
        self.content_input.fill(content)
        self.submit_button.click()

    def ensure_notification_exists(self, title: str, content: str) -> bool:
        """get-or-create: True = vừa tạo mới, False = đã có sẵn"""
        self.search(title)
        # Chờ bảng render xong: có hàng dữ liệu HOẶC có nút tạo mới
        self.rows.first.or_(self.create_button_in_empty).wait_for()
        if self.row_by_title(title).count() > 0:
            return False
        self.create_button_in_empty.click()
        self.create_notification(title, content)
        return True