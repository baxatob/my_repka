#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from home_page import HomePage
from config import baseUrl
from common_methods import *

class Shop(HomePage):
    
    textboxQuantity = (By.ID, 'ProductQty')
    buttonAddToCart = (By.ID, 'btnAddProductToCart')
    buttonRemoveFromCart = (By.XPATH, r'//a[@class="icon icon-close"]')
    buttonYes_alertDialog = (By.XPATH, r'//div[@id="alertDialog"]//a[@class="button"][contains(.,"Yes")]')
    cartUrl = baseUrl+'/Product/Cart'
    counterItems = (By.XPATH, r'//div[@class="badge_circle cartitem-count"]')
    counterPrice = (By.XPATH, r'//strong[@data-bind="money: PriceTotal"]')
        
    def select_product(self, product):
        element = self.driver.find_element(By.XPATH, r'//a[contains(@href, "/ProductDetail/%s")]' % product)
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()
        self.driver.find_element(By.XPATH, r'//a[contains(@href, "/ProductDetail/%s")]//p[@class="button"]' % product).click()
        return self
        
    def add_to_cart(self, quantity):
        self.driver.find_element(*self.textboxQuantity).clear()
        self.driver.find_element(*self.textboxQuantity).send_keys(quantity)
        self.driver.find_element(*self.buttonAddToCart).click()
        waitForElement(self, By.XPATH, r'//div[@class="badge_circle cartitem-count"][text()="%s"]' % quantity)
        return self
    
    def check_content(self, quantity):
        self.driver.get(self.cartUrl)
        try:
            waitForElement(self, By.XPATH, r'//div[@class="badge_circle cartitem-count"][text()="%s"]' % quantity)
        except: raise Exception ('The Cart counter shows incorrect value')
        
    def remove_item_from_cart(self):
        self.driver.find_element(*self.buttonRemoveFromCart).click()
        self.driver.find_element(*self.buttonYes_alertDialog).click()
        