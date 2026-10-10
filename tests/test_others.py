import allure
import pytest
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage

VIEWPORTS = [(1920, 1080), (1366, 768), (1024, 768), (768, 1024)]


@allure.feature("Others")
class TestOthers:

    @allure.title("Others_01: 画面サイズ {width}x{height} のレイアウト確認")
    @pytest.mark.parametrize("width, height", VIEWPORTS, ids=[f"{w}x{h}" for w, h in VIEWPORTS])
    def test_others_01_layout_on_screen_sizes(self, admin_page: TicketListPage, width, height):
        with allure.step(f"1. 画面サイズを {width}x{height} に変更する"):
            admin_page.page.set_viewport_size({"width": width, "height": height})

        with allure.step("期待: 画面が横にはみ出さない（横スクロールなし）"):
            assert not admin_page.has_horizontal_scroll(), f"{width}x{height} で横スクロールが発生"

        with allure.step("2. 期待: 重要なUI要素が表示され、画面外にはみ出さない"):
            for name, locator in admin_page.key_elements().items():
                expect(locator).to_be_visible()
                assert admin_page.is_inside_viewport(locator), f"{name} が画面外にはみ出している（{width}x{height}）"