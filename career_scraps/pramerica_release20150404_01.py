# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

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
	
def job_short_description(desc):
	""" return the first 20 amount of words instead of truncating """
	words = desc.split(" ")
	return " ".join(words[:20])

##### program entry point	
url = "http://www.pramerica.ie/proxy/proxy.ashx?url=ALL"

f = requests.get(url).text
ff = f[f.find('<?xml'):len(f)-1]
rawXML = BeautifulSoup(ff, 'html.parser')
items = rawXML.find_all('item')

##i = 0
xmlWriter = track()
for item in items:
        #debug stub to break after 4 details
##        i = i + 1
##        if i == 5:
##                break
        rawDesc = item.find('cm:jobdescription')
        stripRawDesc = ''
        for stri in rawDesc.stripped_strings:
                stripRawDesc = stripRawDesc + stri
        singleHtml = BeautifulSoup(stripRawDesc, 'lxml')
        jobDetails = ''
        for stri in singleHtml.stripped_strings:
                jobDetails = jobDetails + '\n' + stri
        jobDetails = jobDetails.encode('ascii','ignore')
        jobTitle = item.find('title').text.encode('ascii','ignore')
        jobLocation = item.find('cm:displaylocation').text.encode('ascii','ignore')
        if jobLocation == '':
                jobLocation = 'not specified'
        jobIndustry = item.find('cm:division').text.encode('ascii','ignore')
        jobLink = item.find('link').text.replace('&amp;', '&')
        xmlWriter.newJob(
                jobTitle,
                jobLocation,
                jobIndustry,
                job_short_description(jobDetails),
                jobDetails,
                jobLink
                )

xmlWriter.tree.write("pramerica.xml")

