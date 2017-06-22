#
#
# TODO : Restart download
#   This file is part of fanboy.
#   fanboy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#

import urllib.request
import argparse
import time
import queue
import threading

#
def download():
    while True:
        mydata = threading.local()
        mydata.not_exist = False
        if qq.empty():break
        else:
            mydata.name, mydata.url = qq.get()
        try:
            mydata.html = urllib.request.urlopen(mydata.url,timeout=25)
        except urllib.error.HTTPError as HERR:
            if HERR.code == 404:
                broken += 1
                continue
        except:
            for tmp in range(2):
                try:
                    mydata.html = urllib.request.urlopen(mydata.url)
                    if mydata.html.getcode() == 200:break
                except:continue
            print("ERROR : GET ERROR :",mydata.name,mydata.url)
            failed.append((mydata.name,mydata.url))
            continue
        try:mydata.image = mydata.html.read()
        except:
            print("ERROR : READ ERROR :",mydata.name,mydata.url)
            failed.append((mydata.name,mydata.url))
            continue
        try:open(mydata.name,'wb').write(mydata.image)
        except:
            print("ERROR : WRITE ERROR :",mydata.name,mydata.url)
            continue
        print("INFO : Downloaded",mydata.name)

def mkqueue():
    global total,unique,links
    fhand = open(args.fname,'r')
    links = []
    for tmp in fhand:
        if tmp.startswith('#'):continue
        links.append(tmp.strip())
        total = len(links)
        links = sorted(set(links))
        unique = len(links)
        if unique >
            qq.put((args.prefix+str(1000+n),each.strip()))
    print(str(qq.qsize()),str(n),"Links Found.")
    fhand.close()

def enqueue():
    if qq.qsize() != 0:print("WARNING: Queue not empty. ")
    for name,url in failed:
        qq.put((name,url))

def init_threads():
    for i in range(args.threads):
        t = threading.Thread(target=download)
        threads.append(t)
        t.start()

#

parser = argparse.ArgumentParser(description='Start Tao Downloader.')
parser.add_argument('fname', type=str,
                    help='The File containing list of links.')
parser.add_argument('--prefix', dest='prefix', type = str, default = None, required = False,
                    help='The profile page no to start scraping images from')
parser.add_argument('--from', dest='last_page' , type = int, default = None, required = False,
                    help='Scrap images only upto the page no.')
parser.add_argument('--threads', dest='threads', type = int, default = 10, required = False,
                    help='No. of threads to use.')
args = parser.parse_args()

#
qq = queue.Queue()
threads = []
links   = []
failed  = []
broken  = 00

enqueue()

init_threads()
for t in threads:t.join()

if len(failed) > 0:
    print("INFO : Download failed for {} Items. Trying Again ...".format(len(failed)))
    mkqueue()
    failed.clear()
    for t in threads:t.run(download)
    print("INFO:",len(failed),"Downloads Failed.")

#
