# -*- coding: utf-8 -*-
import pygame
import codecs
import Util
import Face
import Window
import sys
import numpy as np
import cv2
import Face
import random

# 検出された各顔の表情スコアを計算する関数
# 担当外なので、てきとうな値を返すように設定
def compFaceScores(faces):
    for face in faces:
        for emotionName in face.emotionScores.keys():
            #print(emotionName)
            face.emotionScores[emotionName] = random.random()
            face.x      = random.random() * 640
            face.y      = random.random() * 480
            face.width  = 32
