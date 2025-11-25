import os
import time

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions
from faker import Faker

from clients.spends_client import SpendsHttpClient
from pages.auth_reg_page import AuthRegistrationPage


faker = Faker()
auth_page = AuthRegistrationPage()


@pytest.fixture(scope='session')
def envs():
    load_dotenv()


@pytest.fixture(scope='session')
def auth_url(envs):
    return os.getenv('AUTH_URL')


@pytest.fixture(scope='session')
def frontend_url(envs):
    return os.getenv('FRONTEND_URL')


@pytest.fixture(scope='session')
def gateway_url(envs):
    return os.getenv('GATEWAY_URL')


@pytest.fixture(scope='session')
def existed_user_credentials(envs):
    return {
        'username': os.getenv('TEST_USERNAME'),
        'password': os.getenv('TEST_PASSWORD'),
    }


@pytest.fixture(scope='session')
def browser_setup(auth_url):
    options = ChromeOptions()
    prefs = {
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option('prefs', prefs)
    browser.config.driver_options = options
    browser.config.base_url = auth_url
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
    auth_page.open_auth_page()
    auth_page.fill_username(existed_user_credentials.get('username'))
    auth_page.fill_password(existed_user_credentials.get('password'))
    auth_page.login_btn.click()
    time.sleep(1)
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(login, gateway_url) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, login)


@pytest.fixture(params=[])
def category(request, spends_client: SpendsHttpClient):
    category = request.param
    categories = spends_client.get_categories()
    if category not in [category['name'] for category in categories]:
        spends_client.add_category(category)
    return category


@pytest.fixture()
def auth_page_():
    browser.open('/login')


@pytest.fixture()
def registration_page():
    browser.open('/register')


class Auth:
    login = pytest.mark.usefixtures('login')


class Pages:
    auth = pytest.mark.usefixtures('auth_page_')
    registration = pytest.mark.usefixtures('registration_page')


@pytest.fixture(params=[])
def spends(request, spends_client: SpendsHttpClient):
    response = spends_client.add_spends(request.param)
    yield response
    spends_client.remove_spends([response['id']])


class TestData:
    category = lambda x: pytest.mark.parametrize('category', [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize('spends', [x], indirect=True)