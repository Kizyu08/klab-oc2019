# -*- coding: utf-8 -*-
import cv2
import numpy
from face import Face



class Faces:
    """A Faces class"""

    # コンストラクタ
    def __init__(self, image):
        self.__image = image
        self.__faces = []

    def image(self):
        return self.__image

    def set_face(self, newface):
        self.__faces.append(newface)

    def face(self):
        return self.__faces
