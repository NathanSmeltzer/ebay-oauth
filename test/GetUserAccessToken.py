# -*- coding: utf-8 -*-

"""As of 2021, the sandbox signin url does not work via selenium. Production must be used
ebay's guide for this repo:
https://tech.ebayinc.com/engineering/ebay-oauth-client-library-in-python-and-best-practices/"""

import os, sys
import json

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from oauthclient.oauth2api import Oauth2api
import TestUtil
from oauthclient.credentialutil import credentialutil
from oauthclient.model.model import environment
import unittest
from unittest import skip
from decouple import config

app_scopes = [
            # "https://api.ebay.com/oauth/api_scope",
              "https://api.ebay.com/oauth/api_scope/sell.inventory",
              # "https://api.ebay.com/oauth/api_scope/sell.marketing",
              # "https://api.ebay.com/oauth/api_scope/sell.account",
              "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
              ]


class TestGetApplicationCredential(unittest.TestCase):

    @skip
    def test_load_credentials_exp(self):
        """credentialutil.py lod()"""
        app_config_path = config('EBAY_USER_CREDENTIALS')
        with open(app_config_path, 'r') as f:
            if app_config_path.endswith('.json'):
                content = json.loads(f.read())
                print(content)

    def test_generate_authorization_url(self):
        # app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        app_scopes = [
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
        ]
        app_config_path = config('EBAY_CREDENTIALS')
        credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.PRODUCTION, app_scopes)
        self.assertIsNotNone(signin_url)
        print('\n *** test_get_signin_url ***: \n', signin_url)

    # @skip # reskip after done in case tests are automatically run
    def test_exchange_authorization_code(self):
        """
        Use this for getting our business store user code for djproducts
        only works for production (not sandbox)"""
        app_config_path = config('EBAY_CREDENTIALS')
        credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(
            environment.PRODUCTION, app_scopes, state="testval")
        print(f"signin_url: {signin_url}")
        code = TestUtil.get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(environment.PRODUCTION, code)
        self.assertIsNotNone(user_token.access_token)
        self.assertTrue(len(user_token.access_token) > 0)
        print('\n *** test_get_user_access_token ***:\n', user_token)

    @skip  # change to production instead of sandbox for this to work
    def test_exchange_refresh_for_access_token(self):
        app_config_path = config('EBAY_CREDENTIALS')
        credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.SANDBOX, app_scopes)
        code = TestUtil.get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(environment.SANDBOX, code)
        self.assertIsNotNone(user_token.refresh_token)
        self.assertTrue(len(user_token.refresh_token) > 0)

        user_token = oauth2api_inst.get_access_token(environment.SANDBOX, user_token.refresh_token, app_scopes)
        self.assertIsNotNone(user_token.access_token)
        self.assertTrue(len(user_token.access_token) > 0)

        print('\n *** test_refresh_user_access_token ***:\n', user_token)

    # todo: finish or combine
    def test_get_access_token(self):
        inst = Oauth2api()
        print(f"inst: {inst} of type {type(inst)}")
        # token = oauth2api().get_application_token(environment.PRODUCTION, app_scopes)
        # token = token.access_token
        # # todo: remove
        # print('\n *** test_get_application_token ***:\n', token)


if __name__ == '__main__':
    unittest.main()
