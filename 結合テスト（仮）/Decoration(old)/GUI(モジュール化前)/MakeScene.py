# -*- coding: utf-8 -*-
import IScene
import Scene
import Window

def makeScene(sceneID, window):
    if sceneID == IScene.SceneID.MAIN:
        return Scene.Scene(window)
    else:
        return IScene.NoneScene(window)