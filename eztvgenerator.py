from bs4 import BeautifulSoup
import requests
import PyRSS2Gen
import datetime

requests.packages.urllib3.disable_warnings()
 
#--------SETTINGS-------
PATH = "/home/pi/.flexget/"
FILE = "eztv.xml"
XML_TITLE = "EZTV RSS Generator"
XML_LINK = ""
XML_DESCRIPTION = "Generate RSS Feed based on EZTV"
 
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
eztvLink = "https://eztv.ag/sort/100/"
request  = requests.get(eztvLink, verify=False)
data = request.text
soup = BeautifulSoup(data)

rows = soup.find_all("tr", class_="forum_header_border")

for row in rows:
    title = row.find(class_='epinfo').getText()
    temp_link = row.find(class_='download_1')

    # Only magnet link
    link = temp_link if temp_link != None else row.find(class_='magnet')

    # Neither
    if link == None:
        continue

    add_to_rss(title, link['href'], False)
    added_Items += 1

rss.write_xml(open("%s%s" % (PATH, FILE), "w" ))
print "Status: Complete (Found %i New Items)" % (added_Items)