#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from base_page import Base
from selenium.webdriver.common.by import By

from config import baseUrl

class TestPage(Base):
    
    textboxName = (By.ID, 'username')
    textboxPassword = (By.ID, 'password') 
    buttonLogin = (By.ID, '_submit')
    
    def login(self, name, password):
        self.sendKeys(name, *self.textboxName)
        self.sendKeys(password, *self.textboxPassword)
        self.clickOn(*self.buttonLogin)
    
        
    
        