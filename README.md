      __            _
    /  _|          | |
    | |_ __ _ _ __ | |__   ___  _   _
    |  _/ _` | '_ \| '_ \ / _ \| | | |
    | || (_| | | | | |_) | (_) | |_| |
    |_| \__,_|_| |_|_.__/ \___/ \__, |
                                 __/ |
                                |___/


A scraper that can retrive links of hq images from fansites and download them, in bulk.

[![GitHub license](https://img.shields.io/badge/License-GPL-blue.svg)](https://raw.githubusercontent.com/vintol/fanboy/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/vintol/fanboy.svg)](https://github.com/vintol/fanboy/issues)
[![GitHub stars](https://img.shields.io/github/stars/vintol/fanboy.svg?style=plastic)](https://github.com/vintol/fanboy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vintol/fanboy.svg?style=plastic)](https://github.com/vintol/fanboy/network)
[![GitHub release](https://img.shields.io/badge/Release-v2.0.1-blue.svg)](https://github.com/vintol/fanboy/releases)
[![Join the chat](https://badges.gitter.im/vintol-fanboy/Lobby.svg)](https://gitter.im/vintol/fanboy/)

[TOC]

## INSTALL



Fanboy is written in python3.

You will need [python3](https://wiki.python.org/moin/BeginnersGuide/Download).      
You will also need `pip`, the package manager for python external modules.          
It comes bundled in python3 ( >v3.5 ), alternatively get it [HERE](https://pip.pypa.io/en/stable/installing/#).      
Then, install dependancies with following command :

    pip install -U bs4 lxml

## Usage

There are various ways you can go about ..
a most simple one is shown here but it would be very tidious and time consuming for large no. of albums,
for in depth explanation and full features see [HERE](https://github.com/vintol/fanboy/wiki/How-to-Use)


In the terminal(MAC/UNIX) or the command prompt(WIN),
go to the directory you have downloaded the fanboy in and run

    python3 fanboy.py

    python3.exe fanboy.py

It will prompt for URL of the album you want to download images from , paste and press Enter.
A file will be created in working directory with the image links.

I recommand using [retrive.py](https://github.com/vintol/fanboy/wiki/Retrive) to download these images,
Although any downloader will do, retrive.py names the download images for beteer handling and mangement. See the docs for more details.    


## Websites
Currently Fanboy supports 95 fansites. Some of them are ...

- [bella-hadid.fans.bz](http://bella-hadid.fans.bz/gallery/)
- [bella-thorne.com](http://bella-thorne.com/gallery/)
- [iheartwatson.net](http://iheartwatson.net/gallery/)
- [emmaw.net](http://emmaw.net/gallery/)
- [emilia-clarke.com](http://emilia-clarke.com/gallery/)
- [jessica-biel.com](http://jessica-biel.com/gallery/)
- [jessica-chastain.com](http://jessica-chastain.com/gallery/)
- [jenniferlawrencedaily.com](http://jenniferlawrencedaily.com/gallery/)
- [juliannemooreweb.net](http://juliannemooreweb.net/gallery/)
- [margotsource.net](http://margotsource.net/gallery/)
- [scarlett-photos.org](http://scarlett-photos.org/)
- [shailene-woodley.org](http://shailene-woodley.org/gallery/)
- [hq-pictures.com](http://hq-pictures.com/)
- [hqcelebrity.org](http://hqcelebrity.org/)
- [chris-evans.org](http://chris-evans.org/photos/)

See the Full list of supported sites [HERE](https://github.com/vintol/fanboy/wiki/Sites)

-----
