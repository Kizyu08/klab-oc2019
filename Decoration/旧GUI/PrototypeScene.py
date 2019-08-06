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
        self.videoType                = None
        self.drawLargeFrameFlag       = None
        self.drawFaceFramesFlag       = None
        self.drawDetectedRegionsFlag  = None

        # 初期設定ファイルを開く
        sceneInfoFile = open(pathOfSceneInfoFile, "r")

        # 初期設定ファイルが開けない場合は即終了
        if sceneInfoFile == None:
            print(pathOfSceneInfoFile + "が開けませんでした")
            exit()

        self.videoType                = int((sceneInfoFile.readline()).rstrip("\n"))
        self.drawLargeFrameFlag       = int((sceneInfoFile.readline()).rstrip("\n"))
        self.drawFaceFramesFlag       = int((sceneInfoFile.readline()).rstrip("\n"))
        self.drawDetectedRegionsFlag  = int((sceneInfoFile.readline()).rstrip("\n"))

# 尤もらしい表情の名称とスコアを保管するクラス...もとい構造体
# 尤もらしさは仮で各表情別に全顔のスコアの合計値を求め
# 合計値が最大となるものを尤もらしい表情としている
class BestEmotion:
    def __init__(self, name = "None", score = -1):
        self.name    = name
        self.score   = score

    def set(self, name, score):
        self.name    = name
        self.score   = score

# シーンクラス
# 画面内の処理を行う
# （顔の検出やスコアの計算、カメラからの映像やフレームの描画、等）
class PrototypeScene(IScene.IScene):
    # コンストラクタ
    def __init__(self, window):
        # メンバ変数の初期化 ---------------------------------------------------
        super(PrototypeScene, self).__init__(window)
        self.__sceneID = IScene.SceneID.PROTOTYPE_SCENE
        self.__sceneInfo = SceneInfo()

        self.__bestEmotion = BestEmotion()

        self.__window = window                  # シーンを扱うウィンドウを取得する
        self.__initFlags()                      # シーン終了フラグをOFFにする
        self.__sceneEventId = SceneEventID.SceneEventID()    # シーンイベントを初期化する

        self.__videoCapture = VideoCapture.VideoCapture(
                                window, 
                                self.__sceneInfo.videoType
                            )

        # フレーム等の表示/非表示フラグの初期設定を行う
        self.__initDrawFlags()

        self.__faces = faces.Faces(self.__videoCapture.getCaptureImage())                  # 顔リストクラスの初期化を行う

        self.__emotionImages = EmotionImages.EmotionImages(
            self.__window.getWidth(),
            self.__window.getHeight()
        )


# 外部から呼び出されるメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # 更新処理のメインとなるメソッド
    def update(self):
        self.__videoCapture.update()
        self.__eventCheck()         # シーンイベントを確認する
        self.__doEvent()            # シーンイベントを実行する
        return True

    # 描画処理のメインとなるメソッド
    def draw(self):
        self.__drawCaptureImage()       # カメラからの画像を描画する

        # 各顔を表情スコアが最大となる表情のフレームで囲うようにフレームを描画する
        if self.__isDrawFaceFrames:
            self.__drawFrameByFaces()       
        
        # 各顔の検出位置を示す矩形を表示する
        if self.__isDrawDetectedRegions:
            self.__drawDetectedRegions()

        # 画面全体を覆うフレームを描画する
        if self.__isDrawLargeFrame:
            self.__drawFrame()

        self.__window.reverseScreen()   # カメラからの映像は鏡合わせになるので左右反転させる

        return True

    # シーンが終了状態かどうか取得する
    def isExit(self):
        return self.__isExitFlag

    # 次のシーンのIDを取得する
    def getNextSceneID(self):
        return IScene.SceneID.NONE


# 初期化(__init__)関連のメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

    # フラグ関連一式の初期設定を行う
    def __initFlags(self):
        self.__isExitFlag = False               # シーン終了フラグをOFFにする
        self.__initDrawFlags()                  # 表示/非表示関連のフラグの初期設定を行う

    # 表示/非表示関連のフラグの初期設定を行う
    def __initDrawFlags(self):
        self.__isDrawLargeFrame         = self.__sceneInfo.drawLargeFrameFlag
        self.__isDrawFaceFrames         = self.__sceneInfo.drawFaceFramesFlag
        self.__isDrawDetectedRegions    = self.__sceneInfo.drawDetectedRegionsFlag


# 描画(__draw)関連のメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # 検出箇所を描画するメソッド
    def __drawDetectedRegions(self):
        for aface in self.__faces.face():
            rect = aface.rect()
            (x, y), (w, h) = rect
            rectPygame = pygame.Rect(x, y, w, h)
            rgb = (0, 255, 0)
            self.__window.drawRect(rgb, rectPygame, 2)

    # 各顔を表情スコアが最大となる表情のフレームで囲うようにフレームを描画するメソッド
    def __drawFrameByFaces(self):
        resizedFrames = []
        facelist = self.__faces.face()
        frameImage = None
        for aface in facelist:
            likelyEmotionName   = None
            maxScore            = -1
            emotionScores = aface.result()
            rect = aface.rect()
            (x, y), (w, h) = rect
            for emotionName in emotionScores.keys():
                score = emotionScores[emotionName]
                if score > maxScore:
                    maxScore = score
                    likelyEmotionName = emotionName
            frameImage = self.__emotionImages.getEmotionImage(likelyEmotionName, w, h)
            if frameImage:
                self.__window.drawImg(frameImage, x, y)


    # カメラから読み込んだ画像を描画するメソッド
    def __drawCaptureImage(self):
        self.__window.drawImg(self.__videoCapture.getCaptureImageForPygame(), 0, 0)

    
    # フレームを描画するメソッド
    def __drawFrame(self):
        if self.__bestEmotion == None:
            return
        
        if self.__bestEmotion.name in self.__emotionImages.getEmotionNames():
            self.__window.drawImg(
                self.__emotionImages.getEmotionImage(self.__bestEmotion.name),
                0, 0
            )
        else:
            print('\"Face\" クラスに存在しない表情名' + "\"" + self.__bestEmotion.name + "\"が尤もらしい表情として指定されました．")

# 更新(__update)関連のメソッド ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    # シーンの現在行うべきイベントを確認する
    def __eventCheck(self):
        self.__sceneEventId.set(SceneEventID.SceneEventID.NON)                      # イベントIDの記録を初期化
        for event in pygame.event.get():                                            # イベントを確認
            # ウィンドウの×ボタンが押された場合
            if event.type == pygame.QUIT:
                self.__sceneEventId.set(SceneEventID.SceneEventID.EXIT_SCENE)
                break
            # 何かしらキーが押された場合
            elif event.type == KEYUP:
                # [ESC]：シーンを終了状態にするフラグを立てる
                if event.key == K_ESCAPE:   
                    self.__sceneEventId.set(SceneEventID.SceneEventID.EXIT_SCENE)
                # [S]：現在画面に表示されている画像を保存するフラグを立てる
                elif event.key == K_s:      
                    self.__sceneEventId.set(SceneEventID.SceneEventID.SAVE_IMAGE)
                # [1]：画面を覆うフレームの表示/非表示を切り替えるフラグを反転させる
                elif event.key == K_1:
                    self.__isDrawLargeFrame = not self.__isDrawLargeFrame 
                # [2]：各顔を覆うフレームの表示/非表示を切り替えるフラグを反転させる
                elif event.key == K_2:
                    self.__isDrawFaceFrames = not self.__isDrawFaceFrames 
                # [3]：各顔の検出位置を示す矩形の表示/非表示を切り替えるフラグを反転させる
                elif event.key == K_3:
                    self.__isDrawDetectedRegions = not self.__isDrawDetectedRegions 
        if self.__sceneEventId.isNon():
            self.__sceneEventId.set(SceneEventID.SceneEventID.COMPUTE_SCORES)

    # 顔リストに格納された表情スコアを元に画面へ表示するフレームを選択するメソッド
    def __selectDrawFrameByFaces(self):
        # 表情スコア計算用の
        # 辞書型リストを取得する
        emotionSumScores = face.Face().result()

        # 念の為、初期化する
        for emotionName in emotionSumScores.keys():
            emotionSumScores[emotionName] = 0.0

        # 顔を検出する
        self.__faces = self.__detectFaces()
        
        # 各顔の表情スコアを求める
        self.__faces = self.__computeFaceScores(self.__faces)

        # スコア別に合計を求める
        faceList = self.__faces.face()
        for aface in faceList:
            emotionScores = aface.result()
            for emotionName in emotionScores.keys():
                emotionSumScores[emotionName] += emotionScores[emotionName]
        
        # スコアの合計が最大である表情の名称とそのスコアを取得する
        self.__bestEmotion = BestEmotion("None", -1)        # 前回の結果を削除する
        for emotionName in emotionSumScores.keys():         # スコアが最大である表情の名称を検索する
            emotionScore = emotionSumScores[emotionName]    # 表情に対応するスコアを獲得する
            if emotionScore == 0:                           # 表情スコアが０の場合は対象外
                continue                                
            if emotionScore > self.__bestEmotion.score:
                self.__bestEmotion.set(emotionName, emotionScore)


    # 顔を検出するメソッド
    # 実装は他の人が行うので担当外
    # 仮実装として顔の検出数や位置等は乱数
    def __detectFaces(self):
        faces = FaceDetectionDummy.faceDetectionDummy(self.__videoCapture.getCaptureImage())
        return faces

    # 検出された顔の表情スコアを求めるメソッド
    # 実装は他の人が行うので担当外
    def __computeFaceScores(self, facesObj):
        emotionNames = self.__emotionImages.getEmotionNames()
        maxSizeFace = face.Face()
        faceList = facesObj.face()
        (x, y), (w, h) = maxSizeFace.rect()
        for aface in faceList:
            (cx, cy), (cw, ch) = aface.rect()
            if cw > w:
                w = cw
        for aface in faceList:
            (x, y), (w, h) = aface.rect()
            cnt = 0
            pos = int(w / 25) % len(emotionNames)
            emotionScores = aface.result()
            for emotionName in emotionScores.keys():
                if cnt == pos:
                    emotionScores[emotionName] = 1.0
                else:
                    emotionScores[emotionName] = 0
                cnt += 1
        return facesObj

    # 画面の内容を画像として保存する
    def __saveImage(self):
        filename = "./" + datetime.datetime.today().strftime('%Y-%m-%d_%H_%M_%S') + ".jpg"
        print("saved : " + filename)
        self.__window.saveDisp(filename)
    
    # シーンを終了する
    def __exitScene(self):
        self.__isExitFlag = True

    # シーンイベントを実行する
    def __doEvent(self):

        if self.__sceneEventId.isComputeScores():
            self.__selectDrawFrameByFaces()

        elif self.__sceneEventId.isSaveImage():
            self.__saveImage()

        elif self.__sceneEventId.isExitScene():
            self.__exitScene()

        else:
            print("Non Event Now")
