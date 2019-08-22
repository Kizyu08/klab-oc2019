# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from kaogei.models import *

from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

import requests
import json

import base64
import cv2
import numpy as np
import io

from django.http.response import JsonResponse

# 顔芸モジュール
import sys
sys.path.append('./kaogei/face')
import face
import faces
sys.path.append('./kaogei/face_detection')
import face_detection
sys.path.append('./kaogei/face_emotion')
import ident
sys.path.append('./kaogei/Decoration')
import Decoration
import EmotionImages

decorator = Decoration.Decoration(640, 480)


@csrf_exempt
def index(request):
    print("[debug] index Begin -----------------------------------------------------------------")

    #message = request.POST.get("data", "World")
    #dic = {"msg": message}

    # リクエストからJSON文字列を取得する
    jsonStr = request.body
    if len(jsonStr) <= 0:
        print("[debug] input image is empty")
        return JsonResponse({"input image is empty": -1})
    print("[debug] obtained request")

    # JSON文字列を辞書型リストへ変換する
    datas = json.loads(jsonStr)
    print("[debug] converted json string to dictionary list")

    # base64形式でエンコードされた画像の文字列を取得する
    base64Img = datas["data"]
    base64Img = dummyBase64
    print("[debug] obtained base64 image from json string")

    # エンコードされた画像をデコードする
    binImg = base64.b64decode(base64Img)
    jpgImg = np.frombuffer(binImg,dtype=np.uint8)	
    print("[debug] converted base64 image to jpg image")

    # デコードして得られた画像をopenCV形式へ直す
    cvImg = cv2.imdecode(jpgImg, cv2.IMREAD_COLOR)
    print("[debug] converted jpg image to opencv format")

    # 
#    cv2.imshow("test",cvImg)
#    cv2.waitKey(0)

    # 顔リストクラスのインスタンスを作成する
    facesData = faces.Faces(cvImg)
    facesData.set_image(cvImg)
    print("[debug]  made faces class's instans")

    # 顔の検出を行う
    facesData = face_detection.face_detection(facesData)
    if len(facesData.face()) <= 0:
        print("[debug] faces was not detectioned")
        return render(request, 'test.html', dic)
    print("[debug] detected faces")

    # 各顔の各表情スコアを算出する
    facesData = ident.emotion(facesData)
    print("[debug] computed emotions' scores")

    # 装飾する
    facesData = decorator.decorate(facesData)
    print("[debug] decorated capture image")

    # 装飾画像をエンコードする
    result, encImg = cv2.imencode('.jpg', facesData.image())
    base64DecImg = base64.b64encode(encImg)
    print("[debug] encoded a decorated image")

    #cv2.imshow("decorated", facesData.image())
    #cv2.waitKey(0)

    # 元画像・装飾した画像をポストする
    imgList = {"origin" : base64Img, "decorated" : base64DecImg}
    #imgListJson = json.dumps(imgList)
    #sess = requests.session()
    #csrftoken = sess.cookies['csrftoken']
    #headers = {'Content-type': 'application/json',  "X-CSRFToken": csrftoken}
    headers = {'Content-type': 'application/json'}
    #url = "http://localhost:8000/register_pictures/"
    url = "https://133.15.123.97:8000/api2/register_pictures/"
    #pictureID = sess.post(url, data=imgListJson, headers=headers)
    #pictureID = requests.post(url, data=imgListJson, headers=headers)
    pictureID = requests.post(url, headers=headers, data=imgList)
    print("[debug] posted json string of origin capture image and decorated capture image")

    # 各顔の情報をポストする
    #url = "http://localhost:8000/api/faces/"
    url = "https://133.15.123.97:8000/api/faces/"
    for faceData in facesData.face():
        score = 0.0
        (x1, y1), (width, height) = faceData.rect()
        x2 = x1 + width
        y2 = y1 + height
        for emotionName in faceData.result().keys():
            tempScore = faceData.result()[emotionName]
            if score < tempScore:
                score = tempScore
        #faceDataList = {"picture_id" : pictureID, "score" : score, "position" : {"x1" : x1, "y1" : y1, "x2" : x2,"y2" : y2}, }
        faceDataList = {"picture_id": str(pictureID), "score": str(score), "position": {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2)}, }
        #faceDataList = "{:" + str(pictureID) + ",score :" + str(score) + ", position:{x1:" + str(x1) + ",y1:" + str(y1) + ", x2:" + str(x2) + ", y2:" +  str(y2) + "}, }"
        print(faceDataList)

#        faceDataJson = json.dumps(faceDataList)
        #print(faceDataJson)
        # POST送信
#        res = requests.post(url, data=faceDataJson, headers=headers)
        #res = requests.post(url, data=faceDataList, headers=headers)
        res = requests.post(url, headers=headers, data=faceDataList)
    print("[debug] posted json string of faces data")

    # JSON文字列をデータ(辞書)に戻す
    #datas = json.loads(request.body)

    # base64でエンコードされた画像の文字列を取得する
    #base64Img = datas["data"]

    # return JsonResponse({"picture_id": pictureID})
    print("[debug] index End ---------------------------------------------------------------------------------------------------------")
    return JsonResponse({"picture_id": 2})

    #return render(request, 'test.html', dic)

    
