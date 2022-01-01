## Python 3.8
## by alber.py

import os, getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import get_location_data

baseFolder = os.path.dirname(os.path.abspath("__file__"))
user = getpass.getuser()


class TinderBot:
    """ Tinder bot class with all the methods"""

    def __init__(self, location):
        """Method to initialize chrome webdriver with settings"""
        chrome_options = Options()
        # This will create a new profile in your chrome browser
        chrome_options.add_argument(
            f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google Selenium\\Chrome\\User Data"
        )
        chrome_options.add_argument(
            "--profile-directory=Default"
        )
        # Changing the user agent so that tinder.com doesn't know
        # that this is an automated script running using selenium
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.'
            '4044.113 Safari/537.36'
        )
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        lat, lon = get_location_data(location)
        geo_params = {"latitude": float(lat), "longitude": float(lon), "accuracy": 100}
        print(geo_params)
        self.driver = webdriver.Chrome(
            executable_path=baseFolder + "\\chromedriver.exe",  # Path to chrome driver
            chrome_options=chrome_options
        )
        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", geo_params)
        self.location = location

    def start(self, secs=99999):
        """Method to start the bot"""
        self.driver.get('https://tinder.com')
        sleep(secs)