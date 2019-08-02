# -*- coding: utf-8 -*-
import IScene
import PrototypeScene
import Window

def makeScene(sceneID, window):
    nextScene = None

    if sceneID == IScene.SceneID.PROTOTYPE_SCENE:
        nextScene = PrototypeScene.PrototypeScene(window)

    elif sceneID == IScene.SceneID.PLAY_GAME_SCENE:
        print("未実装のシーンです")
        nextScene = IScene.NoneScene(window)

    elif sceneID == IScene.SceneID.START_SCENE:
        print("未実装のシーンです")
        nextScene = IScene.NoneScene(window)
        
    else:
        print("存在しないシーンのIDが渡されました")
        nextScene = IScene.NoneScene(window)

    return nextScene