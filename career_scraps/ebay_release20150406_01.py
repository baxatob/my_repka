#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import time
import requests
import logging
from bs4 import BeautifulSoup
import lxml.etree as ET

logging.basicConfig(filename='eBay.log', format='%(asctime)s, %(message)s', level=logging.ERROR)

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
        self.tree.write("eBay%s.xml" % i, encoding="UTF-8")
        
class MergeList(object):
    '''creates a list of xml-files for further merging'''
    def __init__(self):
        self.root = ET.Element("mergeDocs")
        self.tree = ''
    def add_record_to_merge_list(self, fileName):
        field = ET.SubElement(self.root, "doc", path="%s" % fileName)
        self.tree = ET.ElementTree(self.root)
    def write(self):
        self.tree.write("eBay_mergeList.xml", pretty_print=True, encoding="UTF-8")
        
def job_short_description(desc):
    words = desc.split(" ")
    return " ".join(words[:20])

initialLink = 'https://jobs.ebayinc.com/api/jobs?limit=1&offset=460&page=1'

firstRequest = requests.get(initialLink)
content = json.loads(firstRequest.text)
jobCount = int(content['count']) # get total number of job positions
initialLink = 'https://jobs.ebayinc.com/api/jobs?limit=%s' % jobCount
resp = requests.get(initialLink)
time.sleep(30) # waiting for page load, because we load all data in one JSON file
content = json.loads(resp.text) 
all_jobs_on_page = content['jobs']
xml_files = []
j = 0
tr = Track()
for i in range(jobCount):
    try:
        if 'brand' in all_jobs_on_page[i].keys():
            jobTitle = all_jobs_on_page[i]['title']+' in '+all_jobs_on_page[i]['brand']
        else: jobTitle = all_jobs_on_page[i]['title']
        jobCategory = all_jobs_on_page[i]['categories'][0]['name']
        jobLocation = all_jobs_on_page[i]['country']+', '+all_jobs_on_page[i]['location']
        jobLink = 'https://jobs.ebayinc.com/jobs/'+all_jobs_on_page[i]['slug']+'/'+all_jobs_on_page[i]['seo_title']
        rawDesc = BeautifulSoup(all_jobs_on_page[i]['description'])
        rawDesc = rawDesc.find_all('li')
        jobDesc = ''
        for li in rawDesc:
            jobDesc = jobDesc + li.text
        shortDesc = job_short_description(jobDesc)
        tr.newJob(jobTitle, jobLocation, jobCategory, shortDesc, jobDesc, jobLink)
        if j == 200:
            tr.write(i)
            tr = Track()
            xml_files.append("eBay%s.xml" % i)
            j = 0
        i += 1
        j += 1
    except:
        logging.exception('issue in job parsing: %s' % jobLink)

tr.write(i)
xml_files.append("eBay%s.xml" % i)
            
try:
    xml = MergeList()
    for file_ in xml_files:
        xml.add_record_to_merge_list(file_)
    xml.write()
    dom = ET.parse('eBay_mergeList.xml')
    xslt = ET.parse('merge.xsl')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    f = open('eBay_ALL.xml', 'w')
    f.write(ET.tostring(newdom, encoding="UTF-8"))
    f.close()
except:
    logging.exception('issue in xml files merging')

