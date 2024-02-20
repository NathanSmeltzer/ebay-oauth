import unittest

from decouple import config
import responses
from oauthclient.credentialutil import CredentialUtil
from oauthclient.oauth2api import Oauth2api


class UserAccessTokens(unittest.TestCase):
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

    def test_get_access_token_valid(self):
        refresh_token = config('REFRESH_TOKEN_VALID')
        oauth2api = Oauth2api(environment="production")
        # print(f"environment endpoint: {oauth2api.environment.web_endpoint}")
        token = oauth2api.get_access_token(refresh_token, scopes=self.app_scopes)
        assert token.access_token

    def test_get_access_token_invalid(self):
        oauth2api = Oauth2api(environment="production")
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

    @responses.activate
    def test_exchange_code_for_access_token(self):
        """Mocks resquests response. Not live"""
        oauth2api = Oauth2api(environment="production")
        access_token = "v^1.1#i^1#I^3#f^0#r^0#p^3#t^H4sIAAAAAAA2+SOtRUIkKDRyq+IeBEqsvZt+S/bLQI1MxoAAA=="
        # example from https://developer.ebay.com/api-docs/static/oauth-auth-code-grant-request.html
        exchange_code_response = {
            "access_token": access_token,
            "expires_in": 7200,
            "refresh_token": access_token,
            "refresh_token_expires_in": 47304000,
            "token_type": "User Access Token"
        }
        responses.add(responses.POST, oauth2api.environment.api_endpoint,
                      json=exchange_code_response, status=200)
        token = oauth2api.exchange_code_for_access_token("fakecode")
        print(token)
        print(type(token))
        assert token.access_token == access_token