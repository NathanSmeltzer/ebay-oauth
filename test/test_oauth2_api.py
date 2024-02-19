import os, sys
import json
# todo: needed?
# sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from oauthclient.oauth2api import Oauth2api
import TestUtil
from oauthclient.credentialutil import CredentialUtil
from oauthclient.model.model import Environment
import unittest
from decouple import config

class TestOAuth2API(unittest.TestCase):
    def test_generate_user_authorization_url(self):
        # app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        app_scopes = [
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
        ]
        app_config_path = config('EBAY_CREDENTIALS')
        CredentialUtil.load(app_config_path)
        oauth2api_inst = Oauth2api(environment=Environment.PRODUCTION)
        signin_url = oauth2api_inst.generate_user_authorization_url(app_scopes)
        self.assertIsNotNone(signin_url)
        print('\n *** test_get_signin_url ***: \n', signin_url)