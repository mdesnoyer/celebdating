#!/usr/bin/env python
#import cv2
import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

import json
import tornado.ioloop
import tornado.gen
import tornado.web
import tornado.options
import tornado_mysql
from tornado.options import define, options

#define("db_host", default="dateaceleb.cnvazyzlgq2v.us-east-1.rds.amazonaws.com", help="DB host")
define("db_host", default="localhost", help="DB host")
define("db_port", default=3306, help="DB host")
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

    @staticmethod  
    @tornado.gen.coroutine 
    def get(celeb_id): 
        rv = None 
        conn = yield DBConnection.get_connection() 
        cursor = conn.cursor()
        yield cursor.execute("SELECT * FROM celebrities WHERE celebrity_id = %d" % int(celeb_id))
        row = cursor.fetchone()
        if row:  
            descrips = [] 
            for d in cursor.description:  
               descrips.append(d[0]) 
            rv = dict(zip(descrips, row))  

        raise tornado.gen.Return(rv) 
