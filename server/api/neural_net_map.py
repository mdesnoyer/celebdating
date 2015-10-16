'''
Defines the mapFace class. Inputs:
    mapFace(model_file, pretrained_file, n_imgs)
    
    - instantiation input:
        model_file = the prototext file
        pretrained_file = the pretrained file (.caffemodel)
        n_imgs = the number of images to batch at once.
    
    - calling:
        mF = mapFace(...) # instantiate
        out = mF(image_array_list)

    - calling input:
        where image_array_list is an N-element list of numpy
        arrays representing input images. They must be BGR style,
        although they are resized by the preprocessing script. 

    - output:
        An N-element list of 128-element vectors (as numpy arrays)

NOTE:
All of this is contingent on using BGR images in the openCV style!
'''

import os
from time import time
import traceback
import sys
import cv2
import numpy as np
from threading import Lock

# this will prevent caffe from printing thousands
# of lines to stderr
if 'GLOG_minloglevel' not in os.environ:
    # Hide INFO and WARNING, show ERROR and FATAL
    os.environ['GLOG_minloglevel'] = '2'
    _unset_glog_level = True
else:
    _unset_glog_level = False
import caffe
if _unset_glog_level:
    del os.environ['GLOG_minloglevel']


'''
=======================================================================
'''

caffe.set_mode_gpu()

def _modify_proto(model_file, n_imgs):
    '''
    Modifies the prototext file so that
    it batches the appropriate number of images.
    '''
    f = open(model_file, 'r').read()
    nf = ''
    changed = False
    for ln in f.split('\n'):
        if not changed:
            if 'input_dim' in ln:
                ln = 'input_dim: %i'%(n_imgs)
                changed = True
        nf += ln + '\n'
    nfn = '/tmp/tmp_proto.prototxt'
    with open(nfn,'w') as x:
        x.write(nf.strip())
    return nfn
    
class MapFace(caffe.Net):
    '''
    Maps a batch of face images to their position in 
    feature space.
    '''
    def __init__(self, model_file, pretrained_file, n_imgs=1):
        '''
        model_file : the caffe model to use
        pretrained_file : array of model weights
        '''
        fn = _modify_proto(model_file, n_imgs)
        caffe.Net.__init__(self, fn, pretrained_file, caffe.TEST)
        in_ = self.inputs[0]
        self.image_dims = np.array(self.blobs[in_].data.shape[1:])
        print 'GPU Instantiated'
        self.image_dims = [227, 227]
        self.image_mean = np.array([104,117,123])
        self.lock = Lock()

    def __call__(self, data_list):
        '''
        Actually executes the prediction, provided with an
        N x 3 x H x W array of N images that have already
        been preprocessed and resized.
        '''
        if not len(data_list):
            return []
        for n in range(len(data_list)):
            data_list[n] = self._preprocess(data_list[n])
        data_array = np.array(data_list)
        # check if it's just one image.
        if len(data_array.shape) == 3:
            # if so, elaborate it into a 1 x 3 x H x W images
            data_array = data_array[None, :, :, :]
        if type(data_array).__module__ != np.__name__:
            raise TypeError("data_array type is %s, must be %s" % (
                str(type(data_array)), str(np.__name__)))
        if data_array.dtype != np.dtype('float32'):
            raise ValueError("data_array must be float32")
        with self.lock:
            out = self.forward_all(**{self.inputs[0]: data_array})
        #predictions = np.exp(out[self.outputs[0]])
        return list(out[self.outputs[0]])

    def _preprocess(self, bgr_img):
        '''
        Preprocesses the images.
        '''
        if not type(bgr_img).__module__ == np.__name__:
            raise TypeError("Image must be a numpy array (or str filename)")
        bgr_img = cv2.resize(bgr_img, (self.image_dims[0], self.image_dims[1]))
        if bgr_img.shape[2] == 1:
            # it's a black and white image, we have to colorize it
            bgr_img = cv2.cvtColor(bgr_img, cv2.COLOR_GRAY2BGR)
        elif bgr_img.shape[2] != 3:
            raise ValueError("Image has the incorrect number of channels")
        # subtract the channelwise image means
        if bgr_img.dtype != np.float32:
            bgr_img = bgr_img.astype(np.float32)
        bgr_img -= self.image_mean
        bgr_img = bgr_img.transpose(2, 0, 1)
        return bgr_img



# # ----------  TESTING ---------- # 
# pfx = '/media/nick/d216eb37-b0e1-478c-b170-2270d7699ea2/dbx/mridul_projects/'
# model_pre_tups = [('agenet_clusterloss/age_deploy.prototxt',
#                    ('agenet_clusterloss/snapshots/agenet_iter_48000.caffemodel',
#                     'agenet_clusterloss/snapshots/agenet_iter_54000.caffemodel')),
#                   ('googlenet_clusterloss/deploy.prototxt',
#                    ('agenet_clusterloss/snapshots/googlenet_iter_99000.caffemodel',
#                     'agenet_clusterloss/snapshots/googlenet_iter_177000.caffemodel'))]
# model_file = model_pre_tups[0][0]
# model_file = os.path.join(pfx, model_file)
# pretrained_file = model_pre_tups[0][1][0]
# pretrained_file = os.path.join(pfx, pretrained_file)
# mF = mapFace(model_file, pretrained_file)

# from glob import glob
# imgs = glob('/data/mridul_data/images/*')
# data_list = []
# for i in imgs[:100]:
#     data_list.append(cv2.imread(i))
# out = mF(data_list)
# # ---------- /TESTING ---------- #
