# coding: UTF-8
#!/usr/bin/env python

import random
#import argparse
import numpy
#import copy
import glob
import cv2

import pandas as pd

import chainer
import chainer.optimizers
import chainer.serializers
import chainer.functions as F
import chainer.links as L

## gpu
import chainer.cuda as cuda
import cupy
import cupy.cuda
from cupy.cuda import cudnn

#----------------------------------------------------

csvfile = "myferdata.csv" ##読み込むcsvファイルの名前
input_image_size = [40,40] ## 入力画像サイズ
output_label_dim = 10 ## 表情の種類

gpu_use = True ## gpuを使うならTrue

if gpu_use == True:
	np = cuda.cupy
	gpu_device = 0
	cuda.get_device(gpu_device).use()
else:
	np = numpy

#----------------------------------------------------

## CNNモデル
class ClassificationModel(chainer.Chain):
    def __init__(self):
        super(ClassificationModel, self).__init__()
	with self.init_scope():

		self.conv1 = L.Convolution2D(1,32,7,stride=1,pad=3)
		self.conv2 = L.Convolution2D(32,32,7,stride=1,pad=3)
		self.conv3 = L.Convolution2D(32,32,3,stride=1,pad=1)
		self.conv4 = L.Convolution2D(32,32,3,stride=1,pad=1)

		self.fc1 = L.Linear(None, 32)
		self.fc2 = L.Linear(32, 32)
		self.fc3 = L.Linear(32, output_label_dim)

		self.bnorm0 = L.BatchNormalization(1)
		self.bnorm1 = L.BatchNormalization(32)
		self.bnorm2 = L.BatchNormalization(32)
		self.bnorm3 = L.BatchNormalization(32)
		self.bnorm4 = L.BatchNormalization(32)
		self.bnorm5 = L.BatchNormalization(32)


		self.optimizer = chainer.optimizers.MomentumSGD(lr=0.004, momentum=0.9)
		self.optimizer.setup(self)
		#self.optimizer.add_hook(chainer.optimizer.WeightDecay(0.0001))

    def __call__(self, x):
	h = x
	h = self.bnorm0(h)
	h = F.leaky_relu(F.max_pooling_2d(self.bnorm1(self.conv1(h)), 2, stride=2,pad=0))
	h = F.leaky_relu(F.max_pooling_2d(self.bnorm2(self.conv2(h)), 2, stride=2,pad=0))

	h = F.leaky_relu(self.bnorm3(self.conv3(h)))
	h = F.leaky_relu(self.bnorm4(self.conv4(h)))

	h = F.leaky_relu(self.fc1(h))
	h = F.leaky_relu(self.fc2(h))

	h = self.fc3(self.bnorm5(h))
	h = F.softmax(h)

	return h

    def train(self, image_datas, label_datas):
	x = image_datas
	t = label_datas

	self.cleargrads()
        h = self(x)

        error = F.mean_squared_error(h, t)  ## 結果と教師データとの２乗誤差
        error.backward()
        self.optimizer.update()

	#print t.data[0]
	#print h.data[0]
	#print "\n"

	return float(error.data) ## 誤差を返す

    def identification(self, image_datas): ## 識別する
	x = image_datas

	with chainer.using_config('train', False): ## ドロップアウトを使用しない
	        h = self(x)

	self.cleargrads()

	return h.data ## 識別結果（出力）を返す


## opencvからchainer用に画像データをソート
## opencv  : [hight][wide][bgr]
## chainer : [bgr][hight][wide]
def cv_ch_sort(image):
	image = numpy.float64(image)/255.0
	#c1,c2,c3 = cv2.split(image)
	#image2 = []
	#image2.append(c1)
	#image2.append(c2)
	#image2.append(c3)
	return image

## 画像名リストから画像を読み込む -> [image1,image2,,,]
def readImages(image_names):
	images = []
	for image_name in image_names:
		image = cv_ch_sort(cv2.imread(image_name,1))
		images.append(image)
	return images

## CNNを学習する
def train_cnn(cnn, EPOCH_NUM = 10, BATCH_NUM = 10):

	## 画像,ラベルを取得(仮) : Csvファイルから読み取るように変更してください
	#csv_datas = 	[	['image/1.bmp', 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
	#			['image/2.bmp', 0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
	#			['image/3.bmp', 0, 0, 10, 0, 0, 0, 0, 0, 0, 0],
	#			['image/4.bmp', 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
	#			['image/5.bmp', 0, 0, 0, 0, 10, 0, 0, 0, 0, 0],
	#			['image/6.bmp', 0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
	#			['image/7.bmp', 0, 0, 0, 0, 0, 0, 10, 0, 0, 0],
	#			['image/8.bmp', 0, 0, 0, 0, 0, 0, 0, 10, 0, 0],
	#			['image/9.bmp', 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
	#			['image/0.bmp', 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
	#		]
	csv_datas = pd.read_csv(csvfile,delimiter=',').values.tolist()


	## 画像データ，ラベルデータを用意
	train_image_datas = []
	train_label_datas = []
	size = (input_image_size[0], input_image_size[1])
	for i in range(len(csv_datas)):
		image = cv2.resize(cv2.imread(csv_datas[i][0], 0), size)
		train_image_datas.append(cv_ch_sort(image))
		label_data = csv_datas[i][1:]
		train_label_datas.append([float(j)/10 for j in label_data])

	## ミニバッチ学習
	error = 0
	BATCH_SIZE = len(csv_datas) / BATCH_NUM

	for epoch in range(EPOCH_NUM):
		index = list(zip(train_image_datas, train_label_datas))
		random.shuffle(index)
		image_datas, label_datas = zip(*index) ## データをシャッフル

		for batch in range(BATCH_NUM):
			## ミニバッチデータを準備
			batch_iamge_datas = list(image_datas[BATCH_SIZE * batch : BATCH_SIZE * (batch + 1)])
			batch_label_datas = list(label_datas[BATCH_SIZE * batch : BATCH_SIZE * (batch + 1)])

			## chainer用に変換
			batch_iamge_datas = np.array(batch_iamge_datas, dtype=np.float32).reshape(-1,1,input_image_size[0],input_image_size[1])
			batch_label_datas = np.array(batch_label_datas, dtype=np.float32).reshape(-1,output_label_dim)

			if gpu_use == True:
				batch_iamge_datas = cuda.to_gpu(batch_iamge_datas, device = 0)
				batch_label_datas = cuda.to_gpu(batch_label_datas, device = 0)

			batch_iamge_datas = chainer.Variable(batch_iamge_datas)
			batch_label_datas = chainer.Variable(batch_label_datas)

			## 学習させる
			error = cnn.train(batch_iamge_datas, batch_label_datas)

		error = error / BATCH_NUM

		print "epoch={}, ".format(epoch),
		print "error={}".format(error)


## CNNで識別する
def identification_cnn(cnn):

	## (仮)
	image_data_names = [	'image/0.png',
				'image/1.png',
				'image/2.png',
				'image/3.png',
				'image/4.png',
				'image/5.png',
				'image/6.png',
				'image/7.png',
				'image/8.png',
				'image/9.png'	]


	## 画像データを取得（仮） : 集合写真と顔の位置情報から取得できるように修正してください
	image_datas = []
	for i in range(len(image_data_names)):
		image = cv2.imread(image_data_names[i], 1)
		image_datas.append(image)


	## 画像をリサイズ
	identification_image_datas = []
	size = (input_image_size[0], input_image_size[1])
	for i in range(len(image_datas)):
		image = cv2.resize(image_datas[i], size)
		identification_image_datas.append(cv_ch_sort(image))

	## chainer用に変換
	identification_image_datas = np.array(identification_image_datas, dtype=np.float32).reshape(-1,3,input_image_size[0],input_image_size[1])
	if gpu_use == True:
		identification_image_datas = cuda.to_gpu(identification_image_datas, device = 0)
	identification_image_datas = chainer.Variable(identification_image_datas)

	## 識別する
	identification_output = cnn.identification(identification_image_datas)

	print identification_output


# main -------------------------------------------------
def main():
	cnn = ClassificationModel()
	#chainer.serializers.load_npz("cnn.npz", cnn) ## 学習済みモデルを読み込む

	if gpu_use == True:
		cnn.to_gpu(gpu_device)

	train_cnn(cnn, EPOCH_NUM = 100, BATCH_NUM = 100)
	chainer.serializers.save_npz("cnn.npz", cnn) ## 学習したモデルを保存する

	#identification_cnn(cnn)

if __name__ == "__main__":
    main()
