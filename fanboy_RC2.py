# Fanboy
# Checkpoint V1.0.0
#
#   This file is part of fanboy.
#   fanboy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#

import urllib.request
import bs4
import re
import time
import argparse
import os
import threading

# Functions

# Albums
def getsite(url):
    return url[:url.rfind('/')+1]

def whsite(url):
    return re.findall('https?://w{0,3}\.{0,1}(.+?\.[a-z]+?)/',url.lower().strip())[0]

def mksoup(url):
    html = urllib.request.urlopen(url).read()
    return bs4.BeautifulSoup(html,'lxml')

# Categories

def no_page(soup):
    try:return int(soup.find(style="white-space: nowrap").text.split()[-2])
    except:return int(soup.find(style="white-space: nowrap").text.split()[-3])

def page(url):
    global cats,albs
    soup = mksoup(url)
    pages = no_page(soup)
    for each in soup.find_all('span','catlink'):
        cats.append(site + each.a.get('href'))
    for each in soup.find_all('span','alblink'):
        albs.append(site + each.a.get('href'))
    #print("!!",len(albs),url)
    if pages > 1:
        for i in range(2,pages + 1):
            nsoup = mksoup(url+"&page="+str(i))
            for each in nsoup.find_all('span','catlink'):
                cats.append(site + each.a.get('href'))
            for each in nsoup.find_all('span','alblink'):
                albs.append(site + each.a.get('href'))
            #print("**",len(albs),url+"&page="+str(i))

# Main Flow Switches

def many_fansite():
    self.url = qq.get()

    return albums,images

def category(url):

def album(url):

def scrap(url):
    global site,start_time
    site = whsite(url)
    if site not in sites.keys():
        print("Fansite not supported.")
    else:
        if url.find("thumbnails.php?album") == -1:
            page(url)
            fans = many_fansite()
        else:
            fname, site_name, site_url = sites[site]
            fan = fansite(url)
            elapsed_time = time.strftime("%M:%S",time.gmtime(time.time()-start_time))
            print("Album : {}  ; {} links recovered in {} ".format(fan.title,len(fan.store),elapsed_time))


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
            self.store.append(self.site_url + thumb + each.get('alt') )

    def getinfo(self):
        try: self.title   = self.soup.find("span","statlink").text.strip()
        except:  self.title = self.soup.find("td","statlink").text.strip()
        try:self.info    = self.soup.find(style="white-space: nowrap").text
        except:self.info = "0 Images"
        self.no_page = int(self.info.split()[-2])


    def get_url(self):
        self.album = re.findall('(.+album=[0-9]+)',self.url)[0]
        self.fname, self.site_name, self.site_url = sites[whsite(self.url)]

    def write(self):
        fhand = open(self.fname,'a')
        fhand.write("### {} \n#!!! {} \n### {} \n".format(self.title,self.url,self.info))
        for each in self.store:
            if each not in cref:fhand.write(each+"\n")
        fhand.close()

# Supported Sites and Info
#SITES HERE

# Variables

cats = []
albs = []
DEBUG = False
# Argument Parser

parser = argparse.ArgumentParser(description='FANBOY')
parser.add_argument('--file', dest='file', type = str, default = None, required = False,
                    help='The file containing list of album links')
parser.add_argument('--cross', dest='cross_ref', type = str, default = None, required = False,
                    help='The file to cross reference with')
args = parser.parse_args()

# Main Path

if args.cross_ref is not None:
    for each in open(args.cross_ref,'r'):


if args.file is None:
    iurl = input("Enter the Album Url : ")
    start_time = time.time()
    if iurl.startswith('#'):break
    elif iurl.startswith("http"):scrap(iurl)
    else:print("Is this a URL.\n  Enter # to exit.")
else:file()
