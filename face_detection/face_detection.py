import cv2
import sys
sys.path.append('../face')
import face
import faces

def face_detection(facesIn, window=False):
    """画像を持ったfacesクラスをブチ込むとfaceを入れて返すクラス"""
    """in:faces out:faces"""
    # 定数定義
    ORG_WINDOW_NAME = "org"
    GAUSSIAN_WINDOW_NAME = "gaussian"

    # 分類器の指定
    cascade_file = "haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(cascade_file)

    height, width, channels = facesIn.image().shape

    # ウィンドウの準備
    if window:
        cv2.namedWindow(ORG_WINDOW_NAME)
        cv2.namedWindow(GAUSSIAN_WINDOW_NAME)

    # 画像の取得と顔の検出
    img = facesIn.image()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))

    # 検出した顔に印を付ける
    for (x, y, w, h) in face_list:
        color = (0, 0, 225)
        pen_w = 3
        cv2.rectangle(img_gray, (x, y), (x+w, y+h), color, thickness = pen_w)
        
        facesIn.set_face(face.Face(0, [(x, y), (w, h)]))
        #print( str(w) +','+ str(h))

    # フレーム表示
    if window:
        cv2.imshow(ORG_WINDOW_NAME, img)
        cv2.imshow(GAUSSIAN_WINDOW_NAME, img_gray)

    return facesIn

if __name__ == '__main__':
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL = 33     # 待ち時間
    DEVICE_ID = 0

    

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 初期フレームの読込
    end_flag, img = cap.read()
    print(img.shape)

    FacesIns = faces.Faces(img)
    print(FacesIns.image().shape)

    # 変換処理ループ
    while end_flag == True:
        FacesIns = face_detection(FacesIns, window=True)
        

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
                break

        # 次のフレーム読み込み
        end_flag, img = cap.read()
        FacesIns.set_image(img)


    # 終了処理
    cv2.destroyAllWindows()
    cap.release()
