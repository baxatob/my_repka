#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#from selenium import webdriver
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait, Select
from tests.base_test import Browser

class Base(Browser):
    def __init__(self, driver):
        self.driver = driver
        
    def clickOn(self, locator, value):
        #element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((locator, value)))
        element = self.driver.find_element(locator, value)
        element.click()
        
    def sendKeys(self, input_, locator, value):
        #element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((locator, value)))
        element = self.driver.find_element(locator, value)
        element.send_keys(input_)
        
        