# -*- coding: utf-8 -*-

# シーンのイベントID
class SceneEventID:
    NON = 0                 # 検出イベントなし
    COMPUTE_SCORES  = 1     # スコアの計算
    SAVE_IMAGE      = 2     # 画像の保存
    EXIT_SCENE      = 3     # シーンの終了

    # コンストラクタ
    def __init__(self):
        self.__id = SceneEventID.NON

    # イベントがない状態か
    def isNon(self):
        return self.__id == SceneEventID.NON

    # スコアの計算を行う状態か
    def isComputeScores(self):
        return self.__id == SceneEventID.COMPUTE_SCORES
        
    # シーンを終了する状態か
    def isExitScene(self):
        return self.__id == SceneEventID.EXIT_SCENE

    # 画像を保存する状態か
    def isSaveImage(self):
        return self.__id == SceneEventID.SAVE_IMAGE

    def isNotNon(self):
        return self.__id != SceneEventID.NON

    def isNotComputeScores(self):
        return self.__id != SceneEventID.COMPUTE_SCORES
        
    def isNotExitScene(self):
        return self.__id != SceneEventID.EXIT_SCENE

    def isNotSaveImage(self):
        return self.__id != SceneEventID.SAVE_IMAGE
    
    def set(self, sceneEventID):
        self.__id = sceneEventID

    def get(self):
        return self.__id
