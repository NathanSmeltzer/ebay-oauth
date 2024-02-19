# -*- coding: utf-8 -*-

"""As of 2021, the sandbox signin url does not work via selenium. Production must be used
ebay's guide for this repo:
https://tech.ebayinc.com/engineering/ebay-oauth-client-library-in-python-and-best-practices/"""

import os, sys
import json

from test.utils.test_util import TestUtil

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from oauthclient.oauth2api import Oauth2api
from oauthclient.credentialutil import CredentialUtil
from oauthclient.model.model import Environment
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

# todo: remove if no longer using selenium/tests
class TestGetApplicationCredential(unittest.TestCase):

    # todo:
    # @skip("Part of TestUtil - no longer works")
    def test_exchange_authorization_code(self):
        """
        Use this for getting our business store user code for djproducts
        only works for production (not sandbox)"""
        # oauth2api_inst = Oauth2api()
        # signin_url = oauth2api_inst.generate_user_authorization_url(app_scopes, state="testval")
        # print(f"signin_url: {signin_url}")
        test_util = TestUtil()
        # todo: add back
        # code = TestUtil.get_authorization_code(signin_url)
        # user_token = oauth2api_inst.exchange_code_for_access_token(Environment.PRODUCTION, code)
        # self.assertIsNotNone(user_token.access_token)
        # self.assertTrue(len(user_token.access_token) > 0)
        # print('\n *** test_get_user_access_token ***:\n', user_token)

    # todo: fix
    # @skip  # change to production instead of sandbox for this to work
    def test_exchange_refresh_for_access_token(self):
        oauth2api = Oauth2api(environment="sandbox")
        test_util = TestUtil(oauth2api=oauth2api)
        code = test_util.get_authorization_code()
        user_token = oauth2api.exchange_code_for_access_token(code)
        self.assertIsNotNone(user_token.refresh_token)
        self.assertTrue(len(user_token.refresh_token) > 0)

        # user_token = oauth2api_inst.get_access_token(Environment.SANDBOX, user_token.refresh_token, app_scopes)
        # self.assertIsNotNone(user_token.access_token)
        # self.assertTrue(len(user_token.access_token) > 0)

        print('\n *** test_refresh_user_access_token ***:\n', user_token)


if __name__ == '__main__':
    unittest.main()
