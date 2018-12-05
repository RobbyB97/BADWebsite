"""
Author: Robby Bergers
Info: Methods to convert rss feeds to JSON collections
"""

import requests
from urllib import request
import os
from time import sleep
import logging
import json
from bs4 import BeautifulSoup

#logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.FileHandler('getfeed.log')
handler.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('|%(asctime)s| [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
log.addHandler(consoleHandler)
log.addHandler(handler)
log.info('Running file getfeed.py:')

def clean():
    try:
        log.debug('Clean started:')
        # clear old data
        for file in os.listdir('../docs/mp3files'):
            log.info('Deleting %s...' % file)
            os.unlink('../docs/mp3files/' + file)
        for file in os.listdir('../docs/imgfiles'):
            log.info('Deleting %s...' % file)
            os.unlink('../docs/imgfiles/' + file)
    except Exception:
        log.exception('Error in clean:')

def starTalkGet(link):
    try:
        log.debug('starTalkGet started:')
        log.info('Getting xml from %s...' % link)
        #Set variables
        mp3dict = {}
        jsonfile = open('./JSON/mp3.json', 'w')
        xml = requests.get(link).text
        soup = BeautifulSoup(xml, "lxml")
        i=0
        for element in soup.findAll('enclosure'):
            if (element['url'][-3:] == 'mp3'):
                mp3dict[str(i)] = element['url']
                i += 1
            else:
                log.warning('%s is not an audio file, and will be skipped...' % element['url'][-3:])
        log.info('Found %s mp3 files in XML' % str(len(mp3dict)))
        json_str = json.dumps(mp3dict, sort_keys=True, indent=4)
        jsonfile.write(json_str)
        jsonfile.close()
        log.info('mp3 JSON list created...')
        try:
            jsonfile = open('./JSON/mp3.json', 'r').read()
            jsonobj = json.loads(jsonfile)
            for key in jsonobj:
                url = jsonobj[key]
                newfile = '../docs/mp3files/' + key + '.mp3'
                request.urlretrieve(url, newfile)
                log.info('mp3 file saved to %s' % newfile)
                sleep(0.5)
        except Exception:
            log.exception('Could not download mp3 files:')
        return
    except Exception:
        log.exception('Error in starTalkGet:')

def nasaGet(link):
    try:
        log.debug('nasaGet started:')
        log.info('Getting xml from %s...' % link)
        #Set variables
        imagedict = {}
        jsonfile = open('./JSON/image.json', 'w')
        xml = requests.get(link).text
        soup = BeautifulSoup(xml, "lxml")
        i = 0
        for image in soup.findAll('enclosure'):
            imagedict[str(i)] = image['url']
            i += 1
        log.info('Found %s image files in XML...' % str(len(imagedict)))
        json_str = json.dumps(imagedict, sort_keys=True, indent=4)
        jsonfile.write(json_str)
        jsonfile.close()
        log.info('image JSON list created...')
        try:
            jsonfile = open('./JSON/image.json', 'r').read()
            jsonobj = json.loads(jsonfile)
            for key in jsonobj:
                url = jsonobj[key]
                newfile = '../docs/imgfiles/' + key + '.jpg'
                request.urlretrieve(url, newfile)
                sleep(1)
                log.info('Saved image to %s...' % newfile)
        except Exception:
            log.exception('Could not download image files:')
    except Exception:
        log.exception('Error in nasaGet:')

def spaceGet(link):
    try:
        log.debug('spaceGet started:')
        log.info('Getting xml from %s' % link)
        #Set variables
        videodict = {}
        jsonfile = open('./JSON/video.json', 'w')
        xml = requests.get(link).text
        soup = BeautifulSoup(xml, "lxml")
        i = 0
        for video in soup.findAll('link'):
            if '/watch?v=' in video['href']:
                #Linkext is the part of the URL which is needed to embed the video
                linkext = video['href'].split('/watch?v=')[1]
                videodict[str(i)] = linkext
                i += 1
            else:
                log.warning('%s is not a video URL and will be skipped...' % video['href'])
        log.info('Found %s video files in XML...' % str(len(videodict)))
        json_str = json.dumps(videodict, sort_keys=True, indent=4)
        jsonfile.write(json_str)
        jsonfile.close()
        log.info('video JSON list created...')
    except Exception:
        log.exception('Error in spaceGet:')

def main():
    try:
        log.debug('main started:')
        clean()
        #list of links to XML files to download
        #the links are segregated based on the type of content to pull
        mp3s = 'https://rss.art19.com/startalk-radio'
        images = 'https://www.nasa.gov/rss/dyn/ames_news.rss'
        videos = 'https://www.youtube.com/feeds/videos.xml?user=ouramazingspace'
        #Get mp3 files
        starTalkGet(mp3s)
        #Get image files
        nasaGet(images)
        #Get video files
        spaceGet(videos)
    except Exception:
        log.exception('Error in main:')

if __name__ == '__main__':
    try:
        main()
    except Exception:
        log.exception('FATAL ERROR')