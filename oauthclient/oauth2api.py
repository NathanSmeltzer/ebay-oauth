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

import json
import urllib
from datetime import datetime, timedelta
from loguru import logger

import requests
from decouple import config

from oauthclient.model.model import Environment
from .credentialutil import CredentialUtil
from .model import util
from .model.model import OathToken

default_scopes = [
              "https://api.ebay.com/oauth/api_scope/sell.inventory",
              "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
              ]

class Oauth2api:

    def __init__(self, environment: str = "production", credential_config_path: str = config("EBAY_CREDENTIALS")):
        self.environment = Environment.PRODUCTION if environment == "production" else Environment.SANDBOX
        # load credentials
        CredentialUtil.load(credential_config_path)
        self.credential = CredentialUtil.get_credentials(self.environment)
    def generate_user_authorization_url(self, state=None, scopes: list = default_scopes):

        scopes = ' '.join(scopes)
        param = {
            'client_id': self.credential.client_id,
            'redirect_uri': self.credential.ru_name,
            'response_type': 'code',
            'prompt': 'login',
            'scope': scopes
        }

        if state != None:
            param.update({'state': state})

        query = urllib.parse.urlencode(param)
        return self.environment.web_endpoint + '?' + query

    def get_application_token(self, scopes: list = default_scopes):
        """
            makes call for application token and stores result in credential object
            returns credential object
        """

        logger.info("Trying to get a new application access token ... ")
        headers = util._generate_request_headers(self.credential)
        body = util._generate_application_request_body(self.credential, ' '.join(scopes))

        resp = requests.post(self.environment.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = OathToken()

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            # set token expiration time 5 minutes before actual expire time
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(
                minutes=5)

        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logger.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code,
                          requests.status_codes._codes[resp.status_code])
            logger.error("Error: %s - %s", content['error'], content['error_description'])
        return token

    def exchange_code_for_access_token(self, code):
        """Only used in teesting"""
        logger.info("Trying to get a new user access token ... ")
        logger.debug(f"self.environment: {self.environment} of type {type(self.environment)}")
        headers = util._generate_request_headers(self.credential)
        body = util._generate_oauth_request_body(self.credential, code)
        resp = requests.post(self.environment.api_endpoint, data=body, headers=headers)

        content = json.loads(resp.content)
        token = OathToken()

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(
                minutes=5)
            token.refresh_token = content['refresh_token']
            token.refresh_token_expiry = datetime.utcnow() + timedelta(
                seconds=int(content['refresh_token_expires_in'])) - timedelta(minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logger.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code,
                          requests.status_codes._codes[resp.status_code])
            logger.error("Error: %s - %s", content['error'], content['error_description'])
        return token

    def get_access_token(self, refresh_token, scopes=default_scopes):
        """
        refresh token call
        """

        logger.info("Trying to get a new user access token ... ")

        headers = util._generate_request_headers(self.credential)
        body = util._generate_refresh_request_body(' '.join(scopes), refresh_token)
        resp = requests.post(self.environment.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)

        token = OathToken()
        token.token_response = content

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(
                minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logger.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code,
                          requests.status_codes._codes[resp.status_code])
            logger.error("Error: %s - %s", content['error'], content['error_description'])
        return token
