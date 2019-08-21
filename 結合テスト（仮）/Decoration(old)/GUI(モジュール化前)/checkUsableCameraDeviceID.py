import cv2
import warnings

warnings.filterwarnings('ignore')

deviceIdListFile = open("./usableDeviceIdList.txt", "w")

cap = None

for id in range(-1, 65535, 1):
    cap = cv2.VideoCapture(id)    
    if cap.isOpened():
        cap.release()
        deviceIdListFile.write(str(id) + "\n")

