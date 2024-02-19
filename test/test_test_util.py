from unittest import TestCase

from decouple import config
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from oauthclient.credentialutil import CredentialUtil
from oauthclient.model.model import Environment
from oauthclient.oauth2api import Oauth2api
from .driver import get_chrome_driver

WAIT = 5

app_scopes = [
    # "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    # "https://api.ebay.com/oauth/api_scope/sell.marketing",
    # "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
]


# @skip
class TestUtilTesting(TestCase):
    # todo: complete

    def setUp(self) -> None:
        self.driver = get_chrome_driver()

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


class CredentialUtil(TestCase):

    def test_generate_user_authorization_url(self):
        app_config_path = config('EBAY_CREDENTIALS')
        CredentialUtil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(Environment.SANDBOX, app_scopes)
        print(f"signin_url: {signin_url}")


class GetToken(TestCase):
    def test_get_app_token(self):
        """guide: https://tech.ebayinc.com/engineering/ebay-oauth-client-library-in-python-and-best-practices/"""

        oauth2api_inst = Oauth2api()
        app_token = oauth2api_inst.get_application_token(Environment.PRODUCTION, app_scopes)
