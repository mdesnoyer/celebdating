#!/usr/bin/env python

import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

import cv2
from api.face_extractor import FaceCropper
import api.neural_net_map
from model.person import Person
import tornado.ioloop
import tornado.gen
import tornado.web
import tornado.options
from tornado.options import define, options

define("port", default=80, help="Service port")
define("haar_model", default="", help="File containing the Harr model")
define("caffe_net_model", default="", help="Caffe model")
define("face_model", default="", help="Model weights for the face sigs")

class ImageProcessorHandler(tornado.web.RequestHandler):
    """Handles the endpoints for the images. """
    def initialize(self, haar_model, caffe_net_model, face_model):
        self.face_cropper = FaceCropper(haar_model)
        self.face_mapper = api.neural_net_map.MapFace(caffe_net_model,
                                                      face_model)
    
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
        return self.face_cropper.extract_faces(image)

    @tornado.gen.coroutine
    def get_face_signature(self, face):
        '''Converts a face into a signature for clustering.

        Inputs:
        NxMx3 - numpy array

        Returns:
        Yx1 numpy vector of the signature
        '''
        # TODO(Nick): Check the dimensions of these arrays, 
        #             the ordering may be messed up.
        # TODO(Nick): Make this asynchronous
        return self.face_mapper([face])

    @tornado.gen.coroutine
    def match_face(self, sig, gender)
        '''Matches a face to the closest celeb and the most likely 
           person to date you.

        Inputs:
        Yx1 numpy vector that is the face signature
        Gender you prefer to date

        Outputs:
        (closest_celeb_id, dater_celeb_id)
        '''
        (celeb_id, dated_id) = graph_ranking.find_dating(sig, gender)
        (name, image) = yield finish_response(celeb_id, dated_id)
        return (name, image)

    @tornado.gen.coroutine
    def finish_response(self, closest_celeb_id, dater_celeb_id):
        '''Finishes the response to send back to the user.'''
        pass
    ############ Functions below here are old and might not be needed ######


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

   @tornado.gen.coroutine
   def list_matches(self, host, name, user, password, person):
        '''
        Queries the database for all the celebrity relationships.
        Returns all the celebrities the original celebrity has dated, as well
        as the original celebrity.
        '''
        db = torndb.connect(host, name, user, password)


        sql_id = "SELECT celebrity_id FROM celebrities WHERE name = '%s'" \
                 %(person.get_name)

        celeb_id = db.get(sql_id)

        sql_name = "SELECT dated_id FROM dated WHERE celebrity_id = '%s'" \
                 % (celeb_id)

        name = db.get(sql_name)

        db.close()

        return name

def main():
    tornado.options.parse_command_line()

    graph_ranking = GraphRanking(host, port, db_name, username, password)
    application = tornado.web.Application([
        (r'/process', ImageProcessorHandler, 
         dict(haar_model=options.haar_model,
              caffe_net_model=options.caffe_net_model,
              face_model=options.face_model))
        ], gzip=True)
    
    signal.signal(signal.SIGTERM, lambda sig, y: sys.exit(-sig))
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
