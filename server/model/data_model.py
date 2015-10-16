#!/usr/bin/env python
import cv2
from glob import glob
import json
import MySQLdb
import numpy as np

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
