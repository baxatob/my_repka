# -*- coding: utf-8 -*-
import urllib
import requests
from requests import Session
import html5lib
from bs4 import BeautifulSoup
from bs4 import Tag

def getUrlEncodedHashData(soupObject):
    dermo1 = soupObject.find('input', id='com.salesforce.visualforce.ViewState')['value']
    dermo2 = soupObject.find('input', id='com.salesforce.visualforce.ViewStateVersion')['value']
    dermo3 = soupObject.find('input', id='com.salesforce.visualforce.ViewStateMAC')['value']
    pardict = {
               'AJAXREQUEST':'j_id0:j_id1:atsForm:j_id71',
               'j_id0:j_id1:atsForm':'j_id0:j_id1:atsForm',
               'j_id0:j_id1:atsForm':'j_id32:0:searchCtrl=',
               'j_id0:j_id1:atsForm':'j_id32:1:searchCtrl=',
               'com.salesforce.visualforce.ViewState':dermo1,
               'com.salesforce.visualforce.ViewStateVersion':dermo2,
               'com.salesforce.visualforce.ViewStateMAC':dermo3,
               'j_id0:j_id1:atsForm:j_id117':'j_id0:j_id1:atsForm:j_id117'
              }
    urlEncodedParams = urllib.urlencode(pardict)
    return urlEncodedParams

def nextPageFetchTextPost(aLink, urlEncodedParams, kuka):
    resp = session.post(
        url= aLink,
        data= urlEncodedParams,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
            'Referer': 'http://careers.force.com/jobs',
            'Pragma': 'no-cache',
            'Host':	'careers.force.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': len(urlEncodedParams),
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        },
        cookies= kuka
    )
    return resp.text

########### Program entry point
agent_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
link = 'http://careers.force.com/jobs'
uurl = 'http://careers.force.com/jobs/ts2__JobSearch'

# perform initial request and receive cookie and page
session = Session()
# first request
headers = {'user-agent': agent_str}
resp = session.get(link, headers=headers)
kuka = resp.cookies

firstSoup = BeautifulSoup(resp.text, 'html.parser', from_encoding="utf-8")
jobsAmountText = firstSoup.find('div', id='atsSearchResultsText').text
jobsAmount = int(re.search('\d*', jobsAmountText).group(0))

der_params = getUrlEncodedHashData(firstSoup)
nextText = nextPageFetchTextPost(uurl, der_params, kuka)
nextSoup = BeautifulSoup(nextText, 'html.parser', from_encoding="utf-8")
der_params = getUrlEncodedHashData(nextSoup)

thirdText = nextPageFetchTextPost(uurl, der_params, kuka)
thirdSoup = BeautifulSoup(thirdText, 'html.parser', from_encoding="utf-8")

tabela = thirdSoup.find('table', class_='atsSearchResultsTable', id='j_id0:j_id1:atsForm:atsSearchResultsTable')
jobRows = tabela.findAll('td', class_='atsSearchResultsData')
for jobRow in jobRows:
    texta = ''
    for stri in jobRow.stripped_strings:
        if stri[:2] != u'//':
            texta = texta + stri.encode('ascii', 'xmlcharrefreplace') + '; '
    print(texta)

pass

