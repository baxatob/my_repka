import requests
from bs4 import BeautifulSoup

link = "https://bmcsoftware.taleo.net/careersection/feed/joblist.rss?lang=en&portal=101430233&searchtype=3&f=null&s=3|D&multiline=false"

f = requests.get(link).text

site = BeautifulSoup(f,"xml")

print(site.prettify())
