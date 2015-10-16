#!/usr/bin/env python
#import cv2
import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

import json
#import MySQLdb
import tornado.ioloop
import tornado.gen
import tornado.web
import tornado.options
import tornado_mysql
from tornado.options import define, options
#import numpy as np
#import torndb

#define("db_host", default="dateaceleb.cnvazyzlgq2v.us-east-1.rds.amazonaws.com", help="DB host")
define("db_host", default="localhost", help="DB host")
define("db_port", default="3306", help="DB host")
define("db_name", default="celebs", help="DB name")
define("db_user", default="admin", help="DB username")
define("db_password", default="admin123", help="DB Password")

class DBConnection(object):
    @staticmethod 
    @tornado.gen.coroutine 
    def get_connection(): 
        conn = yield tornado_mysql.connect(host=options.db_host, 
                                           port=options.db_port, 
                                           user=options.db_user, 
                                           passwd=options.db_password, 
                                           db=options.db_name) 
        raise tornado.gen.Return(conn) 
                                                       
class Celebrity:
    def __init__(self, 
                 name, 
                 image=None, 
                 age=None, 
                 gender=None, 
                 orientation=None):
        self.images = []
        self.name = name
        self.age = age
        self.gender = gender
        self.orientation = orientation
    
    def get(self, celeb_id): 
        conn = yield DBConnection.get_connection() 
        cursor = conn.cursor()
        yield cur.execute("SELECT * FROM celebrities WHERE celebrity_id = %d" % int(celeb_id))
        #return self.images

class ImageHandler:
    @tornado.gen.coroutine
    def __init__(self, host, port, db_name, username, password):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password

    @tornado.gen.coroutine
    def post(self):
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

