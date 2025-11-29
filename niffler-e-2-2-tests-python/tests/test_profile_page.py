from selene import have, be
from pages.profile_page import ProfilePage
from conftest import Pages, Auth
from faker import Faker

profile_page = ProfilePage()
faker = Faker()

class TestProfile:
    name = faker.user_name()
    category_name = faker.text(max_nb_chars=5)
    new_category_name = faker.text(max_nb_chars=5)

    @Auth.login
    def test_open_profile_page(self):
        profile_page.open_profile_page()
        profile_page.profile_text.should(be.visible)

    @Auth.login
    def test_add_name(self):
        profile_page.open_profile_page()
        profile_page.fill_name(text=self.name)
        profile_page.alert.should(be.visible)

    @Auth.login
    def test_add_category(self):
        profile_page.open_profile_page()
        profile_page.add_category(name=self.category_name)
        profile_page.category_should_have_name(name=self.category_name)

    @Auth.login
    def test_archive_category(self):
        profile_page.open_profile_page()
        profile_page.archive_category(name=self.category_name)
        profile_page.archive_checkbox.click()
        profile_page.category_should_be_archived(name=self.category_name)

    @Auth.login
    def test_unarchive_category(self):
        profile_page.open_profile_page()
        profile_page.unarchive_category(name=self.category_name)
        profile_page.category_should_be_unarchived(name=self.category_name)

    @Auth.login
    def test_update_category(self):
        profile_page.open_profile_page()
        profile_page.update_category(
            category_name=self.category_name,
            new_name=self.new_category_name,
        )
        profile_page.category_should_have_name(name=self.new_category_name)

    @Auth.login
    def test_add_empty_category(self):
        profile_page.open_profile_page()
        profile_page.category.type(' ').press_enter()
        profile_page.error_text.should(be.visible)
