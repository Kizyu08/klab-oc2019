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


#usage
unkoface=Face(1,[(1,2),(3,4)])
unkoface.set_result(1,1,1,1,1,1,1,1,1)
img=cv2.imread("IMG_0005.png",1)
aaa=Faces(img)
aaa.set_face(unkoface)
