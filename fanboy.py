# Fanboy Clubbed
# v2.0.0 22/06/2017
#
#   fanboy  Copyright (C) 2016  Tejaskumar Maru
#
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
import threading, queue
import better_exceptions

## Functions
# Albums
def getsite(url):
    return url[:url.rfind('/')+1]

def whsite(url):
    return re.findall('https?://w{0,3}\.{0,1}(.+?\.[a-z]+?)/',url.lower().strip())[0]

def mksoup(url):
    print(url)
    html = urllib.request.urlopen(url).read()
    return bs4.BeautifulSoup(html,'lxml')

# Categories
def no_page(soup):
    try:return int(soup.find(style="white-space: nowrap").text.split()[-2])
    except:
        if soup.find(style="white-space: nowrap") is None:return 1
        else:return int(soup.find(style="white-space: nowrap").text.split()[-3])

def gather_links(soup):
    for each in soup.find_all('span','catlink'):
        cat=sites[site][1] + each.a.get('href')
        if cat not in cats:cats.append(cat)
    for each in soup.find_all('span','alblink'):
        alb = sites[site][1] + each.a.get('href')
        if alb not in albs:albs.append(alb)

def page(url):
    global cats,albs,site
    soup = mksoup(url)
    site = whsite(url)
    try:pages = no_page(soup)
    except:pages = 1
    gather_links(soup)
    #print("!!",len(albs),url)
    if pages > 1:
        for i in range(2,pages + 1):
            gather_links(mksoup(url+"&page="+str(i)))
            #print("**",len(albs),url+"&page="+str(i))

# Main Flow Switches
def thread_fansite():
    global images
    while not qq.empty():
        tmp = fansite(qq.get())
        images = images + len(tmp.store)

def many_fansite():
    global qq,cats,albs
    while len(cats) > 0:
        for each in cats:
            page(each)
            cats.remove(each)
    albums = len(sorted(set(albs)))
    qq = queue.Queue()
    for each in sorted(albs):qq.put(each.strip())
    for i in range(args.threads):
        t = threading.Thread(target=thread_fansite)
        threads.append(t)
        t.start()
    for t in threads:t.join()
    return albums

def scrap(url):
    global site,start_time,cats,albs
    cats.clear()
    albs.clear()
    site = whsite(url)
    if site not in sites.keys():
        print("Fansite not supported.")
    else:
        if url.find("thumbnails.php?album") == -1:
            page(url)
            fans = many_fansite()
            elapsed_time = time.strftime("%M:%S",time.gmtime(time.time()-start_time))
            print("Found {} Albums and {} Images in {}".format(fans,images,elapsed_time))
        else:
            fan = fansite(url)
            elapsed_time = time.strftime("%M:%S",time.gmtime(time.time()-start_time))
            print("Album : {}  ; {} links recovered in {} ".format(fan.title,len(fan.store),elapsed_time))


def file():
    global fname
    start_time = time.time()
    for each in open(args.file,'r'):
        if each.startswith('#'):continue
        elif not each.startswith("http"):print("Invalid URL :",each)
        elif whsite(each) not in sites.keys():print("Unsupported Site :",each)
        else:
            if each.find("thumbnails.php?album=") != -1:albs.append(each.strip())
            else:cats.append(each.strip())
    print(" {} Categories and {} Albums found. Getting Image Links ... ".format(len(cats),len(albs)))
    fans = many_fansite()
    elapsed_time = time.strftime("%M:%S",time.gmtime(time.time()-start_time))
    print("Found {} Albums and {} Images in {}".format(fans,images,elapsed_time))

## Class Fansite
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
        self.fname, self.site_url = sites[whsite(self.url)]

    def write(self):
        cref = []
        if args.cross_ref is not None:fhand = open(args.cross_ref,'r')
#        else:fhand = open(self.fname,'r')
#        for each in fhand:
#            if each.startswith('#'):continue
#            cref.append(each.strip())
        fhand = open(self.fname,'a')
        fhand.write("### {} \n#!!! {} \n### {} \n".format(self.title,self.url,self.info))
        for each in self.store:
            if each not in cref:fhand.write(each+"\n")
        fhand.close()

## Supported Sites and Info
sites = {
'goddessadriana.com':["AdrianaL", "http://goddessadriana.com/gallery/"],
'alexandra-daddario.org':["AlexandraD", "http://alexandra-daddario.org/photos/"],
'alexandradaddario.us':["AlexandraD", "http://alexandradaddario.us/photos/"],
'daddariofan.net':["AlexandraD", "http://daddariofan.net/gallery/"],
'anne-hathaway.net':["AnneH", "http://anne-hathaway.net/photos/"],
'anne-hathaway.org':["AnneH", "http://anne-hathaway.org/gallery/"],
'aheardfan.com':["AmberH", "http://www.aheardfan.com/photos/"],
'amberheardweb.org':["AmberH", "http://amberheardweb.org/gallery"],
'ashley-greene.nl':["AshleyG", "http://ashley-greene.nl/gallery"],
'ashleygreene.org':["AshleyG", "http://ashleygreene.org/images/"],
'ashleygreenefans.org':["AshleyG", "http://ashleygreenefans.org/gallery/"],
'barrefaelionline.com':["BarR", "http://gallery.barrefaelionline.com/"],
'b-palvin.net':["BarbaraP", "http://b-palvin.net/gallery/"],
'barbara-palvin.sosugary.org':["BarbaraP2", "http://barbara-palvin.sosugary.org/"],
'behati-prinsloo.us':["BehatiP", "http://behati-prinsloo.us/gallery/"],
'bellahadid.org':["BellaH", "http://bellahadid.org/gallery/"],
'bellahadid.sosugary.org':["BellaH", "http://bellahadid.sosugary.org/"],
'bella-images.org':["BellaT", "http://bella-images.org/"],
'bella-thorne.com':["BellaT", "http://bella-thorne.com/gallery/"],
'bellathornefrance.net':["BellaT", "http://bellathornefrance.net/Photos/"],
'bella-thorne.org':["BellaT", "http://bella-thorne.org/gallery/"],
'bellathorne.net':["BellaT", "http://www.bellathorne.net/photos/"],
'divinecandice.com':["CandiceS", "http://divinecandice.com/photos/"],
'charlizecentral.com':["CharlizeT", "http://charlizecentral.com/gallery/"],
'deborahannwoll.org':["DeborahAW", "http://deborahannwoll.org/photos/"],
'doutzenkfanpage.com':["DoutzenK", "http://www.doutzenkfanpage.com/gallery/"],
'iheartwatson.net':["EmmaW", "http://iheartwatson.net/gallery/"],
'emmaw.net':["EmmaW", "http://emmaw.net/gallery/"],
'emma-watson-fan.org':["EmmaW", "http://emma-watson-fan.org/gallery/"],
'emmawatson.us':["EmmaW", "http://emmawatson.us/gallery/"],
'emilia-clarke.com':["EmiliaC", "http://emilia-clarke.com/gallery/"],
'emilia-clarke.net':["EmiliaC", "http://emilia-clarke.net/gallery/"],
'emiliaclarkefan.net':["EmiliaC", "http://emiliaclarkefan.net/gallery/"],
'emily-blunt.net':["EmilyB", "http://www.emily-blunt.net/gallery/"],
'emilyblunt.net':["EmilyB", "http://emilyblunt.net/gallery/"],
'emilydidonatosource.com':["EmilyD","https://emilydidonatosource.com/gallery/"],
'eblunt.org':["EmilyB", "http://eblunt.org/photos/"],
'elizabeth-gillies.net':["ElizabethG", "http://www.elizabeth-gillies.net/gallery/"],
'evagreenweb.com':["EvaG", "http://evagreenweb.com/gallery/"],
'evangeline-l.us':["Evangeline", "http://evangeline-l.us/gallery/"],
'evangelinelilly.org':["Evangeline", "http://evangelinelilly.org/gallery/"],
'gal-gadot.com':["GalG", "http://gal-gadot.com/gallery/"],
'gal-gadot.net':["GalG", "http://gal-gadot.net/photos/"],
'gadot-gal.com':["GalG", "http://gadot-gal.com/photos/"],
'g-gadot.com':["GalG", "http://g-gadot.com/gallery/"],
'hoskelsa.com':["ElsaH", "http://hoskelsa.com/photos/"],
'gemma-arterton.net':["GemmaA", "http://gemma-arterton.net/media/"],
'g-arterton.net':["GemmaA", "http://g-arterton.net/galeria/"],
'gigi-hadid.org':["GigiH", "http://gigi-hadid.org/gallery/"],
'gigi-hadid.net':["GigiH", "http://gigi-hadid.net/photos/"],
'irinashaykphotos.com':["IrinaS", "http://irinashaykphotos.com/"],
'teamisabelifontana.com':["IsabeliF", "http://teamisabelifontana.com/gallery/"],
'jessica-biel.com':["JessicaB", "http://jessica-biel.com/gallery/"],
'jessica-chastain.com':["JessicaC", "http://jessica-chastain.com/gallery/"],
'jenniferlawrencedaily.com':["JenniferL", "http://jenniferlawrencedaily.com/gallery/"],
'juliannemooreweb.net':["JulianneM", "http://juliannemooreweb.net/gallery/"],
'julianne-moore.org':["JulianneM", "http://julianne-moore.org/photos/"],
'k-winnick.com':["KatherynW", "http://k-winnick.com/photos/"],
'kaya-scodelario.com':["KayaS", "http://kaya-scodelario.com/gallery/"],
'katheryn-winnick.org':["KatherynW", "http://katheryn-winnick.org/photos/"],
'kristenphotos.org':["KristenS", "http://www.kristenphotos.org/"],
'kristensdaily.net':["KristenS", "http://kristensdaily.net/gallery/"],
'kristenstewartdaily.com':["KristenS", "http://kristenstewartdaily.com/gallery/"],
'lili-simmons.net':["LiliS", "http://lili-simmons.net/photos/"],
'livtylerfan.org':["LivT", "http://www.livtylerfan.org/vault/"],
'margotsource.net':["MargotR", "http://margotsource.net/gallery/"],
'margoteliserobbie.com':["MargotR", "http://margoteliserobbie.com/gallery/"],
'margot-robbie.us':["MargotR", "http://margot-robbie.us/photos/"],
'margot-robbie.org':["MargotR", "http://margot-robbie.org/gallery/"],
'margotrobbieonline.com':["MargotR", "http://margotrobbieonline.com/gallery/"],
'm-robbie.org':["MargotR", "http://m-robbie.org/gallery/"],
'simplystreepmedia.com':["MerylS", "http://www.simplystreepmedia.com/gallery/"],
'megan-fox.com':["MeganF", "http://www.megan-fox.com/gallery/"],
'megan-fox.us':["MeganF", "http://megan-fox.us/pix/"],
'morena-baccarin.net':["MorenaB", "http://gallery.morena-baccarin.net/"],
'natalie-dormer.org':["NatalieD", "http://natalie-dormer.org/gallery/"],
'nataliedormer.org':["NatalieD", "http://nataliedormer.org/gallery/"],
'natalie-dormer.com':["NatalieD", "http://natalie-dormer.com/gallery/"],
'noomi-rapace.com':["NoomiR", "http://www.noomi-rapace.com/gallery/"],
'peyton-list.net':["PeytonL", "http://peyton-list.net/photos/"],
'rachelweiszonline.net':["RachelW", "http://gallery.rachelweiszonline.net/"],
'pictures.rosie-huntington-whiteley.com':["RosieHW", "http://pictures.rosie-huntington-whiteley.com/"],
'sampaiopictures.com':["SaraS", "http://sampaiopictures.com/"],
'scarlett-photos.org':["ScarlettJ", "http://scarlett-photos.org/"],
'scarlett-johansson.net':["ScarlettJ", "http://scarlett-johansson.net/gallery/"],
'selenapictures.org':["SelenaG", "http://selenapictures.org/"],
'shailene-woodley.org':["ShaileneW", "http://shailene-woodley.org/gallery/"],
'sophieturner.org':["SophieT", "http://sophieturner.org/gallery/"],
'sophie-turner.us':["SophieT", "http://sophie-turner.us/gallery/"],
'taylorpictures.net':["TaylorS", "http://www.taylorpictures.net/"],
'tonicollette.org':["ToniC", "http://www.tonicollette.org/gallery/"],
'w-holland.org':["WillaH", "http://w-holland.org/photos/"],
'hq-pictures.com':["HQPICS", "http://hq-pictures.com/"],
'hqcelebrity.org':["HQCELEB", "http://hqcelebrity.org/"],
'hqdiesel.net':["HQDisel","http://www.hqdiesel.net/gallery/"],
'chris-evans.org':["ChrisE", "http://chris-evans.org/photos/"],
'chrisevansweb.net':["ChrisE", "http://chrisevansweb.net/gallery/"],
'chris-hemsworth.net':["ChrisH", "http://chris-hemsworth.net/gallery/"],
'chrishemsworth.us':["ChrisH", "http://www.chrishemsworth.us/gallery/"],
'hugh-fan.com':["HughJ", "http://hugh-fan.com/photos/"],
'liam-hemsworth.org':["LiamH", "http://liam-hemsworth.org/gallery/"],
'liamhemsworth.org':["LiamH", "http://liamhemsworth.org/gallery/"]}

## Variables

cats    = []
albs    = []
threads = []
images  = 0
DEBUG   = False

## Argument Parser

parser = argparse.ArgumentParser(description='FANBOY')
parser.add_argument('--file', dest='file', type = str, default = None, required = False,
                    help='The file containing list of album links')
parser.add_argument('--cross', dest='cross_ref', type = str, default = None, required = False,
                    help='The file to cross reference with')
parser.add_argument('--threads', dest='threads', type = int, default = 5, required = False,
                    help='No of threads to use')
args = parser.parse_args()

## Main Path

if args.file is None:
    while True:
        iurl = input("Enter the Album Url : ")
        start_time = time.time()
        if iurl.startswith('#'):break
        elif iurl.startswith("http"):scrap(iurl)
        else:print("Is this a URL?\n  Enter # to exit.")
else:file()
# END
