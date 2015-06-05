#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import lxml.etree as ET
import json
import logging
import re

logging.basicConfig(filename='apple.log', format='%(asctime)s, %(message)s', level=logging.ERROR)

class Track(object):
        def __init__(self):
                self.root = ET.Element("channel")
                self.tree = ''
        
        def newJob(self, jobTitle, jobLocation, jobIndustry, jobShortDesc, jobDescription, jobLink):
                doc = ET.SubElement(self.root, "job")
                field1 = ET.SubElement(doc, "job_title")
                field1.text = jobTitle
                field2 = ET.SubElement(doc, "job_country")
                field2.text = jobLocation
                field3 = ET.SubElement(doc, "job_industry")
                field3.text = jobIndustry
                field4 = ET.SubElement(doc,"job_short_description")
                field4.text = jobShortDesc
                field5 = ET.SubElement(doc,"job_description")
                field5.text = jobDescription
                field6 = ET.SubElement(doc,"link")
                field6.text = jobLink
                self.tree = ET.ElementTree(self.root)
                
        def write(self, i):
                self.tree.write("apple_%s.xml" % i, encoding="UTF-8")
                
class MergeList(object):
        def __init__(self):
                self.root = ET.Element("mergeDocs")
                self.tree = ''
        def add_record_to_merge_list(self, fileName):
                field = ET.SubElement(self.root, "doc", path="%s" % fileName)
                self.tree = ET.ElementTree(self.root)
        def write(self):
                self.tree.write("apple_mergeList.xml", pretty_print=True, encoding="UTF-8")

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Host": "jobs.apple.com",
        "Connection": "keep-alive"
        }

headers2 = {
        "X-Requested-With": "XMLHttpRequest",
        "X-Prototype-Version": "1.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Referer": "https://jobs.apple.com/us/search",
        "Pragma": "no-cache",
        "Host": "jobs.apple.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*"
        }

def request_body_for_jobId(pageNo):
    return '''searchRequestJson={"searchString":"","jobType":0,"sortBy":"req_open_dt","sortOrder":"1","language":null,"autocomplete":null,\
    "delta":0,"numberOfResults":0,"pageNumber":%s,"internalExternalIndicator":0,"lastRunDate":0,"countryLang":null,\
    "filters":{"locations":{"location":[{"type":0,"code":"USA","countryCode":null,"stateCode":null,"cityCode":null,"cityName":null}]},\
    "languageSkills":null,"jobFunctions":null,"retailJobSpecs":null,"businessLine":null,"hiringManagerId":null},"requisitionIds":null}&clientOffset=120''' % pageNo
                
def request_body_for_details(jobId, attr):
    if attr:
        return 'requisitionId=%s&reqType=REQ&clientOffset=120' % jobId
    else: return 'requisitionId=%s&reqType=PT&clientOffset=120' % jobId

firstRequest = requests.get("https://jobs.apple.com/us/search", headers = headers)
cuka = firstRequest.cookies
jobDB = []
pageNo = 0
# parse for jobID
while True:
    request = requests.post("https://jobs.apple.com/us/search/search-result", cookies=cuka, headers=headers2, data=request_body_for_jobId(pageNo))
    if 'jobId' in request.text:
        content = BeautifulSoup(request.text)
        for i in range(len(content.find_all('jobid'))):
            jobDB.append(content.find_all('jobid')[i].get_text())
        pageNo += 1
    else: break
print ("Total jobs: ", len(jobDB))

pattern = re.compile('[A-Za-z]+')
count = 0
sub_count = 0
xml_files = []
tr = Track()
for id_ in jobDB:
    try:
        if not pattern.match(id_):
            request = requests.post("https://jobs.apple.com/us/requisition/detail.json", cookies=cuka, headers=headers2, data=request_body_for_details(id_, 1))
        else: request = requests.post("https://jobs.apple.com/us/requisition/retaildetail.json", cookies=cuka, headers=headers2, data=request_body_for_details(id_, 0))
        content = json.loads(request.text)
        jobTitle = content['requisitionInfo']['postingTitle']
        if 'locationName' in content['requisitionInfo'].keys():
            jobLocation = content['requisitionInfo']['locationName']+' / '+content['requisitionInfo']['stateAbbr']+' / '+content['requisitionInfo']['countryCode']
        else: jobLocation = content['requisitionInfo']['countryCode']
        jobDescription = content['reqTextFields']['description']+'\nEducation: '+content['reqTextFields']['educationDetails']+'\nQualification: '+content['reqTextFields']['keyQualifications']
        shortDesc = content['jobComments']
        jobLink = 'https://jobs.apple.com/us/search?job=%s&openJobId=%s' % (id_, id_)
        tr.newJob(jobTitle, jobLocation, 'IT/Telecommunications', shortDesc, jobDescription, jobLink)
        count += 1
        sub_count += 1
        if sub_count == 200:
            tr.write(count)
            tr = Track()
            xml_files.append("apple_%s.xml" % count)
            sub_count = 0
    except:
        logging.exception('issue parsing the job ID: %s' % id_)

tr.write(count)
xml_files.append("apple_%s.xml" % count)

xml = MergeList()
for file_ in xml_files:
    xml.add_record_to_merge_list(file_)
xml.write()
dom = ET.parse('apple_mergeList.xml')
xslt = ET.parse('merge.xsl')
transform = ET.XSLT(xslt)
newdom = transform(dom)
f = open('apple_ALL.xml', 'w')
f.write(ET.tostring(newdom, encoding="UTF-8"))
f.close()