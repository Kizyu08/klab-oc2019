# -*- coding: utf-8 -*-
import cv2
import sys

sys.path.append('../face_detection')
import sebcam

def main():
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL = 33     # 待ち時間
    DEVICE_ID = 0

    # カメラ映像取得
    cap = cv2.VideoCapture(1)

    # 初期フレームの読込
    end_flag, frame = cap.read()

    # 変換処理ループ
    while end_flag == True:
        length, faces = sebcam.detectface(frame, window=True)
        print(length)
        print(faces)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
                break

        # 次のフレーム読み込み
        end_flag, frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()


main()







'''
    # 入力画像の読み込み
    img = cv2.imread("2019-07-25_18_16_13.jpg")
    
    # カスケード型識別器の読み込み
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 顔領域の探索
    face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    
    # 顔領域を赤色の矩形で囲む
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y+h), (0,0,200), 3)

    # 結果を出力
    cv2.imwrite("result.jpg",img)

        
if __name__ == '__main__':
    main()
'''