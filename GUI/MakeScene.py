# -*- coding: utf-8 -*-
import IScene
import PrototypeScene
import Window

def makeScene(sceneID, window):
    if sceneID == IScene.SceneID.PROTOTYPE_SCENE:
        return PrototypeScene.PrototypeScene(window)
    else:
        return IScene.NoneScene(window)