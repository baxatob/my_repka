#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
#from bs4 import BeautifulSoup
import lxml.etree as ET
import json
import logging

logging.basicConfig(filename='alcatel.log', format='%(asctime)s, %(message)s', level=logging.ERROR)

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
		
	def write(self, i):
		self.tree.write("alcatelucent_%s.xml" % i, encoding="UTF-8")
		
class MergeList(object):
	def __init__(self):
		self.root = ET.Element("mergeDocs")
		self.tree = ''
	def add_record_to_merge_list(self, fileName):
		field = ET.SubElement(self.root, "doc", path="%s" % fileName)
		self.tree = ET.ElementTree(self.root)
	def write(self):
		self.tree.write("alcatel_mergeList.xml", pretty_print=True, encoding="UTF-8")

def requestConstructor(page):
	requestBody = {"fieldData":{"fields":{"KEYWORD":"","LOCATION":""},"valid":"true"},
		 			"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},
																	   {"id":"LOCATION","selectedValues":[]},
																	   {"id":"JOB_FIELD","selectedValues":[]},
																	   {"id":"JOB_TYPE","selectedValues":[]},
																	   {"id":"JOB_SCHEDULE","selectedValues":[]},
																	   {"id":"JOB_LEVEL","selectedValues":[]}]},
		 			"sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"multilineEnabled":"false","pageNo":"%s" % page}
	
	return json.dumps(requestBody)

headers = { 
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Referer": "https://aluperf.taleo.net/careersection/10000/jobsearch.ftl",
        "Pragma": "no-cache",
        "Host": "aluperf.taleo.net",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "865",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
        }
headers2 = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Host": "aluperf.taleo.net",
        "Connection": "keep-alive"
        }

firstRequest = requests.post("https://aluperf.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=640111181", headers = headers, data=requestConstructor(1))
data = json.loads(firstRequest.text)
kuka = firstRequest.cookies
jobAmount = data['pagingData']['totalCount']
pageSize = data['pagingData']['pageSize']
if jobAmount % pageSize == 0:
	totalPages = jobAmount/pageSize
else: totalPages = jobAmount/pageSize + 1
count = 0
sub_count = 0
xml_files = []
xmlWriter = track()
for page in range(1, totalPages+1):
	request = requests.post("https://aluperf.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=640111181", headers = headers, data=requestConstructor(page))
	data = json.loads(request.text)
	for i in range(data['pagingData']['pageSize']):
		try:
			jobLink = 'https://aluperf.taleo.net/careersection/10000/jobdetail.ftl?job=' + data['requisitionList'][i]['contestNo']
			jobTitle = data['requisitionList'][i]['column'][0]
			jobIndustry = 'Information Technologies'
			jobLocation = data['requisitionList'][i]['column'][1].replace('["','').replace('"]','')
			jobDescription = 'You are an accomplished professional with years of experience. You want to apply your knowledge and expertise to exciting new challenges.\
			                  We are a global company that offers superior assignments and opportunities for mobility. We help you chartyour career path, pursue your aspirations and expand your network.\
			                  Take the next step with a career at Alcatel-Lucent. Please follow the link for more details.'
			xmlWriter.newJob(jobTitle, jobLocation, jobIndustry, jobTitle, jobDescription, jobLink)
			count += 1
			sub_count += 1
			if sub_count == 200:
				xmlWriter.write(count)
				xmlWriter = track()
				xml_files.append("alcatelucent_%s.xml" % count)
				sub_count = 0
		except: logging.exception('issue in job parsing: %s' % jobLink)

xmlWriter.write(count)
xml_files.append("alcatelucent_%s.xml" % count)

xml = MergeList()
for file_ in xml_files:
	xml.add_record_to_merge_list(file_)
xml.write()
dom = ET.parse('alcatel_mergeList.xml')
xslt = ET.parse('merge.xsl')
transform = ET.XSLT(xslt)
newdom = transform(dom)
f = open('alcatel_ALL.xml', 'w')
f.write(ET.tostring(newdom, encoding="UTF-8"))
f.close()





