#!/usr/bin/env python
import cv2
import json
import MySQLdb
import numpy as np
import torndb

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
    @tornado.gen.coroutine
    def __init__(self, host, port, db_name, username, password):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password

    @tornado.gen.coroutine
    def post(self)
        '''
        Accepts an image and then sends it to be compared against 
        celebrity faces.
        '''
        resp = urllib.urlopen(img_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")

        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (227, 227))
        image = image[:,:,[2,1,0]]
        image = image.transpose(2,0,1)

        return image

    def list_matches(self, celeb_id, dater_id):
        '''
        Queries the database for the relevant celebrity images
        '''
        db = torndb.connect(self.host, self.user, self.password, self.name)
        
        sql_celeb = "SELECT image_url FROM celebrities WHERE \
                     celebrity_id = '%s'" %(celeb_id)

        celeb_image_url = db.get(sql_celeb)

        sql_dater = "SELECT image_url FROM celebrities WHERE \
                     celebrity_id = '%s'" %(dater_id)

        dater_image_url = db.get(sql_dater)

        db.close()

        return (celeb_image_url, dater_image_url)

