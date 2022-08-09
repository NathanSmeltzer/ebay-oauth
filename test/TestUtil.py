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
import yaml

from decouple import config, UndefinedValueError
from loguru import logger
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

WAIT = 6
LONG_WAIT = 40
SHORT_WAIT = 3

sandbox_key = "sandbox-user"
production_key = "production-user"
_user_credential_list = {}

try:  # instead of manually resetting headless value for testing issues. Getting from normal env file
    headless_setting = config('HEADLESS', cast=bool)
    # logger.warning(f"headless_setting in top of driver.py: {headless_setting}")
except UndefinedValueError:
    # logger.warning("defaulting to True for headless_setting")
    headless_setting = True


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


# todo:refactory/DRY
def get_authorization_code(signin_url):
    user_config_path = config('EBAY_USER_CREDENTIALS')
    read_user_info(user_config_path)

    env_key = production_key
    if "sandbox" in signin_url:
        env_key = sandbox_key

    userid = _user_credential_list[env_key][0]
    password = _user_credential_list[env_key][1]

    chrome_options = Options()
    if headless_setting:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              options=chrome_options)
    driver.get(signin_url)
    # todo: check if recaptcha checkbox iframe
    checkbox_iframes = driver.find_elements(By.CSS_SELECTOR,
                                            "iframe[title='widget containing checkbox for hCaptcha security challenge']")
    if checkbox_iframes:
        logger.info("switching to recaptcha iframe")
        driver.switch_to.frame(checkbox_iframes[0])
        checkbox_elem = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_element_located((By.ID, "checkbox")))
        checkbox_elem.click()

    # todo: remove
    # time.sleep(3000)
    time.sleep(5)

    # form_userid = driver.find_element_by_id('userid')
    form_userid = WebDriverWait(driver, LONG_WAIT).until(
        EC.presence_of_element_located((By.ID, "userid")))

    logger.info("inputting userid")
    form_userid.send_keys(userid)
    logger.info("submitting userid")
    driver.find_element(By.ID, "sgnBt").submit()
    error_messages = driver.find_elements(By.ID, "errormsg")
    if error_messages:
        logger.info("error message found")
    logger.info("sleeping")
    time.sleep(2)  # todo: needed?

    checkbox_iframes = driver.find_elements(By.CSS_SELECTOR,
                                            "iframe[title='widget containing checkbox for hCaptcha security challenge']")
    if checkbox_iframes:
        logger.info("switching to recaptcha iframe")
        driver.switch_to.frame(checkbox_iframes[0])
        checkbox_elem = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_element_located((By.ID, "checkbox")))
        checkbox_elem.click()

    url = driver.current_url
    logger.info(f"url after submitting userid {url}")
    logger.info("getting password element")
    # todo: remove
    # time.sleep(3000)
    form_pw = WebDriverWait(driver, LONG_WAIT).until(
        EC.presence_of_element_located((By.ID, "pass")))
    # form_pw = driver.find_element(By.ID,'pass')
    logger.debug(f"password element: {form_pw}")
    # todo: remove
    # logger.debug(f"password is: {password}")
    logger.info("submitting password")
    form_pw.send_keys(password)
    driver.find_element(By.ID, "sgnBt").submit()
    time.sleep(1) # todo: needed?
    # code may display after password submission before clicking accept
    url = driver.current_url
    if 'code=' in url:
        logger.info("code found after password submission")
        logger.debug(f"url: {url}")
        code = re.findall('code=(.*?)&', url)[0]
        logger.info(f"Code Obtained: {code}")

    else:
        error_messages = driver.find_elements(By.ID, "errormsg")
        if error_messages:
            logger.info("error message found")
        # todo: remove
        # time.sleep(3000)
        logger.info("finding final_submit")
        final_submit = WebDriverWait(driver, SHORT_WAIT).until(
                EC.presence_of_element_located((By.ID, "submit")))
        final_submit.click()
        time.sleep(1) # todo: needed?
        url = driver.current_url
        logger.debug(f"url: {url}")
        if 'code=' in url:
            code = re.findall('code=(.*?)&', url)[0]
            logger.info(f"Code Obtained: {code}")
        else:
            logger.error(f"Unable to obtain code via sign in URL: {url}")
    # url decode
    decoded_code = urllib.parse.unquote(code)
    logger.info(f"decoded_code: {decoded_code}")
    driver.quit()
    return decoded_code
