# -*- coding: utf-8 -*-

# OCGUI ... Open Campus Graphical User Interface

import pygame
from pygame.locals import *
import codecs
import Util
import Face
import sys
sys.path.append('./face')
import face
import Window
import numpy as np
import cv2
import matplotlib.pyplot as plt
import datetime
import Scene
import MakeScene

class OCGUI:
    __dirPathOfInitInfoFiles   = './init'
    __pathOfInitInfoForWindow = __dirPathOfInitInfoFiles + '/window.info'

    # コンストラクタ
    def __init__(self):
        # ウィンドウの初期設定を行う
        self.__initWindow()
        # シーンを作成する
        self.__scene = Scene.Scene(self.__window)


    # 描画処理を行うメソッド
    def __draw(self):
        self.__window.fill()    # ウィンドウの描画内容を消す
        self.__scene.draw()     # 描画処理を行う
        self.__window.flip()    # バッファに描画された内容を画面へ表示する
    

    # 更新処理を行うメソッド
    def __update(self):       
        self.__scene.update()   # シーンの状態を更新する


    # メインループ用のメソッド
    def do(self):
        # Sceneが終了状態出ない限りループ
        while self.__scene.isRunning():
            self.__draw()                   # 描画処理
            self.__update()                 # 更新処理  
            
            if self.__scene.isExit():
                self.__scene = MakeScene.makeScene(
                    self.__scene.getNextSceneID(),
                    self.__window
                )

            self.__clock.tick(self.__FPS)   # FPS調整
         # ウィンドウを閉じる
        self.__window.quit()               


    # ウィンドウの初期設定を行うメソッド
    def __initWindow(self):
        # ウィンドウに関する情報を読み込む
        windowInfoFile  = open(self.__pathOfInitInfoForWindow, 'r')     # ウィンドウの初期設定が記述されたファイルを開く
        windowCaption   = windowInfoFile.readline()                     # ウィンドウのキャプションを読み込む
        windowCaption   = windowCaption.strip("\n")                     # readlineでは改行"\n"も読み込まれるので"\n"を削除する
        windowSize      = windowInfoFile.readline().split()             # 空白区切りでウィンドウサイズを読み込む
        windowSize      = [ int(windowSize[0]), int(windowSize[1]) ]    # 読み込まれたデータは文字列なので各々をint型へ変換する
        windowBgColor   = windowInfoFile.readline().split()             # ウィンドウの画面の初期RGBを設定する
        windowFontName  = windowInfoFile.readline()                     # 読み込まれたデータは文字列なので各々をint型へ変換する
        windowFontName  = windowFontName.strip("\n")                    # フォントの名前を読み込む
        windowFontSize  = int(windowInfoFile.readline())                # フォントのサイズを読み込む
        windowFontColor = windowInfoFile.readline().split()             # フォントの色を設定する
        windowFontColor = [ int(windowFontColor[0]),                    # 読み込まれたデータは文字列なので各々をint型へ変換する
                            int(windowFontColor[1]), 
                            int(windowFontColor[2]),
                          ]
        windowFPS       = int( (windowInfoFile.readline()).strip("\n") )# FPSを読み込む

        self.__window = Window.Window(windowSize[0], windowSize[1])                         # ウィンドウを作成する
        self.__window.setWindowCaption(windowCaption)                                       # ウィンドウのキャプションを作成する
        self.__window.setFont(                                                              # ウィンドウで使用されるフォントを設定する
            windowFontName,                                                                 # フォント名
            windowFontSize,                                                                 # フォントサイズ
            [ int(windowFontColor[0]), int(windowFontColor[1]), int(windowFontColor[2]) ]   # フォントの色（R,G,B）
        )
        self.__clock = pygame.time.Clock()                                                  # FPS計算用のインスタンスを作成
        self.__FPS = windowFPS                                                              # FPSを設定する
