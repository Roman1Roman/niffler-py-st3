from conftest import TestData, spend_db, Auth
from models.category import CategoryAdd
from models.spend import SpendAdd

TEST_CATEGORY = 'test_category'

class TestCategory:

    username = 'test_user'

    @TestData.spends(
        SpendAdd(
            amount=104.3,
            description='test descr',
            category=CategoryAdd(username=username, archived=False, name=TEST_CATEGORY),
            spendDate='2024-08-08T18:39:23.955Z',
            currency='RUB',
        )
    )
    def test_category_in_db(self, spend_db, spends, spends_client):
        response = spend_db.get_user_categories(username=self.username)
        category = response[0]
        assert category.name == TEST_CATEGORY
        assert category.username == self.username
        assert category.archived == False

    @TestData.spends(
        SpendAdd(
            amount=104.3,
            description='test descr',
            category=CategoryAdd(username=username, archived=False, name=TEST_CATEGORY),
            spendDate='2024-08-08T18:39:23.955Z',
            currency='RUB',
        )
    )
    def test_spend_in_db(self, spend_db, spends, spends_client):
        response = spend_db.get_user_spends(username=self.username)
        spends = response[0]
        assert spends.username == self.username
