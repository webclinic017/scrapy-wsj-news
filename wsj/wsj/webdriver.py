import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_name = ''
password = ''
login_page = 'https://accounts.wsj.com/login?target=https%3A%2F%2Fwww.wsj.com%2F'


def init_driver(browser_name):
    path_root = os.path.dirname(os.path.abspath(__file__))
    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        executable_path = os.path.join(path_root, 'driver', 'chromedriver.exe')
        driver = webdriver.Chrome(options=options, executable_path=executable_path)
    elif browser_name == 'phantomjs':
        executable_path = os.path.join(path_root, 'driver', 'phantomjs.exe')
        driver = webdriver.PhantomJS(executable_path=executable_path)
    driver.set_window_size(1920, 1640)
    return driver


def login(driver):
    driver.get(login_page)
    driver.find_element_by_id("username").send_keys(user_name)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_class_name("basic-login-submit").click()


def logout(driver):
    driver.find_element_by_id("customer-nav-full-name").click()
    # driver.find_element_by_link_text("Sign Out")
    locator = (By.LINK_TEXT, 'Sign Out')
    element = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
    element.click()


browser = init_driver('chrome')
login(browser)
sleep(30)
cookies = browser.get_cookies()
print(cookies)
logout(browser)
