#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import requests
import logging
from bs4 import BeautifulSoup
import lxml.etree as ET

logging.basicConfig(filename='cisco.log', format='%(asctime)s, %(message)s', level=logging.ERROR)

class Track(object):
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
    
    def write(self, i):
        self.tree.write("cisco%s.xml" % i, encoding="UTF-8")

class MergeList(object):
    '''creates a list of xml-files for further merging'''
    def __init__(self):
        self.root = ET.Element("mergeDocs")
        self.tree = ''
    def add_record_to_merge_list(self, fileName):
        field = ET.SubElement(self.root, "doc", path="%s" % fileName)
        self.tree = ET.ElementTree(self.root)
    def write(self):
        self.tree.write("cisco_mergeList.xml", pretty_print=True, encoding="UTF-8")
        
def job_short_description(desc):
    words = desc.split(" ")
    return " ".join(words[:20])
tr = Track()
i = 0
j = 0
xml_files = []
while True:
    rootUrl = 'https://jobs.cisco.com/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow=%s' % i
    rawHtml = requests.get(rootUrl).text
    soupedSite = BeautifulSoup(rawHtml)
    soupedSite = soupedSite.body
    [x.extract() for x in soupedSite.findAll('script')]
    
    if soupedSite.find(id = "attention") == None:   # id="attention" is id of warning, which should appear when the last page was reached  
        allLinks = soupedSite.find_all(class_ = 'jobTitle-link')
        links = []
        for elem in allLinks:
            link = 'https://jobs.cisco.com' + elem.attrs['href']
            links.append(link)
        try:    
            for link in links:
                rawHtml = requests.get(link).text
                soupedPage = BeautifulSoup(rawHtml)
                soupedPage = soupedPage.body
                [x.extract() for x in soupedSite.findAll('script')]
                jobTitle = soupedPage.find(id="job-title").get_text()
                jobLocation = soupedPage.find(id='job-location').get_text()
                jobDesc = soupedPage.find_all("td")[6].get_text()
                shortDesc = job_short_description(jobDesc)
                tr.newJob(jobTitle, jobLocation, "IT/Programming", shortDesc, jobDesc, link)
            if j == 150:        # This block will divide all positions into XML-files, each file will contains 150 positions. 
                tr.write(i)
                tr = Track()
                xml_files.append("cisco%s.xml" % i)
                j = 0
            j += 25
            i += 25
        except: 
            logging.exception(link)
            pass
    else: break

tr.write(i)
xml_files.append("cisco%s.xml" % i)

try:
    xml = MergeList()
    for file_ in xml_files:
        xml.add_record_to_merge_list(file_)
    xml.write()
    dom = ET.parse('cisco_mergeList.xml')
    xslt = ET.parse('merge.xsl')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    f = open('cisco_ALL.xml', 'w')
    f.write(ET.tostring(newdom, encoding="UTF-8"))
    f.close()
except:
    logging.exception('xml files merge')

