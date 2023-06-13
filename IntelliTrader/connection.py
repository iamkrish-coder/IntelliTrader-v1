import pyotp
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Connection:
    def __init__(self, config):
        self.properties = config
 
    def broker_login(self, KiteConnect):

        # assign properties
        api_key = self.properties[0]
        secret_key = self.properties[1]
        user_id = self.properties[2]
        user_pass = self.properties[3]
        mfa_token = self.properties[4]

        kite = KiteConnect(api_key = api_key)

        # initialize browser service
        service = webdriver.chrome.service.Service('./driver/chromedriver')
        service.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options = options.to_capabilities()
        driver = webdriver.Remote(service.service_url, options=webdriver.ChromeOptions())

        # auto enter login information
        driver.get(kite.login_url())
        driver.implicitly_wait(1)

        # username input
        username = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value='//*[@id="userid"]'))
        username.send_keys(user_id)
        
        # password input
        password = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value='//*[@id="password"]'))
        password.send_keys(user_pass)

        # submit button
        submit = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value='//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
        submit.click()

        driver.implicitly_wait(1)

        # mfa / external TOTP 
        totp = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div/div/form/div[1]/input'))
        authkey = pyotp.TOTP(mfa_token)
        totp.send_keys(authkey.now())

        # continue button
        continue_btn = WebDriverWait(driver, 100).until(
            lambda x: x.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div/div/form/div[2]/button'))
        continue_btn.click()

        url = driver.current_url
        initial_token = url.split('request_token=')[1]
        request_token = initial_token.split('&')[0]
        with open('./output/request_token.txt', 'w') as r_file:
            r_file.write(request_token)

        driver.close()

        data = kite.generate_session(request_token, api_secret=secret_key)
        kite.set_access_token(data['access_token'])
        return kite