from unicodedata import category

from selene import browser, by, have, be
from pages.spendings_page import SpendingPage

spending_page = SpendingPage()

class ProfilePage:

    def __init__(self):
        self.profile_dd_btn = browser.element('a[href="/profile"]')
        self.save_changes_btn = browser.element('button[type="submit"]')
        self.name = browser.element('#name')
        self.alert = browser.element('div[role="alert"] div:nth-child(2)')
        self.profile_text = browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3')
        self.category = browser.element('#category')
        self.error_text = browser.element('.input__helper-text')
        self.archive_checkbox = browser.element('input[class*="PrivateSwitchBase-input"]')
        self.archive_checkbox_checked = browser.element('span[class*="Mui-checked"]')
        self.archive_ask_btn = browser.element('//button[contains(text(), "Archive")]')
        self.unarchive_btn = browser.all('button[aria-label="Unarchive category"]').first
        self.unarchive_ask_btn = browser.element('//button[contains(text(), "Unarchive")]')
        self.update_category_input = browser.element('input[placeholder="Edit category"]')


    def open_profile_page(self):
        spending_page.avatar_btn.click()
        self.profile_dd_btn.click()

    def fill_name(self, text):
        self.name.type(text)
        self.save_changes_btn.click()

    def add_category(self, name):
        self.category.type(name).press_enter()

    def category_should_have_name(self, name):
        browser.element(f'//span[contains(text(), "{name}")]').should(be.visible)

    def archvive_btn_one_container(self, name):
        return browser.element(
            f'//span[contains(text(), "{name}")]/parent::div/parent::div//button[@aria-label="Archive category"]'
        )

    def category_should_be_archived(self, name):
        browser.element(
            f'//span[contains(text(), "{name}")]/parent::div/parent::div//button[@aria-label="Unarchive category"]'
        ).should(be.visible)

    def update_category_btn(self, name):
        return browser.element(
            f'//span[contains(text(), "{name}")]/parent::div/parent::div//button[@aria-label="Edit category"]'
        )

    def archive_category(self, name):
        self.add_category(name)
        self.archvive_btn_one_container(name).click()
        self.archive_ask_btn.click()

    def unarchive_category(self, name):
        self.archive_category(name)
        self.archive_checkbox.click()
        browser.element(
            f'//span[contains(text(), "{name}")]/parent::div/parent::div//button[@aria-label="Unarchive category"]'
        ).click()
        self.unarchive_ask_btn.click()

    def category_should_be_unarchived(self, name):
        self.archive_checkbox.click()
        self.category_should_have_name(name)

    def update_category(self, category_name, new_name):
        self.add_category(category_name)
        self.update_category_btn(category_name).click()
        self.update_category_input.type(new_name).press_enter()









