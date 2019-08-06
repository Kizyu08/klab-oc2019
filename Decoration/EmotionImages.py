# -*- coding: utf-8 -*-

import codecs
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import datetime
import random

sys.path.append('../face')
import face



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
            #self.__emotionImages[pair[0]] = pygame.image.load("./frame/" + pair[1])
            self.__emotionImages[pair[0]] = cv2.imread("frame/" + pair[1], cv2.IMREAD_UNCHANGED)
            self.__emotionImages[pair[0]] = cv2.resize(
                self.__emotionImages[pair[0]], 
                dsize=(wndWidth, wndHeight)
            )
            

    def getEmotionImage(self, emotionName, w = 0, h = 0):
        emotionImage = None
        if not emotionName in self.__emotionImages.keys():
            print("[error] EmotionImages.getEmotionImage : " + emotionName + " is not exit emotion name")
            return None
        elif w == 0 or h == 0:
            emotionImage = self.__emotionImages[emotionName]            
        else:
            emotionImage = cv2.resize(
                self.__emotionImages[emotionName], 
                dsize=(wndWidth, wndHeight)
            )

        return emotionImage

    def getEmotionNames(self):
        return self.__emotionImages.keys()


        
        