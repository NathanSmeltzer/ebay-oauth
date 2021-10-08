"""create the webdriver instances"""
import random

from decouple import UndefinedValueError, config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

try:  # instead of manually resetting headless value for testing issues. Getting from normal env file
    headless_setting = config('HEADLESS', cast=bool)
    # logger.warning(f"headless_setting in top of driver.py: {headless_setting}")
except UndefinedValueError:
    # logger.warning("defaulting to True for headless_setting")
    headless_setting = True


def get_chrome_driver(headless=headless_setting):
    """
    Creates selenium.webdriver.chrome driver instance
    :param headless: Flag if wanting to run in headless mode
    :type headless: Bool
    :return: chrome driver instance
    :rtype: selenium.webdriver.chrome
    :testing: test_order.GetDriver
    """
    chrome_options = Options()
    # window size required for certain methods such as entering the discount
    # chrome_options.add_argument("--window-size=1024,768")
    # larger size for PN login button
    chrome_options.add_argument("--window-size=1600,900")
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # chromedriver v83 already has this if platform is windows
        # performance options from https://docs.browserless.io/docs/selenium-library.html
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--force-color-profile=srgb")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--mute-audio")
        # "--enable-features=NetworkService,NetworkServiceInProcess", not sure if needed
    chrome_options.add_argument('--no-sandbox')
    # removing since not standard recommendation
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # doesn't allow for headful
    # chrome_options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              options=chrome_options)
    return driver
