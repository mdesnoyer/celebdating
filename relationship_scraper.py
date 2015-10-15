#!/usr/bin/env python

'''
Scrape relationships out of HTML
'''
import re
import os
import urllib2
import json
import logging
import sys
import StringIO


#logging.basicConfig(filename='yt_for_eurogamer.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
#_log = logging.getLogger(__name__)


#_log.info('\n\n-----Checking YT for new Eurogamer videos-----\n')


for root, dirs, files in os.walk("/users/davidlea/Desktop/dating.famousfix.com/"):
    for name in files:

        if name == "dating-history.html":
            with open(os.path.join(root, name), 'r')  as text:
                content = text.read()
                regex = re.compile(r'(.*more.*)')
                for (matches) in re.findall(regex, content):
                    print matches
