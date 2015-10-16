import numpy as np
import os
import cv2
from glob import glob
import pdb, sys
from sklearn import svm
import tempfile
import pickle
from sklearn.externals import joblib
import shutil

def resize_mxS(img, mx, equal=False):
    '''
    Resizes such that the maximum size of img
    is no larger than mx. If equal == True, then
    resize the image such that the max side is
    equivalent to mx
    '''
    cmx = max(img.shape)
    if (cmx < mx):
        if not equal:
            return img
    scaleF = mx*1./cmx
    newD = np.array(img.shape[:-1])*scaleF
    newD = tuple(newD.astype(int))
    return cv2.resize(img, (newD[1], newD[0]))

class CropFaces:
    '''
    Iteratively crops from an image, given a 
    list of tuples of the form
    (name, filename, dest_filename).

    If the user indicates that the photo is good,
    then it moves the cropped file to dest_filename.
    '''
    def __init__(self, haarRoot=None, haarCascade=None):
        if haarRoot == None:
            haarRoot = '/Users/neon/Desktop'
        if haarCascade == None:
            haarCascade = 'haar_cascade.xml'
        self.haarFile = os.path.join(haarRoot, haarCascade)
        self.haarParams = {'minNeighbors': 5, 'minSize': (50, 50), 'scaleFactor': 1.1}
        self.face_cascade = cv2.CascadeClassifier()
        self.face_cascade.load(self.haarFile)

    def get_gray(self, image):
        # returns the grayscale version of an image
        if type(image) == 'str':
            image = cv2.imread(image)
        if len(image.shape) == 3 and image.shape[2] > 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def display_face(self, name, image, coords):
        imcp = image.copy()
        x, y, w, h = coords
        cv2.rectangle(imcp, (x,y),(x+w,y+h), (255,0,0), 2)
        imcp = resize_mxS(imcp, 512)
        print 'IS THIS %s?'%(name)
        cv2.imshow('Face Eval', imcp)
        r = cv2.waitKey(0)
        if r == ord('y'):
            return (True, image[y:(y+h), x:(x+w)])
        elif r == ord('n'):
            return (False, None)
        elif r == ord('q'):
            return (None, None)

    def evaluate(self, person, filen, dest_filen):
        image = cv2.imread(filen)
        if image == None:
            return True
        faces = self.face_cascade.detectMultiScale(
                            image, **self.haarParams)
        for f in faces:
            r = self.display_face(person, image, f)
            if r[0]:
                cv2.imwrite(dest_filen, r[1])
                return True
            if r[0] == None:
                return False
        cv2.imwrite(dest_filen.replace('crop_celebs','uncrop_celebs'), image)
        return True

    def iterate(self, photos):
        for person, filen, dest_filen in photos:
            if os.path.exists(dest_filen):
                continue
            destc = os.path.join(dest_filen.split('/')[-1])
            bdestc = os.path.join(dest_filen.split('/')[-1]).replace('crop_celebs','uncrop_celebs')
            if not os.path.exists(destc):
                os.mkdir(destc)
            if not os.path.exists(bdestc):
                os.mkdir(bdestc)
            r = self.evaluate(person, filen, dest_filen)
            if r == False:
                cv2.destroyAllWindows()
                return
        cv2.destroyAllWindows()

images = glob('/Users/neon/Desktop/celebrities/*/*')
dest_dir = '/Users/neon/Desktop/crop_celebs'
# produce the list
photos = []
for i in images:
    person = i.split('/')[-2]
    dest = os.path.join(dest_dir, person, i.split('/')[-1])
    photos.append((person, i, dest))
cf = CropFaces()
cf.iterate(lst)
