#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from config import *
from base_test import AbstractTestCase, unittest, logging
from pages.home_page import HomePage
from pages.shop import Shop
from common_methods import screenShot

class DemoTest(AbstractTestCase):
        
    def testing(self):
        try:
            page = HomePage(self.driver)
            account = page.account_registration()
            logging.info('Created account with username: %s' % account)
            page.select_category(health)
            page = Shop(self.driver)
            item = page.select_product('anti-aging-collection')
            cart = item.add_to_cart(2)
            cart.check_content('2') # <----------- YOU CAN CHANGE THIS VALUE TO SEE HOW TEST WILL FAIL           
            cart.remove_item_from_cart()
            cart.check_content('0')
            page.logout()
        except:
            logging.exception("%s failed" % self.__class__.__name__)
            screenShot(self)
            print "%s failed" % self.__class__.__name__
        else:
            logging.info("%s passed" % self.__class__.__name__)
            print "%s passed" % self.__class__.__name__
        
if __name__ == '__main__':
    unittest.main()