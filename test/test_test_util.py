from unittest import TestCase

from decouple import config
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from test.utils.driver import get_chrome_driver
from test.utils.test_util import TestUtil

WAIT = 5

app_scopes = [
    # "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    # "https://api.ebay.com/oauth/api_scope/sell.marketing",
    # "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
]


# @skip
class TestTestUtil(TestCase):
    # todo: complete or remove

    def setUp(self) -> None:
        self.test_util = TestUtil()

    def test_read_user_info(self):
        self.test_util.read_user_info()
        assert self.test_util.userid
        assert self.test_util.password

    # todo: finish
    def test_log_in(self):
        self.test_util.log_in()

    # todo: remove?
    def test_signin_exp(self):
        self.driver.get(config('PRODUCTION_AUTH_URL'))
        # sbx
        # self.driver.get(
        #     "https://signin.sandbox.ebay.com/ws/eBayISAPI.dll?SignIn&AppName=NathanSm-OrderAut-SBX-2c22b8256-da03e591&ru=https%3A%2F%2Fauth.sandbox.ebay.com%2Foauth2%2Fauthorize%3Fclient_id%3DNathanSm-OrderAut-SBX-2c22b8256-da03e591%26redirect_uri%3DNathan_Smeltzer-NathanSm-OrderA-dntshp%26scope%3Dhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.inventory%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.marketing%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.account%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.fulfillment%26state%26response_type%3Dcode%26hd")
        form_userid = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located((By.ID, "userid"))
        )
        logger.info("form_userid found")
        form_userid.send_keys("test")
        # form_userid = browser.find_element_by_id('userid')
