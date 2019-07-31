# -*- coding: utf-8 -*-
import cv2
import sys

sys.path.append('../face')
import face

def faceDetectionDummy(img):
   
    # カスケード型識別器の読み込み
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 顔領域の探索
    aface = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    faces = []
    cnt = 0
    # 顔領域を赤色の矩形で囲む
    for (x, y, w, h) in aface:
        faceData = face.Face(cnt, [(x, y), (w, h)])
#        faceData.__rect = [(x,y), (w,h)]
        faceData.__face__id = cnt
        faces.append(faceData)
        cnt += 1
        print(faceData.rect())
        #print(str(faceData.x) + "," + str(faceData.y) + " ... " + str(w) + "x" + str(h))
    #for f in faces:
    #    print(str(f.x) + " " + str(f.y) + " " + str(f.width) + " " + str(f.id))
    return faces