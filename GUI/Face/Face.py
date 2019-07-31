import cv2
import numpy

class Face:
    """A Face class"""
    
    def __init__(self, face_id=0, rect=[(0,0), (0,0)]):
        self.__face_id = face_id
        self.__rect = rect
        self.__result= dict(neutral=0, happiness=0, surprise=0,sadness=0, anger=0, disgust=0, fear=0, contempt=0, unknown=0)

    def face_id(self):
        return self.__face_id

    def rect(self):
        return self.__rect

    def result(self):
        return self.__result

    set 

    def set_result(self, neutral=0, happiness=0, surprise=0, sadness=0, anger=0, disgust=0, fear=0, contempt=0, unknown=0):
        self.__result = dict(neutral, happiness, surprise,
                             sadness, anger, disgust, fear, contempt, unknown)
