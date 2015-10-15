
#!/usr/bin/env python

'''
Scrape photos of celebs from Flickr
'''
import re
import os
import urllib2
import json
import logging
import sys
import xml.etree.ElementTree
import StringIO


# API CALL
#https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=6145ea0768767fed6c9b7aea0764c57f&tags=jared+leto&content_type=1&format=rest&api_sig=61eef0f28ccc831b573b993bb47c1b9d

#URL TO BUILD OUT FROM XML RESPONSE TO API CALL
#https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

#WHAT A JARED LETO IMAGE URL LOOKS LIKE WE CAN DOWNLOAD
#https://farm6.staticflickr.com/5799/21552202603_49029a1bc9.jpg


peeps = ['jared leto', 'brad pitt']

def make_flickr_api_request(q):

    xmlStream = urllib2.urlopen("https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=6145ea0768767fed6c9b7aea0764c57f&tags=%s&content_type=1&format=rest&api_sig=61eef0f28ccc831b573b993bb47c1b9d" % q)
    try:
        xmlDoc = xml.etree.ElementTree.parse(xmlStream)
        root = xmlDoc.getroot()

        for photo in root.iter('{http://search.yahoo.com/mrss/}photos'):
            photo_id = media_group.find('{http://search.yahoo.com/mrss/}id').text
            secret = media_group.find('{http://search.yahoo.com/mrss/}secret').text
            server = media_group.find('{http://search.yahoo.com/mrss/}server').text
            farm = media_group.find('{http://search.yahoo.com/mrss/}farm').text
            url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (farm, server, photo_id, secret)
            print url


    finally:
        xmlStream.close()


for person in peeps:
	make_flickr_api_request(person)

