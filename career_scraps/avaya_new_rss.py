#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import lxml.etree as ET

class track(object):
    def __init__(self):
        self.root = ET.Element("channel")
        self.tree = ''
    def newJob(self,jobtitle,jobcountry,jobindustry,shortdesc,desc,link):
        doc = ET.SubElement(self.root, "job")
        field1 = ET.SubElement(doc, "job_title")
        field1.text = jobtitle
        field2 = ET.SubElement(doc, "job_country")
        field2.text = jobcountry
        field3 = ET.SubElement(doc, "job_industry")
        field3.text = jobindustry
        field4 = ET.SubElement(doc,"job_short_description")
        field4.text = shortdesc
        field5 = ET.SubElement(doc,"job_description")
        field5.text = desc
        field6 = ET.SubElement(doc,"link")
        field6.text = link
        self.tree = ET.ElementTree(self.root)
    
    def write(self):
        self.tree.write("avaya.xml", encoding="UTF-8")
        
def job_short_description(desc):
    words = desc.split(" ")
    return " ".join(words[:20])

rootUrl = 'https://avayacorp.authoria.net/joblist-rss.jsp?erpc=alljobs'
rawHtml = requests.get(rootUrl).text
soupedSite = BeautifulSoup(rawHtml,'xml')
items = soupedSite.find_all('item')

tr = track()
for item in items:
    rawDesc = item.find('description').text
    newDesc = BeautifulSoup(rawDesc)
    jobDesc = newDesc.text
    jobDesc = jobDesc.replace('Apply Here','')
    start = rawDesc.find("Location:")
    end = rawDesc.find("Activation Date:")
    jobLocation = rawDesc[start:end].replace('Location:','').replace('<br>','') 
    jobTitle = item.find('title').text
    jobLink = item.find('link').text
    jobLocation = jobLocation.rstrip().strip()
    shortDesc = job_short_description(jobDesc)
    tr.newJob(jobTitle, jobLocation, "IT/Programming", shortDesc, jobDesc, jobLink)
    
tr.write()
