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
        self.tree.write("avaya.xml", pretty_print=True, encoding='cp1252')
        


rootUrl = 'https://avayacorp.authoria.net/joblist.html?quicksearch-all=1&ERFormID=newjoblist&ERFormCode=3.2697127323162722'
rawHtml = requests.get(rootUrl).text
soupedSite = BeautifulSoup(rawHtml)
soupedSite = soupedSite.body

[x.extract() for x in soupedSite.findAll('script')]

tr = track()

allLinks = soupedSite.find_all(href = re.compile('viewjob.html'))
links = []
for elem in allLinks:
    link = 'https://avayacorp.authoria.net/' + elem.attrs['href'][:71]
    links.append(link)

for link in links:
    rawHtml = requests.get(link).text
    soupedPage = BeautifulSoup(rawHtml)
    soupedPage = soupedPage.body
    [x.extract() for x in soupedSite.findAll('script')]
    jobTitle = soupedPage.find(class_ = 'pageheading').get_text()
    p = soupedPage.find_all('p')
    jobDesc=''
    for item in p:
        jobDesc = jobDesc + item.get_text() + '\n'
    labels = soupedPage.find_all(class_ = 'formlabel')
    for i in labels:
        if i.string == 'Location':
            target = i.parent.find_next_sibling()
            jobLocation = target.find(class_ = "sectionbody").get_text()
        if i.string == 'Job Function':
            target = i.parent.find_next_sibling()
            jobFunc = target.find(class_ = "sectionbody").get_text()
        if i.string == 'Job Level':
            target = i.parent.find_next_sibling()
            jobLevel = target.find(class_ = "sectionbody").get_text()
    tr.newJob(jobTitle, jobLocation, "IT/Programming", jobFunc+' - '+jobLevel, jobDesc, link)
tr.write()   