#!/usr/bin/env python
import cv2
from glob import glob
import json
import MySQLdb
import numpy as np

import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web

import urllib

class Person:
    
    def __init__(self, image, name, age, gender, orientation):
        self.images = []
        self.images.append(image)
        self.name = name
        self.age = age
        self.gender = gender
        self.orientation = orientation

    def get_images(self)
        return self.images

    def add_image(self, image):
        self.images.append(image)

    def get_name(self)
        return self.name

    def set_name(self, name)
        self.name = name   

    def get_age(self)
        return self.age

    def set_age(self, age)
        self.age = age

    def get_gender(self)
        return self.gender

    def set_gender(self, gender)
        self.gender = gender

    def get_orientation(self)
        return self.orientation

    def set_orientation(self, orientation)
        self.orientation = orientation

class ImageHandler:
    """Handles the endpoints for the images. """
    @tornado.gen.coroutine
    def post(self, img_url):
        '''
        Accepts an image url and then sends it to be compared against 
        celebrity faces. Returns the name of the celebrity.
        '''
        resp = urllib.urlopen(img_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (227, 227))
        image = image[:,:,[2,1,0]]
        image = image.transpose(2,0,1)

        return image

    def list_matches(self, p):
        '''
        Queries the database for all the celebrity relationships.
        Returns all the celebrities the original celebrity has dated, as well
        as the original celebrity.
        '''
        #TODO: Add setup information
        db = MYSQLdb.connect("INFORMATION")

        cursor = db.cursor()

        sql = "SELECT name1 FROM tableWHERE name2 = '%s' UNION \
               SELECT name2 FROM table WHERE name1 = '%s'" \
               % (p.get_name, p.get_name)
        cursor.execute(sql)
        results = cursor.fetchall()
       
        names = []
        names.append(p.get_name)
        for row in results:
           names.append(row[0])
        
        db.close()

        return names

    def to_json(self, *persons):
        '''
        Sends back the data as JSON
        '''
        data = []
        for person in persons:
            data.append({ 'name':person.name, 'age':person.age, 
                          'gender':person.gender,
                          'orientation':person.orientation}) 

        return json.dumps(data)
