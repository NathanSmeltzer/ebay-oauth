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
    app_scopes = [
        "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
    ]

    def test_generate_user_authorization_url(self):
        app_config_path = config('EBAY_CREDENTIALS')
        CredentialUtil.load(app_config_path)
        oauth2api = Oauth2api()
        signin_url = oauth2api.generate_user_authorization_url(self.app_scopes)
        self.assertIsNotNone(signin_url)
        print('\n *** test_get_signin_url ***: \n', signin_url)

    def test_get_access_token(self):
        refresh_token = config('REFRESH_TOKEN_VALID')
        oauth2api = Oauth2api(environment="production")
        # print(f"environment endpoint: {oauth2api.environment.web_endpoint}")


        token = oauth2api.get_access_token(refresh_token, scopes=self.app_scopes)

        assert token.access_token

        #  faulty token
        refresh_token = config('REFRESH_TOKEN_INVALID')
        token = oauth2api.get_access_token(refresh_token, scopes=self.app_scopes)
        assert token.access_token is None
        assert "500" in token.error
        print(type(token.error))

        # invalid request scope
        refresh_token = config('REFRESH_TOKEN_VALID')
        app_scopes_invalid = [
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
            # no access to this scope
            "https://api.ebay.com/oauth/api_scope",
        ]
        token = oauth2api.get_access_token(refresh_token, scopes=app_scopes_invalid)
        # print(f"token.access_token: {token.access_token} of type: {type(token.access_token)}")
        # print(token.error)
        assert "400" in token.error

        # issued other client/expired - invalid or issued to another client
        refresh_token = config('REFRESH_TOKEN_EXPIRED')
        app_scopes = [
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
            "https://api.ebay.com/oauth/api_scope/sell.inventory",
        ]
        token = oauth2api.get_access_token(refresh_token, scopes=app_scopes)
        # print(f"token.access_token: {token.access_token} of type: {type(token.access_token)}")
        # print(token.error)
        assert "400" in token.error
        assert "another client" in token.error