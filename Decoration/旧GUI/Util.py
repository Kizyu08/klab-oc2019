# -*- coding: utf-8 -*-
import pygame
import codecs
import Util
import Window
import sys
import numpy as np
import cv2
import numpy


def getListValue(key, list):
    values = [x['Value'] for x in list if 'Key' in x and 'Value' in x and x['Key'] == key]
    return values[0] if values else None

def cvtOpenCVImgToPygame(opencvImg):
    # RGBがOpenCVとPygameでは順序が反対なので画素毎に逆順にする
    #opencvImgCpy = opencvImg[:,:,::-1]
    opencvImgCpyR = cv2.cvtColor(opencvImg, cv2.COLOR_BGR2RGB)

    # 画像の幅,高さを取得する
    #  shape[] = {列数, 行数, チャンネル数}
    #  pygame形式へ変換するには{幅, 高さ}の順で格納でされたコンテナがほしい
    #  よって、shape = {行数, 列数} となるようにopencv.shapeから情報を取得する
    shape = opencvImgCpyR.shape[1::-1]

    # 画像を生成して戻り値として返す
    return pygame.image.frombuffer(opencvImgCpyR.tostring(), shape, 'RGB')
        