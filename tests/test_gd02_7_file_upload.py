import allure
from playwright.sync_api import expect

from pages.ticket_detail_dialog import TicketDetailDialog
from pages.ticket_list_page import TicketListPage


@allure.feature("GD02.7-FileUpload")
class TestGD02_7_FileUpload:

    @allure.title("GD02.7-01: ファイルアップロード（正常）")
    def test_gd02_7_01_upload_png(self, admin_page: TicketListPage, tmp_path):
        # Tạo file .png khoảng 1MB ngay lúc chạy test
        png_file = tmp_path / "sample_1mb.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * (1024 * 1024 - 8))

        detail = TicketDetailDialog(admin_page.page)

        with allure.step("前提: 任意の行の「詳細」ボタンを押下し、詳細ダイアログを表示"):
            admin_page.click_detail(admin_page.visible_ids()[0])
            expect(detail.dialog).to_be_visible()
            expect(detail.file_preview).to_be_hidden()

        with allure.step("1. ドロップゾーンに.pngファイル（1MB程度）をアップロードする"):
            detail.upload_file(png_file)

        with allure.step("期待: ファイル名とサイズがプレビュー表示される"):
            expect(detail.file_preview).to_be_visible()
            expect(detail.file_name).to_have_text("sample_1mb.png（1024KB）")

        with allure.step("期待: 削除アイコンが表示され、エラーは出ない"):
            expect(detail.remove_file_button).to_be_visible()
            expect(detail.file_error).to_be_hidden()