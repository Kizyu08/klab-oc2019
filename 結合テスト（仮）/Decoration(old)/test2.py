import sys
sys.path.append('../Decoration')
import EmotionImages
import cv2

if __name__ == '__main__':
    ei = EmotionImages.EmotionImages()
    cv2.imshow("test", ei.getEmotionImage("neutral"))
    cv2.waitKey(0)
    print("a")