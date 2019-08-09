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

import IScene
import Util
import Window
import SceneEventID
import FaceDetectionDummy
import EmotionImages
import VideoCapture

sys.path.append('../face')
import face
import faces

# 構造体...pytho2に構造体ないのでclassで代用
class SceneInfo:
    def __init__(self, pathOfSceneInfoFile = "./init/scene.info"):
        self.videoType = 0



class Event:
    def __init__(self, window):
        ''' '''


class PlayGameScene(IScene.IScene):
# 外部から呼び出されるメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # コンストラクタ
    def __init__(self, window):
        # スーパークラスのコンストラクタを呼び出す
        super(PlayGameScene, self).__init__(window)    
        
        # シーンの初期設定が記述されたファイルを読み込む
        self.__readSceneInfo()

        # 対象となるウィンドウを設定する
        self.__initWindow(window)

        # シーンIDを初期化する
        self.__initSceneID()

        # タイマーを初期化する
        self.__initTimer()

        # 獲得スコアを初期化する
        self.__initScore()

        # カメラキャプチャーを初期化する
        self.__initCameraCapture()

        # 各フラグ変数を初期化する
        self.__initFlags()

        # 描画に使用する画像を読み込む
        self.__initImages()

    # 更新処理
    def update(self):
        # カメラキャプチャーを更新する
        self.__videoCapture.update()
        
        # 雑実装
        # 必要に応じて修正とメソッド化
        # ESCキー or ×ボタンでシーンもといプログラム全体を終了
        for event in pygame.event.get():                                            # イベントを確認
            # ウィンドウの×ボタンが押された場合
            if event.type == pygame.QUIT:
                exit()
                break
            # 何かしらキーが押された場合
            elif event.type == KEYUP:
                # [ESC]：シーンを終了状態にするフラグを立てる
                if event.key == K_ESCAPE:   
                    exit()
        return True

    # 描画処理
    def draw(self):
        # カメラからキャプチャーした画像を描画する
        self.__drawCaptureImage()
    
        # カメラからの映像は鏡合わせになるので左右反転させる
        self.__window.reverseScreen()

        # 文字描画テスト
        self.__window.drawText("00", 100, 100, 100, (100, 100, 100))
        return True


    # シーンが終了状態かどうか返す
    def isExit(self):
        return self.__isExitFlag == True

    # 次のシーンのIDを返す
    def getNextSceneID(self):
        return IScene.SceneID.NONE


# 初期化処理で使用するメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # シーンの初期設定が記述されたファイルを読み込む
    def __readSceneInfo(self):
        self.__sceneInfo = SceneInfo()

    # 対象となるウィンドウを設定する
    def __initWindow(self, window):
        self.__window = window

    # シーンIDを初期化する
    def __initSceneID(self):
        self.__sceneID = IScene.SceneID.PLAY_GAME_SCENE

    # タイマーを初期化する
    def __initTimer(self):
        ''' '''

    # 獲得スコアを初期化する
    def __initScore(self):
        ''' '''

    # カメラキャプチャーを初期化する
    def __initCameraCapture(self):
        self.__videoCapture = VideoCapture.VideoCapture(
            self.__window,
            self.__sceneInfo.videoType
        )

    # 各フラグ変数を初期化する
    def __initFlags(self):
        self.__isExitFlag = False

    # 描画に使用する画像を読み込む
    def __initImages(self):
        ''' images is anything '''

# 更新処理で使用されるメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# 描画処理で使用されるメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # カメラからキャプチャーした画像を描画するメソッド
    def __drawCaptureImage(self):
        self.__window.drawImg(
            self.__videoCapture.getCaptureImageForPygame(), 
            0, 
            0
        )



# その他 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # シーンを終了する
    def __exitScene(self):
        self.__isExitFlag = True
