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
        self.tree.write("iquate.xml", encoding="UTF-8")

def urlPageIs404(alink):
    """checks if the page under link is "Error 404 Page". Returns True if blank page"""
    pageBlank = False
    rawHtml = requests.get(alink).text
    soupedSite = BeautifulSoup(rawHtml)
    soupedSite = soupedSite.body
    if soupedSite.find_all(text=re.compile('Error 404 Page')):
        pageBlank = True
    return pageBlank


#**** program entry point ********
# constants
mainPageKeyword = "Current Roles"
markupTag = 'div'

#get mainpage and soupe it
rootUrl = "http://www.iquate.com/career-opportunities-2"
rawHtml = requests.get(rootUrl).text
soupedSite = BeautifulSoup(rawHtml)
soupedSite = soupedSite.body
#remove scripts
[x.extract() for x in soupedSite.findAll('script')]
# instantiate XML maker class
tr = track()
#find element which contains keyword
elem = soupedSite.find_all(text=re.compile(mainPageKeyword))[0]
#determine nearest markup tag
for upLevel in elem.parents:
    if upLevel.name == markupTag:
        jobListSection = upLevel
        break
#collect links within jobListSection
jobLinks = []
for jobLink in jobListSection.find_all('a'):
    if jobLink.get('href').startswith("http://"):
        jobLinks.append(jobLink)
#iterate trough every link to grab target contents
for jobLink in jobLinks:
    if not urlPageIs404(jobLink.get('href')):
        #get target page
        rawHtml = requests.get(jobLink.get('href')).text
        soupedSite = BeautifulSoup(rawHtml)
        #before cleanup target page, grag Short Job Description from <meta> tag
        valueShortDesc = soupedSite.find('meta', {"name": "description"}).get("content")
        #page cleanup and remove scripts
        soupedSite = soupedSite.body
        [x.extract() for x in soupedSite.findAll('script')]
        #collect fields before "description"
        keyRole = soupedSite.find_all(text=re.compile("Role:"))[0]
        keyRole = keyRole.parent
        valueRole = keyRole.next_sibling
        keyRole = keyRole.parent
        keyLocation = soupedSite.find_all(text=re.compile("Location:"))[0]
        keyLocation = keyLocation.parent
        valueLocation = keyLocation.next_sibling
        keyLocation = keyLocation.parent
        keyTheRole = soupedSite.find_all(text=re.compile("The Role"))[0]
        keyTheRole = keyTheRole.parent
        iterat = keyTheRole.parent
        #glue description text until "About iQuate" is reached
        desc = ""
        while True:
            iterat = iterat.next_sibling
            try:
                if iterat.text == "About iQuate":
                    break
                desc += iterat.text + "\n"
            except AttributeError:
                continue
        #instantiate XML element
        tr.newJob(valueRole,
                  valueLocation,
                  "IT/Programming",
                  valueShortDesc,
                  desc,
                  jobLink.get('href')
                  )
#flush XML to file
tr.write()        















