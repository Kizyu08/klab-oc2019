# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import codecs
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import datetime
import random

sys.path.append('../face')
import face
import faces
import IScene
import Util
import Window
import SceneEventID
import FaceDetectionDummy
import EmotionImages


class PlayGame(IScene.IScene):
    # コンストラクタ
    def __init__(self, window):
        # スーパークラスのコンストラクタを呼び出す
        super(PrototypeScene, self).__init__(window)    
        
        # メンバ変数を一通り初期化

