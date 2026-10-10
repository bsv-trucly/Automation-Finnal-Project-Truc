import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.ticket_list_page import TicketListPage     
from test_data.accounts import ADMIN

expect.set_options(timeout=5000)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def admin_page(login_page: LoginPage) -> TicketListPage:   
    login_page.login(ADMIN["id"], ADMIN["password"])
    expect(login_page.header_username).to_have_text(ADMIN["name"])
    return TicketListPage(login_page.page)                