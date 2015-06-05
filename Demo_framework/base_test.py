import unittest
import logging
from selenium import webdriver
from config import baseUrl, NAME, KEY

"""class AbstractTestCase(unittest.TestCase):
    #USE THIS CLASS FOR TESTING WITH BROWSER STACK PLATFORM
    
    def setUp(self):
        desired_cap = {'browser': 'Firefox', 'browser_version': '35.0', 'os': 'Windows', 'os_version': '7', 'resolution': '1024x768'}
        self.driver = webdriver.Remote(
                                        command_executor='http://%s:%s@hub.browserstack.com:80/wd/hub' % (NAME, KEY),
                                        desired_capabilities=desired_cap)
        
        self.driver.implicitly_wait(15)
        self.driver.get(baseUrl)
        
    def tearDown(self):
        self.driver.close()
"""

      
class AbstractTestCase(unittest.TestCase):
    #USE THIS CLASS FOR LOCAL TESTING
    
    def setUp(self):
        logging.basicConfig(filename='ameripride.log', format='%(asctime)s, %(message)s', level=logging.INFO)
        self.driver = webdriver.Firefox()        
        self.driver.implicitly_wait(15)
        self.driver.get(baseUrl)
        
    def tearDown(self):
        self.driver.close()