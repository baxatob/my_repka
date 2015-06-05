#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests import Session
import html5lib
from bs4 import BeautifulSoup
from bs4 import Tag
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
        self.tree.write("f5.xml", encoding='UTF-8')
##### class ends
def job_short_description(desc):
    """ return the first 20 amount of words instead of truncating """
    words = desc.split(" ")
    return " ".join(words[:20])

##### program entry point
# this is to emulate browser
agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
# urls
initialLink = 'https://www4.recruitingcenter.net/Clients/f5/PublicJobs/controller.cfm'

# initial request to establish session & get cookie
mySession = Session()
response = mySession.get(
    url= initialLink,
    headers={
        'user-agent': agent_str,
        'Host': 'www4.recruitingcenter.net',
        'Connection': 'keep-alive',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
)
kukaInitial = response.cookies

#prepare form data
formData = {
    'State': '',	
    'START': 1,
    'SecondaryCat': '',	
    'SearchJobs': 'Search',
    'ReqNum': '',	
    'Keyword': '',	
    'jbaction': 'JobSearch',
    'esid': 'az',
    'DisplayNumPos': -1,
    'cityName': ''
}

#submit form
response = mySession.post(
    url= initialLink,
    headers={
        'user-agent': agent_str,
        'Referer': initialLink,
        'Host': 'www4.recruitingcenter.net',
        'Connection': 'keep-alive',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    cookies= kukaInitial,
    data= formData
)

#prepare list of jobs from mainpage
partialLink = 'https://www4.recruitingcenter.net/Clients/f5/PublicJobs/' #this is to glue the full link for xml output
indexSoup = BeautifulSoup(response.text, 'html5lib')
indexTable = indexSoup.find('table', summary='this table contains a list of available jobs.')
tBody = indexTable.contents[1]
tBody.contents[0].decompose()
allJobs = []
for elem in tBody.children:
    if isinstance(elem, Tag):
        tt = elem.find_all('td')
        atag = tt[0].find('a')
        alink = atag['href']
        jobTitle = atag.text
        loc1 = tt[2].text.strip()
        loc2 = tt[3].text.strip()
        if loc1.lower() != loc2.lower:
            jobLocation = loc1 + ', ' + loc2
        else:
            jobLocation = loc1
        allJobs.append([jobTitle, jobLocation, partialLink+alink])

#   iterate over sub-pages to get details
xmlWriter = track()
##i = 0
for job in allJobs:
    #debug stub to break after 3 details
##    i = i + 1
##    if i == 4:
##        break
    alink = job[2]
    response = mySession.get(
        url= alink,
        headers={
            'user-agent': agent_str,
            'Referer': initialLink,
            'Host': 'www4.recruitingcenter.net',
            'Connection': 'keep-alive',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        },
        cookies= kukaInitial
    )
    tt = response.text.replace('&middot;', '')
    supik = BeautifulSoup(tt, 'lxml')
    firstTable = supik.find('table', summary='Job profile.')
    detailsTable = firstTable.find_next_sibling('table')
    if detailsTable.find('marquee'):
        detailsTable.find('marquee').decompose()
    jobDetails = ''
    for string in detailsTable.stripped_strings:
        jobDetails = jobDetails + '\n' + string
    #next line is to see if something is going on (for debug)
    #print job[0]

    #NOTE. The site does not provide something like "job field (or type)". Therefore
    #<job_industry></job_industry> tag will be 'Information Tecnologies'
    xmlWriter.newJob(job[0],job[1],"Information Technologies",job_short_description(jobDetails) + "...",jobDetails,job[2])

# final file
xmlWriter.tree.write("f5.xml")




