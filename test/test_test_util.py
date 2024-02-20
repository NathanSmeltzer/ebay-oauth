from unittest import TestCase, skip

from test.utils.test_util import TestUtil

WAIT = 5

app_scopes = [
    # "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    # "https://api.ebay.com/oauth/api_scope/sell.marketing",
    # "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
]

# todo:
# @skip("Not currently working")
class TestTestUtil(TestCase):

    def setUp(self) -> None:
        self.test_util = TestUtil()
        self.test_util.read_user_info()

    def test_read_user_info(self):
        self.test_util.read_user_info()
        assert self.test_util.userid
        assert self.test_util.password

    def test_log_in(self):
        self.test_util.log_in()

    def test_get_code_from_url(self):
        url = "https://app.example.com/accounts/login/?next=/users/ebay-auth/%3Fcode%3Dv%255E1.1%2523i%255E1%2523p%255E3%2523r%255E1%2523f%255E0%2523I%255E3%2523t%255EUl41XzY6Q0ZGNkUxNURGOTgwMjVFMDBENjkyOEEwNjUwNEVBMzlfMl8xI0VeMjYw%26expires_in%3D299"
        code = self.test_util.get_code_from_url(url)
        assert code

    def test_get_authorization_code(self):
        code = self.test_util.get_authorization_code()
        print(f"code: {code}")