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
        self.__emotionImages = EmotionImages.EmotionImages(wndWidth, wndHeight) 

    # 引数として渡された画像に対して
    # 表情スコアを基にフレームを付与するモジュール
    # 引数はすべて入力として扱う
    # 戻り値は加工した画像(opencv3形式)
    # スコアの合計値が高いものを尤もらしい表情として扱い，同値ならば辞書順で若い方を選ぶ
    def decorate(
        self,
        faces                               # Facesクラスのインスタンス
    ):
        # 表情スコアの合計計算用の辞書型リストを用意する
        # 辞書型リストは表情名がキー，値はスコアとなっている
        # 詳しくはFaceクラス参照してください
        emotionSumScores = face.Face().result()

        # 念の為，各合計スコアを0.0で初期化する
        for emotionName in emotionSumScores.keys():
            emotionSumScores[emotionName] = 0.0

        # スコア別に合計を求める
        for aface in faces:
            emotionScores = aface.result()
            for emotionName in emotionScores.keys():
                emotionSumScores[emotionName] += emotionScores[emotionName]

        # スコアの合計が最大である表情の名称とそのスコアを取得する
        bestEmotion = BestEmotion("None", -1)        # 前回の結果を削除する
        for emotionName in emotionSumScores.keys():         # スコアが最大である表情の名称を検索する
            emotionScore = emotionSumScores[emotionName]    # 表情に対応するスコアを獲得する
            if emotionScore == 0:                           # 表情スコアが０の場合は対象外
                continue                                
            if emotionScore > bestEmotion.score:
                bestEmotion.set(emotionName, emotionScore)

        bestEmotionImage = self.__emotionImages.getEmotionImage(bestEmotion.name)

        cvCapImg = cv2.cvtColor(faces[0].capImg, cv2.COLOR_BGR2RGB)
        pilCapImg = Image.fromarray(cvCapImg)
        pilCapRGBAImg = pilCapImg.convert('RGBA')

        if bestEmotionImage is None:
            print("failed to get best emotion image")
            return cvImg

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

        faces[0].decImg = cvResImg

        return faces


if __name__ == '__main__':
    import VideoCapture
    import FaceDetectionDummy
    import computeFaceScoresDummy

    cap = VideoCapture.VideoCapture()

    decoration = Decoration(640, 480)

    while True:
        key =  cv2.waitKey(1)
        if key == 27:
            break

        cap.update()
        img = cap.getCaptureImage()
        faces = FaceDetectionDummy.faceDetectionDummy(img)
        faces = computeFaceScoresDummy.computeFaceScoresDummy(faces)
        if len(faces) <= 0:
            print("faces is failed") 
        faces = decoration.decorate(faces)
        cv2.imshow("test", faces[0].decImg)

    print "a"


