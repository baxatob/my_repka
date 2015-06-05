#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
import os
from config import timeFormat

def screenShot(obj):
    obj.driver.get_screenshot_as_file(os.path.join('Logs', '%s.jpg' % time.strftime(timeFormat)))
    
def waitForElement(obj, locator, value):
    WebDriverWait(obj.driver, 10).until(EC.presence_of_element_located((locator, value))) 
    
def waitAndClick(obj, locator, value):
    element = WebDriverWait(obj.driver, 10).until(EC.element_to_be_clickable((locator, value)))
    element.click()
    
def randomString(length=7):
    dic = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    textString = ''
    for i in range(length):
        textString = textString + dic[random.randint(0, len(dic) - 1)]
    return textString