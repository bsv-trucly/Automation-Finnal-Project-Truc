from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.nav_tabs = page.locator("#nav_tabs")
        self.header_username = page.locator("#header_username")
        self.toasts = page.locator("#toast_container .toast")

    def open_tab(self, tab_name: str) -> None:
        self.nav_tabs.get_by_text(tab_name, exact=True).click()

    def expect_toast(self, text: str) -> None:
        expect(self.toasts.filter(has_text=text)).to_be_visible()

    def is_inside_viewport(self, locator) -> bool:
        """Phần tử có nằm trọn trong chiều ngang màn hình không"""
        box = locator.bounding_box()
        width = self.page.viewport_size["width"]
        return box is not None and box["x"] >= 0 and box["x"] + box["width"] <= width

    def has_horizontal_scroll(self) -> bool:
        """Trang có bị tràn ngang (xuất hiện thanh cuộn ngang) không"""
        return self.page.evaluate("document.documentElement.scrollWidth > window.innerWidth")