#!/usr/bin/env python

import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

from api.face_extractor import FaceCropper
import cgi 
import cv2
import json
#import api.neural_net_map
#import model
from model import data_model
import numpy as np

import signal 
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.web
import tornado.options
from tornado.options import define, options

define("port", default=8083, help="Service port")
define("haar_model", default="", help="File containing the Harr model")
define("caffe_net_model", default="", help="Caffe model")
define("face_model", default="", help="Model weights for the face sigs")

class ResponseCode(object):
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_NOT_FOUND = 404

class APISender(object):
    def success(self, data, code=ResponseCode.HTTP_OK):
        self.set_status(code)
        self.write(data)
        self.finish()

class APIHandler(tornado.web.RequestHandler, APISender):
    def initialize(self):
        self.set_header("Content-Type", "application/json")

class ImageProcessorHandler(APIHandler):
    """Handles the endpoints for the images. """
        #self.face_cropper = FaceCropper(options.haar_model)
        #self.face_mapper = api.neural_net_map.MapFace(options.caffe_net_model,
        #                                              options.face_model)

    #def __init__(self, graph_ranking):
    #    self.graph_ranking = graph_ranking

    @tornado.gen.coroutine
    def post(self):
        '''
        Accepts an form-encoded post with two parameters:
        gender - A string defining the gender
        file - base64 encoded version of the image
        '''

        im = self.get_image_from_request()
        ''' 
        TODO commenting for now, due to caffe issues 

        faces = self.find_faces(im)
        if len(faces) == 0:
            raise tornado.web.HTTPError(400, "Could not find a face")
        sig = yield self.get_face_signature(faces[0])
        closest_celeb_id, dater_celeb_id = yield match_face(sig)
        ''' 

        closest_celeb_id = 1 
        dater_celeb_id = 2
        matching_celeb = yield data_model.Celebrity.get(closest_celeb_id) 
        would_date_me = yield data_model.Celebrity.get(dater_celeb_id)

        if matching_celeb and would_date_me: 
            rv = {} 
            rv['closest_match'] = matching_celeb
            rv['future_ex_spouse'] = would_date_me 
            self.success(json.dumps(rv)) 
        else: 
            raise Exception('could not find a match') 
          
    def get_image_from_request(self):
        '''Extracts the image from the http post request.

        returns a NxMx3 numpy array
        '''
        image_body = self.request.files['upload'][0]['body']

        if not image_body: 
            raise Exception('no image no work') 

        image = np.asarray(bytearray(image_body), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (227, 227))
        image = image[:,:,[2,1,0]]
        image = image.transpose(2,0,1)
        return image

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
        raise tornado.gen.Return(self.face_mapper([face]))

    @tornado.gen.coroutine
    def match_face(self, sig, gender):
        '''Matches a face to the closest celeb and the most likely
           person to date you.

        Inputs:
        Yx1 numpy vector that is the face signature
        Gender you prefer to date

        Outputs:
        (closest_celeb_id, dater_celeb_id)
        '''
        raise tornado.gen.Return(self.graph_ranking.find_dating(sig, gender))

    @tornado.gen.coroutine
    def finish_response(self, closest_celeb_id, dater_celeb_id):
        '''Finishes the response to send back to the user.'''
        return self.image_response.list_matches(closest_celeb_id, 
                                                dater_celeb_id) 
def main():
    tornado.options.parse_command_line()
    graph_ranking = 123 
    image_response = 123 
    #graph_ranking = GraphRanking(options.host, options.port, options.db_name,
    #                             options.username, options.password,
    #                             options.celebrity_model)
    
    # what was this for?
    #image_response = ImageResponse(options.host, options.port, options.db_name,
    #                               options.username, options.password)

    application = tornado.web.Application([
        (r'/process', ImageProcessorHandler)
        ], gzip=True)
    
    print 'running' 
    signal.signal(signal.SIGTERM, lambda sig, y: sys.exit(-sig))
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
