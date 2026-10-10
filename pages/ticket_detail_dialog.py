from pathlib import Path

from playwright.sync_api import Page

from pages.base_page import BasePage


class TicketDetailDialog(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dialog = page.get_by_role("dialog", name="チケット詳細")

        # input file bị ẩn (display:none) → dùng set_input_files, KHÔNG click dropzone
        self.file_input = page.locator("#detail_file_input")
        self.file_preview = page.locator("#detail_file_preview")
        self.file_name = page.locator("#detail_file_name")
        self.remove_file_button = self.dialog.get_by_role("button", name="ファイルを削除")
        self.file_error = page.locator("#detail_file_error")

    def upload_file(self, file_path: Path) -> None:
        self.file_input.set_input_files(str(file_path))