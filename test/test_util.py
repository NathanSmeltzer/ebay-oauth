import json
import logging
import yaml
from unittest import TestCase

from decouple import config
from loguru import logger

from oauthclient.model.model import environment
from oauthclient.oauth2api import oauth2api
from .driver import get_chrome_driver

app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope/sell.inventory",
              "https://api.ebay.com/oauth/api_scope/sell.marketing",
              "https://api.ebay.com/oauth/api_scope/sell.account",
              "https://api.ebay.com/oauth/api_scope/sell.fulfillment"]
sandbox_key = "sandbox-user"
production_key = "production-user"
_user_credential_list = {}
oauth2api_inst = oauth2api()


def read_user_info(conf=None):
    logger.info("Loading user credential configuration file at: %s", conf)
    with open(conf, 'r') as f:
        if conf.endswith('.yaml') or conf.endswith('.yml'):
            content = yaml.load(f)
        elif conf.endswith('.json'):
            content = json.loads(f.read())
        else:
            raise ValueError('Configuration file need to be in JSON or YAML')

        for key in content:
            logging.debug("Environment attempted: %s", key)

            if key in [sandbox_key, production_key]:
                userid = content[key]['username']
                password = content[key]['password']
                _user_credential_list.update({key: [userid, password]})


class TestUtil(TestCase):
    # todo: complete
    def setUp(self) -> None:
        self.driver = get_chrome_driver()

    def test_signin(self):
        user_config_path = config('EBAY_USER_CREDENTIALS')
        read_user_info(user_config_path)
        env_key = production_key
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.SANDBOX, app_scopes)
        print(signin_url)
        # if "sandbox" in signin_url:
        #     env_key = sandbox_key
        # userid = _user_credential_list[env_key][0]
        # password = _user_credential_list[env_key][1]
        # self.driver.get(signin_url)