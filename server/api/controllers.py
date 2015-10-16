#!/usr/bin/env python

import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

import cv2
from model.person import Person
import tornado.ioloop
import tornado.gen
import tornado.web
import tornado.options
from tornado.options import define, options

define("port", default=80, help="Service port")

class ImageProcessorHandler(tornado.web.RequestHandler):
    """Handles the endpoints for the images. """
    def initialize(self):
        pass
    
    @tornado.gen.coroutine
    def post(self):
        '''
        Accepts an form-encoded post with two parameters:
        gender - A string defining the gender
        file - base64 encoded version of the image
        '''
        im = self.get_image_from_request()
        faces = self.find_faces(im)
        if len(faces) == 0:
            raise tornado.web.HTTPError(400, "Could not find a face")
        sig = yield self.get_face_signature(faces[0])
        closest_celeb_id, dater_celeb_id = yield match_face(sig)

        yield self.finish_response(closest_celeb_id, dater_celeb_id)

    def get_image_from_request(self):
        '''Extracts the image from the http post request.

        returns a NxMx3 numpy array
        '''
        pass

    def find_faces(self, image):
        '''Extracts a face out of an image

        returns a list of [NxMx3] images of the faces in the image
        '''
        pass

    @tornado.gen.coroutine
    def get_face_signature(self, face):
        '''Converts a face into a signature for clustering.

        Inputs:
        NxMx3 - numpy array

        Returns:
        Yx1 numpy vector of the signature
        '''
        pass

    @tornado.gen.coroutine
    def match_face(self, sig)
        '''Matches a face to the closest celeb and the most likely person to date.

        Inputs:
        Yx1 numpy vector that is the face signature

        Outputs:
        (closest_celeb_id, dater_celeb_id)
        '''
        pass

    @tornado.gen.coroutine
    def finish_response(self, closest_celeb_id, dater_celeb_id):
        '''Finishes the response to send back to the user.'''
        pass
    ############ Functions below here are old and might not be needed ######

    @tornado.gen.coroutine
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

    @tornado.gen.coroutine
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

def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r'/process', ImageProcessorHandler)
        ], gzip=True)
    
    signal.signal(signal.SIGTERM, lambda sig, y: sys.exit(-sig))
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
