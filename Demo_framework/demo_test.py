#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from base_test import AbstractTestCase, unittest, logging
from page_object import StartPage, Item, Registration

class RegistrationWithWrongZIP(AbstractTestCase):
        
    def testing(self):
        try:
            startPage = StartPage(self.driver)
            startPage.click_on_item()
            
            item = Item(self.driver)
            item.select_color_and_qty('Black', 1)
            item.add_to_cart()
            
            page = Registration(self.driver)
            page.registration('wrongZIP')
            
            self.assertTrue(page.zip_alert_displayed())
        except:
            logging.exception("Test failed")
        else:
            logging.info("Test passed")
        
if __name__ == '__main__':
    unittest.main()


    


