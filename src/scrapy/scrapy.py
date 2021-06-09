import time
import random
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary


class SuumoScrapyJob:
    def __init__(self, option=False):
        self.state = False
        if option:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--headless")
            self.options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(options=self.options)
        else:
            self.driver = webdriver.Chrome()
