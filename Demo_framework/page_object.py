#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import baseUrl

class Base(object):
    def __init__(self, driver):
        self.driver = driver


class StartPage(Base):
    demoItem = (By.XPATH, r'//div[@class="item-wrap eq"]//div[@class="item-thumb"]/a')
        
    def click_on_item(self):
        link = self.driver.find_element(*self.demoItem).get_attribute('href')
        self.driver.get(link)    
    

class Item(Base):   
    def select_color_and_qty(self, color, qty):
        self.driver.find_element(By.XPATH, r'//select[@id="trait_Color"]//option[text()="%s"]' % color).click()
        self.driver.find_element(By.XPATH, r'//input[@id="textfield"]').send_keys(qty)
    
    def add_to_cart(self):
        self.driver.find_element(By.ID, 'displayAddToCart').click()
        

class Registration(Base):
    invalidZIPalert = (By.XPATH, r'//span[@class="field-validation-error"][text()="Invalid bill to zip/postal code."]')
    
    def registration(self, zipCode, customerNum='123456', fName='Auto', lName='Test', uName='autotest', eMail='test@test.com', password='123456', retypePswd='123456'):
        self.driver.find_element(By.ID, 'CustomerNumber').send_keys(customerNum)
        self.driver.find_element(By.ID, 'BTZipCode').send_keys(zipCode)
        self.driver.find_element(By.ID, 'FirstName').send_keys(fName)
        self.driver.find_element(By.ID, 'LastName').send_keys(lName)
        self.driver.find_element(By.ID, 'UserName').send_keys(uName)
        self.driver.find_element(By.ID, 'Email').send_keys(eMail)
        self.driver.find_element(By.ID, 'Password').send_keys(password)
        self.driver.find_element(By.ID, 'RetypePassword').send_keys(retypePswd)
        self.driver.find_element(By.ID, 'submitRegistration').click()
    
    def zip_alert_displayed(self):
        if self.driver.find_element(*self.invalidZIPalert).is_displayed():
            return True
        else: return False
        
            