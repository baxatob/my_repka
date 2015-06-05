#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from base_page import *
from config import baseUrl
from common_methods import *

class HomePage(Base):
    menuShop = (By.XPATH, r'//a[@class="open-remote-click"][contains(., "Shop")]')
    
    def account_registration(self, first_name='Test', last_name='Automation', email=randomString(5)+'@autotest.com', phone='(123) 123-1234', password='tEst1234'):
        self.driver.get(baseUrl+'/Account/CreateAccount')
        self.driver.find_element(By.ID, 'Email').send_keys(email)
        self.driver.find_element(By.ID, 'ConfirmEmail').send_keys(email)
        self.driver.find_element(By.ID, 'FirstName').send_keys(first_name)
        self.driver.find_element(By.ID, 'LastName').send_keys(last_name)
        self.driver.find_element(By.ID, 'Phone').send_keys(phone)
        self.driver.find_element(By.ID, 'Password').send_keys(password)
        self.driver.find_element(By.ID, 'ConfirmPassword').send_keys(password)
        self.driver.find_element(By.XPATH, r'//a[@class="button"][text()="Create Account"]').click()
        waitAndClick(self, By.XPATH, r'//a[@class="button"][text()="Submit"]')
        waitForElement(self, *self.menuShop)
        return email
    
    def select_category(self, category):
        self.driver.find_element(*self.menuShop).click()
        self.driver.find_element(By.XPATH, r'//img[@alt="%s"]' % category).click()
        
    def logout(self):
        element = self.driver.find_element(By.XPATH, r'//i[@class="icon icon-user"]')
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()
        self.driver.find_element(By.XPATH, r'//a[@class="logout-menu-item"]').click()
        
        