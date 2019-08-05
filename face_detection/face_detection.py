import cv2
#import Face


def face_detection(c_frame, window=False):
    # 定数定義
    ORG_WINDOW_NAME = "org"
    GAUSSIAN_WINDOW_NAME = "gaussian"

#    face = Face()

    # 分類器の指定
    cascade_file = "haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(cascade_file)

    height, width, channels = c_frame.shape

    # ウィンドウの準備
    if window:
        cv2.namedWindow(ORG_WINDOW_NAME)
        cv2.namedWindow(GAUSSIAN_WINDOW_NAME)


    # 画像の取得と顔の検出
    img = c_frame
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))

    # 検出した顔に印を付ける
    for (x, y, w, h) in face_list:
        color = (0, 0, 225)
        pen_w = 3
        cv2.rectangle(img_gray, (x, y), (x+w, y+h), color, thickness = pen_w)
        #print( str(w) +','+ str(h))

    # フレーム表示
    if window:
        cv2.imshow(ORG_WINDOW_NAME, c_frame)
        cv2.imshow(GAUSSIAN_WINDOW_NAME, img_gray)
    
    

    return len(face_list), face_list 

if __name__ == '__main__':
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL = 33     # 待ち時間
    DEVICE_ID = 0

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 初期フレームの読込
    end_flag, frame = cap.read()

    # 変換処理ループ
    while end_flag == True:
        length, faces = face_detection(frame, window=True)
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
