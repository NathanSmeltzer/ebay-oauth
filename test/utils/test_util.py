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
import re
import time
import urllib
from typing import Optional
from urllib.parse import urlparse

import yaml
from decouple import config, UndefinedValueError
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from oauthclient.model.model import Environment
from oauthclient.oauth2api import Oauth2api
from test.utils.driver import get_chrome_driver

WAIT = 6
LONG_WAIT = 40
SHORT_WAIT = 3

try:  # instead of manually resetting headless value for testing issues. Getting from normal env file
    headless_setting = config('HEADLESS', cast=bool)
    # logger.warning(f"headless_setting in top of driver.py: {headless_setting}")
except UndefinedValueError:
    # logger.warning("defaulting to True for headless_setting")
    headless_setting = True

class TestUtil:
    """No longer works"""
    def __init__(self, oauth2api: Oauth2api = Oauth2api(),
                 driver: webdriver.Chrome = get_chrome_driver(headless=headless_setting),
                 user_config_path: str = config('EBAY_USER_CREDENTIALS', default="ebay_user.json")):
        self.oauth2api = oauth2api
        self.driver = driver
        # get environment from oauth2api
        self.environment = "production" if self.oauth2api.environment == Environment.PRODUCTION else "sandbox"
        self.user_config_path = user_config_path
        # get user info
        self.userid = None
        self.password = None

    def read_user_info(self):
        conf_path = self.user_config_path
        logger.debug(f"conf_path: {conf_path}")
        sandbox_key = "sandbox-user"
        production_key = "production-user"
        if self.environment == "production":
            key = production_key
        else:
            key = sandbox_key

        with open(self.user_config_path, 'r') as f:
            if conf_path.endswith('.yaml') or conf_path.endswith('.yml'):
                content = yaml.load(f)
            elif conf_path.endswith('.json'):
                logger.debug("loading json")
                content = json.loads(f.read())
            else:
                raise ValueError('Configuration file need to be in JSON or YAML')

            self.userid = content[key]['username']
            self.password = content[key]['password']

    def click_recaptcha_checkboxes(self):
        """NOTE: You will have to manually intervene sometimes for image selection.
        After manually selecting the correct images, the automated checkbox clicking works for some time"""
        logger.debug("inside click_recaptcha_checkboxes")
        time.sleep(1)  # needed
        checkbox_iframes = self.driver.find_elements(By.CSS_SELECTOR,
                                                     "iframe[title='Widget containing checkbox for hCaptcha security challenge']")
        logger.debug(f"checkbox_iframes: {checkbox_iframes}")
        if checkbox_iframes:
            logger.info("switching to recaptcha iframe")
            self.driver.switch_to.frame(checkbox_iframes[0])
            checkbox_elem = WebDriverWait(self.driver, LONG_WAIT).until(
                EC.presence_of_element_located((By.ID, "checkbox")))
            checkbox_elem.click()

    def log_in(self) -> str:
        auth_url = self.oauth2api.generate_user_authorization_url()
        logger.debug(f"auth_url: {auth_url}")
        self.driver.get(auth_url)
        self.click_recaptcha_checkboxes()
        form_userid = WebDriverWait(self.driver, LONG_WAIT).until(
            EC.presence_of_element_located((By.ID, "userid")))
        logger.info(f"submitting userid: {self.userid}")
        form_userid.send_keys(self.userid)
        self.driver.find_element(By.ID, "signin-continue-btn").submit()
        logger.info(f"url after submitting userid {self.driver.current_url}")
        # hcaptcha sometimes comes up twice
        self.click_recaptcha_checkboxes()
        logger.info("getting password element")
        form_pw = WebDriverWait(self.driver, LONG_WAIT).until(
            EC.presence_of_element_located((By.ID, "pass")))
        logger.debug(f"password element: {form_pw}")
        logger.info("submitting password")
        form_pw.send_keys(self.password)
        logger.debug("typed the password, about to submit")
        # time.sleep(3000)
        signin_button = self.driver.find_element(By.ID, "sgnBt")
        logger.debug(f"signin_button: {signin_button}")
        signin_button.submit()
        # todo: stops after the signin_button - unsure why
        logger.debug(f"url after submitting password: {self.driver.current_url}")
        return self.driver.current_url

    def get_code_from_url(self, url) -> Optional[str]:
        parsed_url = urlparse(url)
        query_string = parsed_url.query
        query_params = urllib.parse.parse_qs(query_string)
        next_param = query_params.get('next', None)[0]
        if next_param:
            next_params = urllib.parse.parse_qs(urllib.parse.urlparse(next_param).query)
            code = next_params.get('code', [])
            return code[0]

    def get_authorization_code(self) -> Optional[str]:
        self.read_user_info()
        url = self.log_in()
        # logger.debug(f"url in from login: {url}")
        code = self.get_code_from_url(url)
        return code if code else None