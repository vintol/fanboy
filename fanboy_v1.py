#
# Fansite Image Retriver
# 03/06/2017
#
#


import urllib.request
import bs4
import re
import time

# Functions

def whsite(url):
    return re.findall('https?://w{0,3}\.{0,1}(.+?\.[a-z]+?)/',url.lower().strip())[0]

def mksoup(url):
    html = urllib.request.urlopen(url).read()
    return bs4.BeautifulSoup(html,'lxml')

def file():
    global fname, site_name, site_url
    start = time.time()
    fread = open(input("Enter file name to read links from : "),'r').read().split()
    print(" {} links found. Getting Image Links ... ".format(len(fread)))
    for one in fread:
        site = whsite(one)
        if site not in sites.keys():
            print("Fansite not supported.")
            continue
        fname, site_name, site_url = sites[site]
        fan = fansite(one)
    finish = time.time()
    print("Time Taken :",time.strftime("%H:%M:%S",time.gmtime(finish-start)))

# Class Fansite

class fansite():
    def __init__(self, url):
        self.url = url
        self.store = []
        self.get_url()
        self.soup  = mksoup(self.album)
        self.getinfo()
        self.page(self.soup)
        if self.no_page > 1:
            for i in range(2,self.no_page+1):
                self.page(mksoup(self.album+"&page="+str(i)))
        self.write()

    def page(self,soup):
        for each in soup.find_all('img','image'):
            thumb = re.findall('(.+/)thumb.+',each.get('src'))[0]
            self.store.append(site_url + thumb + each.get('alt') )

    def getinfo(self):
        try: self.title   = self.soup.find("span","statlink").text.strip()
        except:  self.title = self.soup.find("td","statlink").text.strip()
        try:self.info    = self.soup.find(style="white-space: nowrap").text
        except:self.info = "0 Images"
        self.no_page = int(self.info.split()[-2])


    def get_url(self):
        self.album = re.findall('(.+album=[0-9]+)',self.url)[0]

    def write(self):
        fhand = open(fname,'a')
        fhand.write("### {} \n#!!! {} \n### {} \n".format(self.title,self.url,self.info))
        for each in self.store:
            fhand.write(each+"\n")
        fhand.close()

# Supported Sites and Info
from sites import *
# Main Path

while True:
    url = input("Enter the Album Url : ")
    if url.startswith('#'):break
    if url.startswith("!!!"):
        file()
        quit()
    start = time.time()
    site = whsite(url)
    if site not in sites.keys():
        print("Fansite not supported.")
        continue
    fname, site_name, site_url = sites[site]
    fan = fansite(url)
    finish = time.time()
    ttaken = time.strftime("%M:%S",time.gmtime(finish-start))
    print("Album : {}  ; {} links recovered in {} ".format(title,str(len(links)),ttaken))
