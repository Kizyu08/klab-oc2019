# -*- coding: utf-8 -*-

import sys

sys.path.append('../face')
import face

def computeFaceScoresDummy(faces):
    maxSizeFace = face.Face()
    emotionNames = maxSizeFace.result().keys()


    (x, y), (w, h) = maxSizeFace.rect()
    for aface in faces:
        (cx, cy), (cw, ch) = aface.rect()
        if cw > w:
            w = cw
    for aface in faces:
        (x, y), (w, h) = aface.rect()
        cnt = 0
        pos = int(w / 25) % len(emotionNames)
        emotionScores = aface.result()
        for emotionName in emotionScores.keys():
            if cnt == pos:
                emotionScores[emotionName] = 1.0
            else:
                emotionScores[emotionName] = 0
            cnt += 1
    return faces
