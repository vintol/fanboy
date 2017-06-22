#
# Category Crawler
# 29/10/2016
#
#   This file is part of fanboy.
#   fanboy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
import urllib.request
import bs4

#
def mksoup(url):
    print(url)  #DEBUG
    html = urllib.request.urlopen(url).read()
    return bs4.BeautifulSoup(html,'lxml')

def page(url):
    soup = mksoup(url)
    if len(soup.find_all('span','catlink')) > 0:catlinks(soup,getsite(url))
    if len(soup.find_all('span','alblink')) > 0:alblinks(url,soup,getsite(url))

def no_page(soup):
    try:return int(soup.find(style="white-space: nowrap").text.split()[-2])
    except:return int(soup.find(style="white-space: nowrap").text.split()[-3])


def catlinks(soup,site):
    global cats
    for each in soup.find_all('span','catlink'):
        cats.append(site + each.a.get('href'))

def alblinks(url,soup,site):
    global albs
    pages = no_page(soup)
    for each in soup.find_all('span','alblink'):
        albs.append(site + each.a.get('href'))
    #print("!!",len(albs),url)
    if pages > 1:
        for i in range(2,pages + 1):
            nsoup = mksoup(url+"&page="+str(i))
            for each in nsoup.find_all('span','alblink'):
                albs.append(site + each.a.get('href'))
            #print("**",len(albs),url+"&page="+str(i))

def getsite(url):
    return url[:url.rfind('/')+1]

#
cats = []
albs = []
#

iurl = input("Enter the URL : ")
if iurl.startswith('#'):quit()
if iurl.startswith("!!!"):
    for each in open(input("Name of file to read links from. : "),'r'):
        if each.startswith('#'):continue
        if each.find("thumbnails.php?album") > 1:albs.append(each)
        else:page(each.strip())
else:page(iurl)
if len(cats) != 0:
    print("CATS:",len(cats))
    for each in cats:page(each)
print("ALBS:",len(albs))
#
fhand = open(input("Enter File Name to write links : "),'a')
for each in albs:fhand.write(each+"\n")
fhand.close()

#print(cats,albs)
