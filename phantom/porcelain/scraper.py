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
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((locator, value))) 
            return True
        except: return False
        
logging.basicConfig(filename='porcelain.log', format='%(asctime)s, %(message)s', level=logging.ERROR)
driver = webdriver.Firefox()
driver.implicitly_wait(15)


"""driver.get('http://auction.artron.net/BJCX-0144/PMH206210/PZ2024943/')

lot_links = []
page_links = []
page_links_raw = driver.find_elements(By.XPATH, r'//div[@class="result-page"]//a[@href[contains(.,"BJCX-0144/PMH206210/")]]')

for el in page_links_raw:
    link = el.get_attribute('href')
    if link not in page_links and 'javascript' not in link:
        page_links.append(link)
        
       
for link in page_links:
    driver.get(link)
    raw_links = driver.find_elements(By.XPATH, r'//a[@href[contains(.,"/paimai-art")]]')
    for el in raw_links:
        lot_link = el.get_attribute('href')
        if lot_link not in lot_links and 'javascript' not in lot_link:
            lot_links.append(lot_link)
            
with open("LOT_URLs.json", "w") as file_:
    file_.write(json.dumps(lot_links))"""

with open("LOT_URLs.json", "r") as file_:
    lot_links = json.load(file_)

DB = []

for link in lot_links:
    try:
        driver.get(link)
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
            currency = 'Not defined'
            lowEstimate = 'Not defined'
            highEstimate = price
            
        record = {
                  "URL":link,
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
        with open("PORCELAIN.json", "w") as file_:
            file_.write(json.dumps(DB))
    except:
        logging.exception('error')
    
driver.quit()
print "Done with %s records" % len(DB)
