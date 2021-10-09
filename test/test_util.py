from unittest import TestCase
from unittest import skip

from decouple import config
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .driver import get_chrome_driver

WAIT = 5

@skip
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
