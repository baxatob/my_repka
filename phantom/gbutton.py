#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

credentials = [{'login':'stephanie.yanchinski@caltech.edu', 'password':'Quebecrules15!'}]

#Global variables:
time_format = '%b %d, %Y'

class GenericUtility(object):
    def __init__(self):
        '''Initialize whatever is needed, selenium, requests session etc etc'''
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", "C:\\TEST\\")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/xml, text/xml")
        profile.set_preference("browser.helperApps.neverAsk.openFile", 'application/xml, text/xml')
        
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver.implicitly_wait(15)
                
    def is_element_presented(self, locator, value):
        '''check if element presented in DOM'''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((locator, value))) 
            return True
        except: return False
        
    def is_element_displayed(self, locator, value):
        '''check if element displayed on the page'''
        if self.driver.find_element(locator, value).is_displayed():
            return True
        else: return False
        
    def wait_for_element(self, locator, value, timeout=15):
        '''wait for expected element and raise timeout exception if element will not presented '''
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((locator, value)))

    def login(self, user):
        self.driver.get('https://www.sce.com/wps/portal/')
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, 'fullLoginEmail'))) 
        self.driver.find_element(By.ID, 'fullLoginEmail').send_keys(user['login'])
        self.driver.find_element(By.ID, 'fullLoginPassword').send_keys(user['password'])
        self.driver.find_element(By.ID, 'loginSubmitDesktopButton_label').click()
        if self.is_element_presented(By.XPATH, r'//div[@class="errorContainer"]') and self.is_element_displayed(By.XPATH, r'//div[@class="errorContainer"]'):
            return "failed"
        else:
            frame = self.driver.find_element(By.XPATH, r'//iframe[@id="DotNetApp_dotNetIframe"]')
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, r'//iframe[@id="DotNetApp_dotNetIframe"]')))
            self.driver.switch_to_frame(frame)
        
    def logout(self):
        self.driver.switch_to_default_content()
        self.driver.find_element(By.XPATH, r'//a[@id="loginLink"]').click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, r'//a[contains(.,"Log In")]')))
        
    def get_green_button(self, starttime = None, endtime = None, meter_id = None, data_type = None):
        '''Tries to go get the green button data for specified time frame.  If startime or endtime is None, extend parameter as far as it can go.  
        Usually that is 1 year back, but that depends on the user account.
        '''
        self.driver.find_element(By.XPATH, r'//span[contains(.,"Green Button")]/ancestor::a').click()
        self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_txtFromDate').send_keys(starttime)
        self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_txtToDate').send_keys(endtime)
        self.driver.find_element(By.XPATH, r'//select[@id="ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_DownloadFormatDropDown"]/option[contains(.,"XML Format")]').click()
        #Selecting the property:
        self.driver.find_element(By.XPATH, r'//table[@id="ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_SmartConnectSAListGrid"]//td[contains(.,"%s")]/preceding-sibling::td[1]//input' % meter_id).click()
        
        self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_DownloadButton').click()
        i=0
        while os.path.exists("*.xml") == False or i <= 30:
            time.sleep(1) # timeout to generate and download the file
            i += 1


if __name__ == '__main__':
    logging.basicConfig(filename='green_button.log', format='%(asctime)s, %(message)s', level=logging.ERROR)
    for user in credentials:
        page = GenericUtility()
        try:
            login = page.login(user)
            page.get_green_button('03/01/2015', '03/31/2015', '2-17-713-5548')
            page.driver.quit()
        except:
            logging.exception()
            page.driver.get_screenshot_as_file('%s.jpg' % time.strftime('%d_%b_%Y_%H-%M-%S'))
            page.driver.quit()
        
            
