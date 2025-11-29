import os
import time

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions
from faker import Faker

from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from pages.auth_reg_page import AuthRegistrationPage
from models.config import Envs


faker = Faker()
auth_page = AuthRegistrationPage()


@pytest.fixture(scope='session')
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv('FRONTEND_URL'),
        gateway_url=os.getenv('GATEWAY_URL'),
        spends_db_url=os.getenv('SPEND_DB_URL'),
        test_username=os.getenv('TEST_USERNAME'),
        test_password=os.getenv('TEST_PASSWORD'),
        auth_url=os.getenv('AUTH_URL'),
    )


@pytest.fixture(scope='session')
def existed_user_credentials(envs):
    return {
        'username': envs.test_username,
        'password': envs.test_password,
    }


@pytest.fixture(scope='session')
def browser_setup(envs):
    options = ChromeOptions()
    prefs = {
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option('prefs', prefs)
    browser.config.driver_options = options
    browser.config.base_url = envs.frontend_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open('/')
    yield
    browser.quit()


@pytest.fixture(scope='function')
def generate_user_data():
    return {
        'username': faker.user_name(),
        'password': faker.password(length=8),
        'submit_pass': faker.password(length=8),
    }


@pytest.fixture(scope='session')
def login(existed_user_credentials, browser_setup):
    auth_page.fill_username(existed_user_credentials.get('username'))
    auth_page.fill_password(existed_user_credentials.get('password'))
    auth_page.login_btn.click()
    time.sleep(1)
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spends_db_url)


@pytest.fixture(scope='session')
def spends_client(login, envs) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, login)


@pytest.fixture(params=[])
def category(request, spends_client: SpendsHttpClient, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture()
def auth_page_(browser_setup):
    browser.open()


@pytest.fixture()
def registration_page(envs):
    browser.open(f'{envs.auth_url}/register')


@pytest.fixture()
def main_page(browser_setup):
    browser.open('/main')


class Auth:
    login = pytest.mark.usefixtures('login')


class Pages:
    auth = pytest.mark.usefixtures('auth_page_')
    registration = pytest.mark.usefixtures('registration_page')
    main = pytest.mark.usefixtures('main_page')


@pytest.fixture(params=[])
def spends(request, spends_client: SpendsHttpClient, spend_db):
    response = spends_client.add_spends(request.param)
    yield response
    all_spends = spends_client.get_spends()
    all_categories = spends_client.get_categories()
    if response.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([response.id])
    if response.category.id in [category.id for category in all_categories]:
        spend_db.delete_category(category_id=response.category.id)


class TestData:
    category = lambda x: pytest.mark.parametrize('category', [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize('spends', [x], indirect=True, ids=lambda param: param.description)