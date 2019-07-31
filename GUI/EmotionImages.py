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
    def __init__(self, pathOfEmotionImagesList = "./frame/emotionImagesList.txt"):
        self.__emotionImages = {}       # 表情と表情に対応する画像を格納する辞書型リスト {(表情名,画像), ...}
        emotionNames =                  # 表情名を一通り取得する        
            Face.Face().result().keys() # 表情名が辞書型リストのキーになっている（と信じたい）

        # 表情名と表情に対応する画像ファイルのパスが対で記述されたファイルを開く
        emotionImagesListFile = open(pathOfEmotionImagesList, "r")

        # ファイルが開けない場合は強制終了
        if not emotionImagesListFile.isOpen():
            print("\"" + pathOfEmotionImagesList + "\"の読み込みに失敗しました")
            exit()

        for emotionName in emotionNames:


        pathListEmotionImages = {}      # 各表情に対応するフレーム画像各々のファイルパスを格納する辞書型リスト {(表情名, ファイルパス)}
        
        