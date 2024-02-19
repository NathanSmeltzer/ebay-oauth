# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

"""
from oauthclient.oauth2api import Oauth2api
import unittest

app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope"]
invalid_app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope/sell.inventory"]

class TestGetApplicationCredential(unittest.TestCase):

        
    def test_invalid_oauth_scope(self):
        oauth2api_inst = Oauth2api()
        app_token = oauth2api_inst.get_application_token(invalid_app_scopes)
        self.assertIsNone(app_token.access_token)
        self.assertIsNotNone(app_token.error)
        print('\n *** test_invalid_oauth_scope ***\n', app_token)
    

    def test_client_credentials_grant_sandbox(self):
        oauth2api = Oauth2api(environment="sandbox")
        app_token = oauth2api.get_application_token(app_scopes)
        self.assertIsNone(app_token.error)
        self.assertIsNotNone(app_token.access_token)
        self.assertTrue(len(app_token.access_token) > 0)
        print('\n *** test_client_credentials_grant_sandbox ***:\n', app_token)

    def test_client_credentials_grant_production(self):
        oauth2api = Oauth2api(environment="production")
        app_token = oauth2api.get_application_token(app_scopes)
        self.assertIsNone(app_token.error)
        self.assertIsNotNone(app_token.access_token)
        self.assertTrue(len(app_token.access_token) > 0)
        # print('\n *** test_client_credentials_grant_production ***:\n', app_token)


if __name__ == '__main__':
    unittest.main()