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
import faces
import IScene
import Util
import Window
import SceneEventID
import FaceDetectionDummy
#import EmotionImages
sys.path.append('../Decoration')
import EmotionImages

VIDEO_TYPE_DEFALT = 0

class VideoCapture:
    # コンストラクタ
    def __init__(self, window, videoType = VIDEO_TYPE_DEFALT):
        self.__captureImage             = None
        self.__captureImageForPygame    = None
        self.__videoType                = videoType

        # 引数： 0...内蔵カメラ　1...USB接続カメラ
        # ※ ぶっちゃけ環境依存なので付属pythonプログラム "checkUsableCameraDeviceID.py"
        # を実行して出力される"usableDeviceList.txt"を確認してください
        self.__cameraCapture = cv2.VideoCapture(videoType)  

        # カメラ（ビデオ）の読み込みができる場合
        if self.__cameraCapture.isOpened():
            self.__readVideoCapture()
        else:
            print("ID(orファイル)" + str(self.__videoType) + "は読み込みできません")

    # クラスの情報を更新する
    def update(self):
        self.__readVideoCapture()

    # カメラから映像１フレーム分を読み込むメソッド
    def __readVideoCapture(self):
        isSuccessed, captureImage = self.__cameraCapture.read()   
        if isSuccessed:
            self.__captureImage = captureImage                                              # まず、普通にOpenCVで使用可能な形式で読み込み、
            self.__captureImageForPygame = Util.cvtOpenCVImgToPygame(self.__captureImage)   # これをpygameで使用可能な形式へと変換する
        else:
            print("failed to read video camera image...")
            size = self.__window.getHeight(), self.__window.getWidth(), 3
            contours = np.array( [ [0,0], [0,size[1]], [size[0], size[1]], [size[0],0] ] )
            #dummy = np.zeros(size, dtype=np.uint8)
            dummy = None

    # 読み込んだ画像を取得する(OpenCV形式)
    def getCaptureImage(self):
        print("[debug] ******************: getCaptureImage :************************")
        print(type(self.__captureImage))
        print("[debug] ******************: getCaptureImage :************************ end")
        return self.__captureImage

    # 読み込んだ画像を取得する(pygame形式)
    def getCaptureImageForPygame(self):
        return self.__captureImageForPygame
