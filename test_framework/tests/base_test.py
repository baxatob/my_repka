#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import logging
import time
import os
from selenium.webdriver.remote.command import Command
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver 
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By
from config import baseUrl, timeFormat

class Browser(WebDriver):
    def find_element(self, by=By.ID, value=None):
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        print "OVERRIDED!"
        return self.execute(Command.FIND_ELEMENT,
                             {'using': by, 'value': value})['value']

  
class AbstractTestCase(unittest.TestCase, Browser):
    
    def setUp(self):
        logging.basicConfig(filename = os.path.join('Logs', 'modere_testing_%s.log' % time.strftime(timeFormat)), format='%(asctime)s, %(message)s', level=logging.INFO)
        self.driver = webdriver.Firefox()        
        self.driver.implicitly_wait(15)
        self.driver.get(baseUrl)
        
    def tearDown(self):
        self.driver.close()