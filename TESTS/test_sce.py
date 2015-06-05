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

def is_element_presented(locator, value):
        '''check if element presented in DOM'''
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((locator, value))) 
            return True
        except: return False
        

logging.basicConfig(filename='porcelain.log', format='%(asctime)s, %(message)s', level=logging.ERROR)
driver = webdriver.Firefox()
driver.implicitly_wait(15)

    
driver.get('http://auction.artron.net/paimai-art0046580719/')
imageURL = driver.find_element(By.ID, "smallPic").get_attribute('src')
saleName = driver.find_element(By.XPATH, r'//table//tr[6]/td[2]/a').text
saleDate = driver.find_element(By.XPATH, r'//table//tr[5]/td[2]/em').text
date_ = driver.find_element(By.XPATH, r'//table//tr[2]/td[2]').text
lotNum = re.search('\d+', driver.find_element(By.TAG_NAME, 'h1').text)
lotNum = lotNum.group(0)
price = driver.find_element(By.XPATH, r'//table//tr[3]/td/em').text
size = driver.find_element(By.XPATH, r'//table//tr[1]/td[2]').text
if 'cm' in size:
    size = size.replace('cm', '')
unit = 'cm'
artist = driver.find_element(By.XPATH, r'//table//tr[1]/td[1]').text
title = driver.find_element(By.TAG_NAME, 'h1').text
if is_element_presented(By.XPATH, r'//table//tr[7]/td'):
    description = driver.find_element(By.XPATH, r'//table//tr[7]/td').text
else: description = 'Not defined'
if is_element_presented(By.XPATH, r'//table//tr[8]/td'):
    literature = driver.find_element(By.XPATH, r'//table//tr[8]/td').text
else: literature = 'Not defined'

currency = re.search('\w+', price)
if currency != None:
    currency = currency.group(0)
    lowEstimate = re.search('[0-9,]+', price)
    lowEstimate = int(lowEstimate.group(0).replace(',', ''))
    highEstimate = re.search('-[0-9,]+', price)
    highEstimate = int(highEstimate.group(0).replace(',', '').replace('-', ''))
else: 
    currency = price
    lowEstimate = 'Not defined'
    highEstimate = 'Not defined'

DB = []    
record = {
          "URL":'http://auction.artron.net/paimai-art0046580719/',
          "image":imageURL,
          "saleName":saleName,
          "saleDate":saleDate,
          "lotNum":lotNum,
          "currency":currency,
          "lowEstimate":lowEstimate,
          "highEstimate":highEstimate,
          "size":size,
          "unit": unit,
          "date":date_,
          "artist":artist,
          "title":title,
          "literature":literature,
          "description":description
          }

DB.append(record)
with open("missed.json", "w") as file_:
            file_.write(json.dumps(DB))