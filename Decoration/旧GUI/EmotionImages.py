# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import codecs
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import datetime
import random

sys.path.append('../face')
import face
import IScene
import Util
import Window
import SceneEventID
import FaceDetectionDummy

# 表情に対応するフレーム画像を管理するクラス
# 画像は GUI 周りを管理している Pygame の形式で管理する
class EmotionImages:
    # コンストラクタ
    def __init__(
        self, 
        wndWidth = 640,
        wndHeight = 480,
        pathOfEmotionImagesList = "./frame/emotionImageList.txt",
    ):
        self.__emotionImages = {}       # 表情と表情に対応する画像を格納する辞書型リスト {(表情名,画像), ...}
        
        # 表情名を一通り取得する
        self.__emotionNames = face.Face().result().keys() # 表情名が辞書型リストのキーになっている（と信じたい）

        # 表情名と表情に対応する画像ファイルのパスが対で記述されたファイルを開く
        emotionImageListFile = open(pathOfEmotionImagesList, "r")

        # ファイルが開けない場合は強制終了
        if not emotionImageListFile:
            print("\"" + pathOfEmotionImagesList + "\"の読み込みに失敗しました")
            exit()

        pathListEmotionImages = {}      # 各表情に対応するフレーム画像各々のファイルパスを格納する辞書型リスト {(表情名, ファイルパス)}

        while True:
            line = emotionImageListFile.readline()
            if not line:
                break
            line.strip("\n")
            pair = line.split()
            if len(pair) < 2:
                continue
            self.__emotionImages[pair[0]] = pygame.image.load("./frame/" + pair[1])
            imgRect = self.__emotionImages[pair[0]].get_rect()
            imgWidth = imgRect.width
            imgHeight = imgRect.height
            widthRate = float(wndWidth) / float(imgWidth)
            heightRate = float(wndHeight) / float(imgHeight)
            self.__emotionImages[pair[0]] = pygame.transform.scale(
                    self.__emotionImages[pair[0]], (wndWidth, wndHeight)
            )

    def getEmotionImage(self, emotionName, w = 0, h = 0):
        emotionImage = None            
        if w == 0 or h == 0:
            emotionImage = self.__emotionImages[emotionName]            
        else:
            emotionImage = pygame.transform.scale(
                self.__emotionImages[emotionName],
                (w,h)
            )
        return emotionImage

    def getEmotionNames(self):
        return self.__emotionImages.keys()


        
        