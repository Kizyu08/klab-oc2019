# -*- coding: utf-8 -*-
import sys
sys.path.append('../face')
from face import Face
from faces import Faces
import cv2
import chainer
from CNN import ClassificationModel
import CNN
import numpy as np
import chainer.cuda as cuda


def emotion(data):
    

    
    input_image_size = [40,40]
    gpu_use = True
    cnn = ClassificationModel()
    chainer.serializers.load_npz("cnn.npz", cnn)
    
    cnn.to_gpu(0)
 
    
    facelist = data.face()
    img = data.image()
    image_datas = []
    

    capH, capW = img.shape[:2]


    # 画像の切り出し
    for i in range (len(facelist)):
        (x,y), (width,height)=facelist[i].rect()
        print("x,y = " + str(x) + ", " + str(y))
        print("wid,hei = " + str(width) + ", " + str(height))
        right=(x+width)
        btm  = (y+height)
        img_dist = img[y:btm, x:right]
        image_datas.append(img_dist)
        height, width = img_dist.shape[:2]
        print("Rect size = " + str(width) + " x " + str(height))

		
    
    identification_image_datas = []
    size = (input_image_size[0], input_image_size[1])
    for i in range(len(image_datas)):
    	image = cv2.resize(image_datas[i], size)
    	identification_image_datas.append(CNN.cv_ch_sort(image))
    
    identification_image_datas = np.array(identification_image_datas, dtype=np.float32).reshape(-1,1,input_image_size[0],input_image_size[1])
    if gpu_use == True:
    	identification_image_datas = cuda.to_gpu(identification_image_datas, device = 0)
    identification_image_datas = chainer.Variable(identification_image_datas)
    
    identification_output = cnn.identification(identification_image_datas)
    #print("neutral,happiness,surprise,sadness,anger,disgust,fear,contempt,unknown,NF")
    
    #スコアの書き出し
    for i in range (len(facelist)):
        data.face()[i].set_result(identification_output[i][0],identification_output[i][1],identification_output[i][2],identification_output[i][3],identification_output[i][4],identification_output[i][5],identification_output[i][6],identification_output[i][7],identification_output[i][8])
    
    
    return data

