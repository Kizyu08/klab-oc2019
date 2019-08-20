# -*- coding: utf-8 -*-

# 別途インストールが必要なライブラリ
#   - pillow : αチャンネルを元に透過処理するとき楽なので使用

import cv2

from PIL import Image
import numpy as np

import sys
sys.path.append('../face')
import face
import EmotionImages

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

class Decoration:
    # コンストラクタ
    def __init__(
        self,
        wndWidth,   # 描画領域の幅
        wndHeight   # 描画領域の高さ
    ):
        #print("Decoration : init() begin")
        self.__emotionImages = EmotionImages.EmotionImages(wndWidth, wndHeight) 
        #self.__debugLogFile = open("debugLogFile.txt", "w")
        #keys = ""
        #for key in face.Face().result().keys():
        #    keys = keys + key + " "
        #self.__debugLogFile.write(keys + "\n")
        #self.__debugLogFile.close()
        #print("Decoration : init() end")



    # 引数として渡された画像に対して
    # 表情スコアを基にフレームを付与するモジュール
    # 引数はすべて入力として扱う
    # 戻り値は加工した画像(opencv3形式)
    # スコアの合計値が高いものを尤もらしい表情として扱い，同値ならば辞書順で若い方を選ぶ
    def decorate(
        self,
        faces                               # Facesクラスのインスタンス
    ):
        if len(faces.face()) <= 0:
            return faces

        size = faces.image().shape[:2]
        if size <= 0:
		    return faces

        # 表情スコアの合計計算用の辞書型リストを用意する
        # 辞書型リストは表情名がキー，値はスコアとなっている
        # 詳しくはFaceクラス参照してください
        emotionSumScores = face.Face().result()

        # 念の為，各合計スコアを0.0で初期化する
        for emotionName in emotionSumScores.keys():
            emotionSumScores[emotionName] = 0.0

        # スコア別に合計を求める
        for aface in faces.face():
            emotionScores = aface.result()
            for emotionName in emotionScores.keys():
                emotionSumScores[emotionName] += emotionScores[emotionName]

        # スコアの合計が最大である表情の名称とそのスコアを取得する
        bestEmotion = BestEmotion("None", -1)        # 前回の結果を削除する
        for emotionName in emotionSumScores.keys():         # スコアが最大である表情の名称を検索する
            emotionScore = emotionSumScores[emotionName]    # 表情に対応するスコアを獲得する
#            if emotionScore == 0:                           # 表情スコアが０の場合は対象外
#                continue                                
            if emotionScore > bestEmotion.score:
                bestEmotion.set(emotionName, emotionScore)



        #print("--- self.__emotionImages.getEmotionImage(bestEmotion.name) type is")
        #print(type(self.__emotionImages.getEmotionImage(bestEmotion.name)))
        #print("---")

        bestEmotionImage = self.__emotionImages.getEmotionImage(bestEmotion.name)

        cvCapImg = cv2.cvtColor(faces.image(), cv2.COLOR_BGR2RGB)
        pilCapImg = Image.fromarray(cvCapImg)
        pilCapRGBAImg = pilCapImg.convert('RGBA')

        #print("[Type] bestEmotionImage : ")
        #print(type(bestEmotionImage))


        cvFrameImg = cv2.cvtColor(bestEmotionImage, cv2.COLOR_BGRA2RGBA)
        pilFrameImg = Image.fromarray(cvFrameImg)
        pilFrameRGBAImg = pilFrameImg.convert('RGBA')

        pilRGBATmp = Image.new('RGBA', pilCapRGBAImg.size, (255, 255, 255, 0))

        point = (0, 0)
        pilRGBATmp.paste(pilFrameRGBAImg, point, pilFrameRGBAImg)

        pilResImg = \
            Image.alpha_composite(pilCapRGBAImg, pilRGBATmp)

        cvResImg = cv2.cvtColor(
                    np.asarray(pilResImg), cv2.COLOR_RGBA2BGRA)


        # デバッグ表示、デバッグファイル出力
        #c = 1
        #valuesStr = ""
        #self.__debugLogFile = open("debugLogFile.txt", "a")
        #for scoreName in emotionSumScores.keys():
        #    cv2.putText(cvResImg, scoreName + " = " + str(emotionSumScores[scoreName]), (10, c*20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        #    valuesStr = valuesStr + " " + str(emotionSumScores[scoreName])
        #    c = c+1
        #self.__debugLogFile.write(valuesStr + "\n")
        #self.__debugLogFile.write("best emotion = " + bestEmotion.name + ", score = " + str(bestEmotion.score) + "\n")
        #self.__debugLogFile.write("\n")
        #self.__debugLogFile.close()



        #faces[0].decImg = cvResImg
        faces.set_image( cvResImg )

        return faces


