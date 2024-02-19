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

# todo: remove after refactored into class
sandbox_key = "sandbox-user"
production_key = "production-user"
_user_credential_list = {}

try:  # instead of manually resetting headless value for testing issues. Getting from normal env file
    headless_setting = config('HEADLESS', cast=bool)
    # logger.warning(f"headless_setting in top of driver.py: {headless_setting}")
except UndefinedValueError:
    # logger.warning("defaulting to True for headless_setting")
    headless_setting = True

# todo: remove if not using
# class TestUser:



class TestUtil:
    def __init__(self, oauth2api: Oauth2api = Oauth2api(),
                 driver: webdriver.Chrome=get_chrome_driver(headless = headless_setting),
                 user_config_path: str = config('EBAY_USER_CREDENTIALS', default="ebay_user.json" )):
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

    # todo: finish
    def click_recaptcha_checkboxes(self):
        """NOTE: You will have to manually intervene sometimes for image selection.
        After manually selecting the correct images, the automated checkbox clicking works for some time"""
        logger.debug("inside click_recaptcha_checkboxes")
        time.sleep(1)  # needed
        # time.sleep(30000) # todo: remove
        checkbox_iframes = self.driver.find_elements(By.CSS_SELECTOR,
                                                "iframe[title='Widget containing checkbox for hCaptcha security challenge']")
        logger.debug(f"checkbox_iframes: {checkbox_iframes}")
        if checkbox_iframes:
            logger.info("switching to recaptcha iframe")
            self.driver.switch_to.frame(checkbox_iframes[0])
            checkbox_elem = WebDriverWait(self.driver, LONG_WAIT).until(
                EC.presence_of_element_located((By.ID, "checkbox")))
            checkbox_elem.click()

    # todo: finish
    def log_in(self):
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
        logger.info("getting password element")
        form_pw = WebDriverWait(self.driver, LONG_WAIT).until(
            EC.presence_of_element_located((By.ID, "pass")))
        logger.debug(f"password element: {form_pw}")
        logger.info("submitting password")
        form_pw.send_keys(self.password)
        self.driver.find_element(By.ID, "sgnBt").submit()

# todo: needed?
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
            logger.debug("Environment attempted: %s", key)

            if key in [sandbox_key, production_key]:
                userid = content[key]['username']
                password = content[key]['password']
                _user_credential_list.update({key: [userid, password]})


def click_recaptcha_checkboxes(driver):
    logger.debug("inside click_recaptcha_checkboxes")
    time.sleep(1)  # needed
    checkbox_iframes = driver.find_elements(By.CSS_SELECTOR,
                                            "iframe[title='widget containing checkbox for hCaptcha security challenge']")
    logger.debug(f"checkbox_iframes: {checkbox_iframes}")
    if checkbox_iframes:
        logger.info("switching to recaptcha iframe")
        driver.switch_to.frame(checkbox_iframes[0])
        checkbox_elem = WebDriverWait(driver, LONG_WAIT).until(
            EC.presence_of_element_located((By.ID, "checkbox")))
        checkbox_elem.click()


def get_authorization_code(signin_url):
    """NOTE: No longer works as of 2/2024"""
    # todo: needed?
    user_config_path = config('EBAY_USER_CREDENTIALS')
    logger.debug(f"user_config_path: {user_config_path}")
    read_user_info(user_config_path)

    env_key = production_key
    if "sandbox" in signin_url:
        env_key = sandbox_key

    userid = _user_credential_list[env_key][0]
    password = _user_credential_list[env_key][1]
    driver = get_chrome_driver(headless = headless_setting)
    driver.get(signin_url)
    click_recaptcha_checkboxes(driver)


    form_userid = WebDriverWait(driver, LONG_WAIT).until(
        EC.presence_of_element_located((By.ID, "userid")))

    logger.info(f"inputting userid into {form_userid}")
    form_userid.send_keys(userid)
    logger.info("submitting userid")

    driver.find_element(By.ID, "signin-continue-btn").submit()
    url = driver.current_url
    logger.info(f"url after submitting userid {url}")
    logger.info("getting password element")
    form_pw = WebDriverWait(driver, LONG_WAIT).until(
        EC.presence_of_element_located((By.ID, "pass")))
    logger.debug(f"password element: {form_pw}")
    logger.info("submitting password")
    form_pw.send_keys(password)
    driver.find_element(By.ID, "sgnBt").submit()
    # code may display after password submission before clicking accept
    url = driver.current_url
    if 'code=' in url:
        logger.info("code found after password submission")
        logger.debug(f"url: {url}")
        code = re.findall('code=(.*?)&', url)[0]
        logger.info(f"Code Obtained: {code}")

    else:
        logger.info("finding final_submit")
        final_submit = WebDriverWait(driver, LONG_WAIT).until(
            EC.presence_of_element_located((By.ID, "submit")))
        logger.debug(f"final_submit: {final_submit}")
        final_submit.click()
        url = driver.current_url
        logger.debug(f"url before parsing: {url}")
        # get the code query parameter from the url
        parsed_url = urlparse(url)
        query_string = parsed_url.query
        query_params = urllib.parse.parse_qs(query_string)
        next_param = query_params.get('next', None)[0]
        code = None
        if next:
            next_params = urllib.parse.parse_qs(urllib.parse.urlparse(next_param).query)
            code = next_params.get('code', None)
        if code:
            logger.info(f"Code Obtained: {code}")
        else:
            logger.error(f"Unable to obtain code via sign in URL: {url}")
            return
    # url decode (unsure if still needed since using urllib.parse.parse_qs) earlier
    decoded_code = urllib.parse.unquote(code)
    logger.info(f"decoded_code: {decoded_code}")
    driver.quit()
    return decoded_code
