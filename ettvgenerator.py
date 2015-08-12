from bs4 import BeautifulSoup
import requests
import PyRSS2Gen
import datetime

requests.packages.urllib3.disable_warnings()
 
#--------SETTINGS-------
PATH = "/home/pi/.flexget/"
FILE = "ettv.xml"
XML_TITLE = "ETTV RSS Generator"
XML_LINK = ""
XML_DESCRIPTION = "Generate RSS Feed based on ETTV kickass user"
 
#-----------------------
 
rss = PyRSS2Gen.RSS2(
    title = XML_TITLE,
    link = XML_LINK,
    description = XML_DESCRIPTION,
    lastBuildDate = datetime.datetime.now())
 
def add_to_rss(title, link, debug):
    item = PyRSS2Gen.RSSItem(pubDate=datetime.datetime.now(),title=title,link=link)
    rss.items.append(item)
    if debug:
        print "---------------------------------------------------"
        print "Title: " + xtitle
        print "\tLink: " + xlink
 
 
added_Items = 0

ettvLink = "https://kat.cr/usearch/ettv/"
ettvSort = "/?field=time_add&sorder=desc"

for i in range (1,3):
    ettv = ettvLink + str(i) + ettvSort
    request  = requests.get(ettv, verify=False)
    data = request.text
    soup = BeautifulSoup(data)
    for row in soup.find_all(class_='odd'):
            title = row.find('a', class_='cellMainLink').getText() 
            link  = row.find('a', class_="imagnet icon16")
            add_to_rss(title, link['href'], False)
            added_Items += 1
    for row in soup.find_all(class_='even'):
            title = row.find('a', class_='cellMainLink').getText()
            link  = row.find('a', class_="imagnet icon16")
            add_to_rss(title, link['href'], False)
            added_Items += 1 

rss.write_xml(open("%s%s" % (PATH, FILE), "w" ))
#print "Status: Complete (Found %i New Items)" % (added_Items)