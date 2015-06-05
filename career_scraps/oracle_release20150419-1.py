import json
import requests
import urllib
from requests import Session
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
        
def job_short_description(desc):
    """ return the first 20 amount of words instead of truncating """
    words = desc.split(" ")
    return " ".join(words[:20])

def GetPost(sessia, alink, sup, page):
    frm = sup.find('form', attrs = {'name':'ftlform'})
    payload = {}
    count = 1
    inputs = frm.findAll('input', attrs = {'type':'hidden'})
    for inp in inputs:
        if 'name' in inp.attrs:
            if inp['id'] == inp['name']:
                key = inp['name']
                value = inp['value']
                payload[key] = value
                count += 1
    
    payload['actNbElementByPage.target'] = ''
    payload['dropListSize'] = 100
    payload['dropSortBy'] = 10
    payload['jobfield1'] = 140430775
    payload['jobfield1L1'] = 140430775
    payload['jobNumberSearch'] = ''
    payload['keyword'] = ''
    payload['languageSelect'] = 'en'
    payload['location1'] = ''
    payload['location1L1'] = -1
    payload['nameValue'] = ''
    payload['postedDate'] = 'com.taleo.careersection.entity.lookup.PostedDate__0'
    
    payload['countryPanelErrorDrawer.state'] = 'false'
    payload['errorMessageDrawer.state'] = 'false'
    payload['focusOnField'] = 'requisitionListInterface.dropListSize'
    payload['ftlcompclass'] = 'PageComponent'
    payload['ftlcompid'] = 'actNbElementByPage'
    payload['ftlinterfaceid'] = 'requisitionListInterface'
    payload['ftlwinscr'] = '1051'
    payload['jobFieldMenu.selected'] = 'tabJobField'
    payload['jobTypeMenu.selected'] = 'jobTypeTab'
    payload['jsfCmdId'] = 'actNbElementByPage'
    payload['locationMenu.selected'] = 'tabLocation'
    payload['postedDateMenu.selected'] = 'postedDateTab'
    payload['radiusSiteListDrawer.state'] = 'false'
    payload['restoreInitialHistoryOnRefresh'] = 'true'
    payload['tz'] = 'GMT%252b04%3A00'
    payload['udf5Menu.selected'] = '0'
    payload['willTravelMenu.selected'] = 'willTravelTab'
    payload['zipcodePanelErrorDrawer.state'] = 'false'
    
    payload['rlPager.currentPage'] = page
    
    
    response = sessia.post(
        url= alink,
        data= payload,
        
        headers={
            'user-agent': agent_str,
            'Referer': 'https://oracle.taleo.net/careersection/2/moresearch.ftl',
            
            'Host':	'oracle.taleo.net',
            
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    )
    return response.text

def appendToDB(DB, entry):
    struct = {'jobTitle' : entry[4],
              'jobIndustry' : '',
              'jobLocation' : entry[12],
              'shortDesc' : ' ',
              'jobDescription' : ' ',
              #'jobId' : entry['jobId'],
              #'contestNo' : entry['contestNo'],
              'jobLink': urllib.unquote(entry[39]),
              'status' : 'OK'
    }
    DB.append(struct)

def getRecords(txta):
    startStr = u"api.fillList('requisitionListInterface', 'listRequisition', ["
    ssLen = len(startStr)
    found = txta.find(startStr)
    if found > 0:
        stri = txta[found+ssLen:len(txta)]
        count = 1
        pos = 0
        while (pos < len(stri) and count != 0):
            if stri[pos] == '[':
                count += 1
            if stri[pos] == ']':
                count -= 1
            pos += 1
        extract = stri[:pos - 1]
        argList = extract.split("','")
    
    i = 0
    adder = 42
    nextStart = i + adder
    record = []
    records = []
    for elem in argList:
        if i == nextStart:
            nextStart += adder
            record = []
        record.append(elem)
        if len(record) == adder:
            records.append(record)
        i += 1
    return records

def getDetails(alink):
    session = Session()
    headers = {'user-agent': agent_str, 'Connection': 'keep-alive'}
    resp = session.get(alink, headers=headers)
    startStr = u"api.fillList('requisitionDescriptionInterface', 'descRequisition', ["
    ssLen = len(startStr)
    found = resp.text.find(u"api.fillList('requisitionDescriptionInterface', 'descRequisition', [")
    
    if found > 0:
        stri = resp.text[found+ssLen:len(resp.text)]
        count = 1
        pos = 0
        while (pos < len(stri) and count != 0):
            if stri[pos] == '[':
                count += 1
            if stri[pos] == ']':
                count -= 1
            pos += 1
        extract = stri[:pos - 1]
        argList = extract.split("','")
        desc = argList[16]
        fld = argList[18]
        if desc[:3] == '!*!':
            desc = desc[3:len(desc)]
        desc = urllib.unquote(desc)
        if desc[:4] == u'<!--':
            desc = 'Na'
        tup = (desc, fld)
    else:
        tup = ('Na', 'Na')
    return tup


agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
initialLink = 'https://oracle.taleo.net/careersection/2/moresearch.ftl'
indexPageLink = 'https://oracle.taleo.net/careersection/2/moresearch.ftl'


session = Session()
headers = {'user-agent': agent_str, 'Connection': 'keep-alive', 'Host': 'oracle.taleo.net'}
resp = session.get(initialLink, headers=headers)
kuka = resp.cookies

soup0 = BeautifulSoup(resp.text)
selects = soup0.find('select', id='advancedSearchInterface.jobfield1L1')
opts = selects.findAll('option')

txt1 = GetPost(session, indexPageLink, soup0, 1)
soup1 = BeautifulSoup(txt1)

txt2 = GetPost(session, indexPageLink, soup1, 2)
soup2 = BeautifulSoup(txt2)

txt3 = GetPost(session, indexPageLink, soup2, 3)
soup3 = BeautifulSoup(txt3)

txt4 = GetPost(session, indexPageLink, soup3, 4)
soup4 = BeautifulSoup(txt4)


rawRecords = []
rawRecords += getRecords(txt1)
rawRecords += getRecords(txt2)
rawRecords += getRecords(txt3)
rawRecords += getRecords(txt4)



jobDB = []
for el in rawRecords:
    appendToDB(jobDB, el)
    


i = 0
for job in jobDB:
    txt = getDetails(job['jobLink'])
    jobDB[i]['jobDescription'] = txt[0]
    jobDB[i]['jobIndustry'] = txt[1]
    if txt[0] == 'Na':
        jobDB[i]['status'] = 'Error'
    
    i += 1

xmlWriter = track()
for record in jobDB:
    if record['status'] == 'OK':
        xmlWriter.newJob(
                         record['jobTitle'],
                         record['jobLocation'],
                         record['jobIndustry'],
                         job_short_description(record['jobDescription']) + "...",
                         record['jobDescription'],
                         record['jobLink']
                        )
# final file
xmlWriter.tree.write("oracle.xml")

huj = 1



