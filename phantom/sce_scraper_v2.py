#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import sys
import json
import time
import logging
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Input data:
timeout = 15
startdate = 'Dec 01, 2014'
enddate = 'Mar 30, 2015'

credentials = [{'login':'stephanie.yanchinski@caltech.edu', 'password':'Quebecrules15!'}]

#Global variables:
time_format = '%b %d, %Y'

class GenericUtility(object):
    def __init__(self):
        '''Initialize whatever is needed, selenium, requests session etc etc'''
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS()
        #self.driver.set_window_size(1600, 900)
        self.driver.maximize_window()
        self.driver.implicitly_wait(timeout)
                
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
        
    def wait_for_element(self, locator, value, timeout_=15):
        '''wait for expected element and raise timeout exception if element will not presented '''
        WebDriverWait(self.driver, timeout_).until(EC.presence_of_element_located((locator, value)))

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
        self.driver.find_element(By.XPATH, r'//table[@id="ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_SmartConnectSAListGrid"]\
                                            //td[contains(.,"%s")]/preceding-sibling::td[1]//input' % meter_id).click()
        
        self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceHolder_DownloadButton').click()
        time.sleep(timeout) #wait to generate and download the file
        
    
    def get_meters(self):
        '''Tries to get the meters associated with this account.  Should collect meter's address, service account number, meter number, rates, type of account and store it in a list of dictionary:
        Such that len(self.meters) == number of meters associated with this account. yes this works for a dict.
        returns a list.
        '''
        try:
            self.driver.find_element(By.XPATH, r'//span[contains(.,"Services")]/ancestor::a').click()
            self.driver.find_element(By.XPATH, r'//span[contains(.,"Services")]/ancestor::a').click() # Second click requires to load data about enrolled programs.
            self.acc_number = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_LoginBoxPlace_LoginControl_AccountNumber').text
            self.acc_type = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_LoginBoxPlace_LoginControl_RateLink').text
            if self.is_element_presented(By.XPATH, r'//span[@id[contains(.,"EnrolledProgramText")]]/a'):
                self.enrolled = self.driver.find_element(By.XPATH, r'//span[@id[contains(.,"EnrolledProgramText")]]/a').text
            else: self.enrolled = 'No enrolled programs'
            self.driver.find_element(By.XPATH, r'//span[contains(.,"My Property")]/ancestor::a').click()
            self.address = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceTab_UserControl0_LblServiceAddress').text
            self.service_accNumber = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceTab_UserControl0_LblServiceAcctNumber').text
            self.footage = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceTab_UserControl0_AnswerDiv1').text
            return {
                    'user_account_number':self.acc_number,
                    'address':self.address,
                    'service_account_number':self.service_accNumber,
                    'footage':self.footage,
                    'account_type':self.acc_type,
                    'enrolled_program':self.enrolled
                    }
        except:
            logging.exception("Error while getting the property")
            self.driver.get_screenshot_as_file('%s.jpg' % time.strftime('%d_%b_%Y_%H-%M-%S'))
            self.driver.quit()

    def get_bills(self, starttime, endtime, address = None, meter_id = None):
        '''Get the bills associated with the provided address or meter_id.  
        starttime and endtime specify the range.  If both are None, it should return ALL available bills'''
        try:
            self.data_ = []
            self.driver.find_element(By.XPATH, r'//span[contains(.,"My Account Home")]/ancestor::a').click()
            self.driver.find_element(By.XPATH, r'//h3//span[contains(.,"Usage")]/ancestor::a').click()
            self.driver.find_element(By.LINK_TEXT, 'Billed Months').click()
            
            self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_BillMonthCal_CalendarImage').click()
            
            # Here we get all time intervals and extract JavaScript commands to load each interval on the page:
            all_records = self.driver.find_elements(By.XPATH, r'//a[@class="toolTipCalendar"][@onclick[contains(.,"SetselectedPeriod")]]')
            scripts = []
            for rec in all_records: 
                script = rec.get_attribute('href')
                script = script.replace("javascript:", "").replace("%20", " ")
                if script not in scripts:
                    scripts.append(script)
                    
            if starttime == None:
                self.starttime = 'Jan 01, 2000'
                s1 = time.strptime(self.starttime, time_format)
            else: s1 = time.strptime(starttime, time_format)
            if endtime == None:
                self.endtime = date(date.today().year, date.today().month, date.today().day).strftime(time_format)
                e1 = time.strptime(self.endtime, time_format)
            else: e1 = time.strptime(endtime, time_format)
                            
            for script in scripts:
                period_start = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{1,2}, [0-9]{4}', script)
                period_start = period_start.group(0)
                s2 = time.strptime(period_start, time_format)
                period_end = re.search(' (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{1,2}, [0-9]{4}', script)
                period_end = period_end.group(0)
                period_end = period_end.replace(" ", "", 1)
                e2 = time.strptime(period_end, time_format)
                                
                if s1 <= s2 <= e1 and s1 <= e2 <= e1:
                    self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_BillMonthCal_CalendarImage').click()    
                    period_expected = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{1,2}, [0-9]{4} - (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{1,2}, [0-9]{4}', script)
                    period_expected = period_expected.group(0)
                    
                    self.driver.execute_script(script) #JavaScript execution
                    
                    self.wait_for_element(By.XPATH, r'//span[@class="billDate"][contains(.,"%s")]' % period_expected, 150) # Waiting to load the data for the determined period
                    self.wait_for_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_BilledMonthReportDate')
                    billing_period = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_BilledMonthReportDate').text
                    #self.driver.get_screenshot_as_file("%s.jpg" % period_expected)
                    if self.is_element_presented(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_ErrorMessage'):
                        record = {'billing_period':billing_period,
                                  'billing_usage':'data is unavailable',
                                  'billing_cost':'data is unavailable'}
                    else:
                        billing_usage_text = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_TotalUsage').text
                        billing_usage = re.search('[0-9,]+ kWh', billing_usage_text)
                        billing_cost_text = self.driver.find_element(By.ID, 'ctl00_ctl00_ctl00_EscBaseMasterCentralPlace_CentralContentPlace_CentralContentPlaceInnerTab_BilledCost').text
                        billing_cost = re.search('[$0-9.]+', billing_cost_text)
                        record = {'billing_period':billing_period,
                                  'billing_usage':billing_usage.group(0),
                                  'billing_cost':billing_cost.group(0)}
                    
                    self.data_.append(record)
                    with open("Usage.json", "w") as file_:
                        file_.write(json.dumps(self.data_))
            return self.data_
        except:
            logging.exception("Error while getting the bill")
            self.driver.get_screenshot_as_file('%s.jpg' % time.strftime('%d_%b_%Y_%H-%M-%S'))
            return self.data_

if __name__ == '__main__':
    logging.basicConfig(filename='script_v2.log', format='%(asctime)s, %(message)s', level=logging.ERROR)
        
    dates = [startdate, enddate] #Quick check for correct date format
    for date_ in dates:
        if date_ != None: 
            try:
                datetime.datetime.strptime(date_, time_format)
            except:
                logging.exception("Please check the date format. SHOULD BE: Jan 01, 2015")
                sys.exit()
            
    for user in credentials:
        utility = GenericUtility()
        login = utility.login(user)
        if login == "failed":
            logging.exception("Login failed, user: %s" % user['login'])
            utility.driver.quit()
        else:
            property_ = utility.get_meters()
            usage = utility.get_bills(startdate, enddate)
            utility.logout()
            utility.driver.quit()
                        
            result = [property_, usage]    
            with open("%s.json" % property_['user_account_number'], "w") as file_:
                file_.write(json.dumps(result))
            print "Parsing for Account# %s completed" % property_['user_account_number']        
        