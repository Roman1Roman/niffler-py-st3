import random
from pickle import FALSE

import pytest
from selene import have, be

from models.category import CategoryAdd
from models.spend import SpendAdd
from pages.auth_reg_page import AuthRegistrationPage
from pages.spendings_page import SpendingPage
from faker import Faker
from conftest import Auth, category, TestData, Pages

auth_page = AuthRegistrationPage()
spending_page = SpendingPage()
faker = Faker()


class TestSpending:

    description_1_row = 'test_1'
    description_2_row = 'test_2'
    test_category = 'school'

    @TestData.category(test_category)
    @Auth.login
    def test_add_spendings_datepicker_input(self, category):
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.currency.click()
        spending_page.usd_btn.click()
        spending_page.fill_category(category=category)
        spending_page.fill_datepicker_input(full_date='10/10/2024')
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()
        spending_page.table_description_first_row.should(have.text(self.description_1_row))
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()


    @Auth.login
    @TestData.category('schools')
    def test_add_spendings_datepicker_btns(self, category):
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.currency.click()
        spending_page.usd_btn.click()
        spending_page.fill_category(category=category)
        spending_page.fill_date_picker_btns()
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()
        spending_page.table_description_first_row.should(have.text(self.description_1_row))
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()


    @Pages.main
    @TestData.category('schools')
    @TestData.spends(
        SpendAdd(
            amount=104.3,
            description='test descr',
            category=CategoryAdd(username='test_name', archived=False),
            spendDate='2024-08-08T18:39:23.955Z',
            currency='RUB',
        )
    )
    def test_delete_spending(self, spends, category):
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()
        spending_page.delete_alert.should(be.visible)
