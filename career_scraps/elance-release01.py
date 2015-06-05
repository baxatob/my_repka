# -*- coding: UTF-8 -*-
import re
import math
import json
from requests import Session
from urlparse import urlparse
from bs4 import BeautifulSoup

##https://www.elance.com/r/jobs/cat-it-programming/sct-other-it-programming-12350-data-analysis-14174-web-programming-10224-data-science-14176

class Miner:
    def __init__(self, initialLink, nextPageLink, hitsPerPage):
        # hard-coded & non-conditional
        self.browserType = ''
        self.acceptLanguage = 'en-US;q=0.5,en;q=0.3'
        self.acceptEncoding = 'gzip, deflate'
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.contentType = 'text/plain; charset=UTF-8'
        self.session = Session()
        # user-defined
        self.initialLink = initialLink
        self.nextPageLink = nextPageLink
        self.host = urlparse(self.initialLink).hostname
        self.hitsPerPage = hitsPerPage
         # evaluated
        self.totalEntries = 0
        self.kBytes = 0
        #self.startHTML, self.kuka = self.placeGetRequest(self.initialLink)
        print 'Class Miner instance initilized'
        
    def placeGetRequest(self, link):
        headers = {'user-agent': self.browserType,
                   'Connection': 'keep-alive',
                   'Host' : self.host,
                   'Accept-Language' : self.acceptLanguage,
                   'Accept-Encoding' : self.acceptEncoding,
                   'Accept' : self.accept
                  }
        resp = self.session.get(link, headers = headers)
        self.kBytes += len(resp.content)
        #print 'First GET completed.', self.kBytes, 'Bytes'
        return (resp.text, resp.cookies)

class OreTreatment:
    def totalPagesToIterate(self, totalEntries, hitsPerPage):
        pagesTuple = math.modf(1.0*totalEntries/hitsPerPage)
        if pagesTuple[0] > 0:
            tPages = pagesTuple[1] + 1
        else:
            tPages = pagesTuple[1]
        return int(tPages)

    def extractStatistics(self, statText):
        #extracting constants
        cPosted = 'Posted: '
        cEnds = 'Ends: '
        cProposals = 'Proposal'
        for t in statText:
            elem = t.strip()
            dt = elem.find(cPosted)
            end = elem.find(cEnds)
            prop = elem.find(cProposals)
            if dt > -1:
                date = elem[dt + len(cPosted):]
                dt = -1
            if end > -1:
                duration = elem[end + len(cEnds):]
                end = -1
            if prop > -1:
                proposals = re.search('\d+', elem).group(0)
                prop = -1
        return (date, duration, proposals)
    
    def extractProperties(self, props):
        #extracting constants
        cCategory = 'Category:'
        cSkills = 'Skills:'
        txt = props[0].text
        cat = txt.find(cCategory)
        ski = txt.find(cSkills)
        jobCategory = txt[cat+len(cCategory):ski].strip()
        jobSkills = txt[ski+len(cSkills):].strip()
        jobLocation = props[1].text.split('|')[-1].strip()
        return (jobCategory, jobSkills, jobLocation)
    

print 'Started...'
db_file = 'elance.json'
wm = Miner('https://www.elance.com/r/jobs/cat-it-programming/sct-other-it-programming-12350-data-analysis-14174-web-programming-10224-data-science-14176',
           'https://www.elance.com/r/jobs/cat-it-programming/sct-other-it-programming-12350-data-analysis-14174-web-programming-10224-data-science-14176/p-',
           25)
ot = OreTreatment()

cPage = 1
tPages = 10
totalCount = 1
jobDB = []
while cPage <= tPages:
    # debugging stub
    #if cPage > 10:
    #    break
    # requests block
    if cPage == 1:
        link = wm.initialLink
    else:
        link = wm.nextPageLink + str(cPage)
    txt = wm.placeGetRequest(link)[0]
    soup = BeautifulSoup(txt)
    if cPage == 1:
        countt = soup.find('span', class_ = 'resultsDisplay').text.replace(',','')
        wm.totalEntries = int(re.search('\d{2,}', countt).group(0))
        tPages = ot.totalPagesToIterate(wm.totalEntries, wm.hitsPerPage)
        print 'Total jobs:', wm.totalEntries, 'on', tPages, 'pages'

    blocks = soup.findAll('div', class_ = 'jobCard')
    for block in blocks:
        id = block['data-jobid']
        tit = block.find('a', class_ = 'title')
        jobTitle = tit.text.strip()
        jobURL = tit['href']
        jobDescription = block.find('div', id = id + 'Desc').text.strip()
        stat = block.find('div', class_ = 'stats').text.split('|')
        jobDate, jobDuration, proposalsSoFar = ot.extractStatistics(stat)
        props = block.findAll('div', class_ = 'prof')
        jobCategory, jobSkills, jobLocation = ot.extractProperties(props)
        struct = {'Id' : id,
                  'Title': jobTitle,
                  'URL' : jobURL,
                  'Description' : jobDescription,
                  'Date' : jobDate,
                  'Duration' : jobDuration,
                  'Proposals' : proposalsSoFar,
                  'Category' : jobCategory,
                  'Skills' : jobSkills,
                  'Location' : jobLocation
                 }
        jobDB.append(struct)
        print 'job number', totalCount
        totalCount += 1

    f = open(db_file, 'w')
    f.write(json.dumps(jobDB).encode('utf8'))
    f.close()
    print 'Processed page', cPage, 'of total', tPages, '; ', totalCount-1, 'jobs, of total', wm.totalEntries, 'Bytes:', wm.kBytes
    cPage += 1

print 'Work complete!'