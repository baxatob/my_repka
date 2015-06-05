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

def requestPagePost(session, alink, pageNo, kuka, industryID):
    # this is to emulate browser
    agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
    # this is a structure to be converted to json to pass to get listPage
    # list page number should be set via dat['pageNo'] = <number>
    listPageStruct = {
      "advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION", "selectedValues":[]},
                                                                       {"id":"LOCATION", "selectedValues":[]},
                                                                       {"id":"JOB_FIELD", "selectedValues":[]},
                                                                       {"id":"URGENT_JOB", "selectedValues":[]},
                                                                       {"id":"EMPLOYEE_STATUS", "selectedValues":[]},
                                                                       {"id":"STUDY_LEVEL", "selectedValues":[]},
                                                                       {"id":"WILL_TRAVEL", "selectedValues":[]},
                                                                       {"id":"JOB_SHIFT", "selectedValues":[]},
                                                                       {"id":"JOB_NUMBER", "selectedValues":[]}
                                                                      ]
                                            },
      "fieldData":{"fields":{"KEYWORD":"", "LOCATION":"", "JOB_NUMBER":""},
                   "valid":True
                  },
      "filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE", "selectedValues":[]},
                                                        {"id":"LOCATION", "selectedValues":[]},
                                                        {"id":"JOB_FIELD", "selectedValues":[]},
                                                        {"id":"JOB_TYPE", "selectedValues":[]}
                                                       ]
                             },
      "sortingSelection":{"sortBySelectionParam":"3", "ascendingSortingOrder":"false"},
      "multilineEnabled":False,
      "pageNo":pageNo
    }
    ind = int(industryID)
    if ind != 0:
        listPageStruct['advancedSearchFiltersSelectionParam']['searchFilterSelections'][2]['selectedValues'].append(ind)
    # convert to json
    listPageQuery = json.dumps(listPageStruct, skipkeys=False, sort_keys=True, separators=(',', ':'))
    # perform request
    response = session.post(
        url= alink,
        data= listPageQuery,
        cookies= kuka,
        headers={
            'user-agent': agent_str,
            'Referer': 'https://bmcsoftware.taleo.net/careersection/bmc_external/jobsearch.ftl',
            'X-Requested-With': 'XMLHttpRequest',
            'Host':	'bmcsoftware.taleo.net',
            'Content-Type':	'application/json; charset=UTF-8',
            'Content-Length': len(listPageQuery),
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
    )
    txt = json.loads(response.text)
    output = dict(txt)
    return output

def appendToDB(DB, entry, industry):
    struct = {'jobTitle' : entry['column'][0],
              'jobIndustry' : industry['text'],
              'jobLocation' : entry['column'][1][2:-2],
              'shortDesc' : ' ',
              'jobDescription' : ' ',
              'jobId' : entry['jobId'],
              'contestNo' : entry['contestNo'],
              'jobLink': 'https://bmcsoftware.taleo.net/careersection/bmc_external/jobdetail.ftl' + '?job=' + entry['contestNo'],
              'status' : 'OK'
    }
    DB.append(struct)

def getDetails(sessia, url):
    
    agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
    headers = {'user-agent': agent_str,
               'Connection': 'keep-alive'}
    #sessia = Session()
    resp = sessia.get(url, headers=headers)#, cookies=kuka)
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
        
        i = 0
        size = len(argList)
        while (i < size and argList[i][:3] != '!*!'):
            i += 1
        
        startExtract = 3 #if description field starts with !*!, discard it
        # there are cases when no !*! markup is used. Then:
        if i == size:
            i = 17
            startExtract = 0
       
        percents = argList[i]
        rawHtml = urllib.unquote(percents[startExtract:len(percents)])
        rawHtml = rawHtml.replace('\n', '').replace(u'\xa0', u' ').replace(u'\xb7', u'-').replace(u'\t', u'')
        soup = BeautifulSoup(rawHtml, 'lxml')
        
        output = ''
        for strin in soup.stripped_strings:
            if strin[:4] != u'<!--':
                lineBrake = '\n'
                if strin == u' ':
                    lineBrake = ' '
                if len(strin.split(" ")) < 2:
                    lineBrake = ' '
                output = output + strin.encode('ascii', 'xmlcharrefreplace') + lineBrake
       
        output = output.replace(u'\xa0', u' ')
    else:
        output = 'Na'
    return output

# ######## program entry point ******************
# this is to emulate browser
agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
# urls
initialLink = 'https://bmcsoftware.taleo.net/careersection/bmc_external/jobsearch.ftl'
indexPageLink = 'https://bmcsoftware.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'
detailLink = 'https://bmcsoftware.taleo.net/careersection/bmc_external/jobdetail.ftl'

# initial request - get cookie
session = Session()
headers = {'user-agent': agent_str, 'Connection': 'keep-alive'}
resp = session.get(initialLink, headers=headers)
kuka = resp.cookies

# second request via POST
indexData = requestPagePost(session, indexPageLink, 1, kuka, 0)
industries = indexData['facetResults'][0]['facetValueResults']
totalRecords = 0
totalInIndustry = 0

jobDB = []
count = 1

for industry in industries:
    entriesProcessed = 0
    pageNumber = 1
    once = 1
    industryName = industry['text']
    industryID = industry['id']
    while True:
        jobList = requestPagePost(session, indexPageLink, pageNumber, kuka, industryID)
        totalInIndustry = int(jobList['pagingData']['totalCount'])
        if once:
            totalRecords += totalInIndustry
            once = 0
        for entry in jobList['requisitionList']:
            #print 'rec:', count, ' of:', totalRecords, ' # within category:', entriesProcessed, ' fld:', industry['text']
            appendToDB(jobDB, entry, industry)
            entriesProcessed += 1
            count += 1
        pageNumber += 1
        if not entriesProcessed < totalInIndustry:
            break

#print 'collected ', count-1, ' indexes, in database should be ', totalRecords
count = 1
for job in jobDB:
    job['jobDescription'] = getDetails(session, job['jobLink'])
    if job['jobDescription'] == 'Na':
        job['status'] = 'Error'
    #print 'rec:', count, ' of:', totalRecords, ' ID:', job['contestNo'], '|', job['jobDescription'][:80] + '...'
    count += 1

# write xml
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
xmlWriter.tree.write("bmc.xml")
