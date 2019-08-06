# -*- coding: utf-8 -*-

class SceneID:
    NONE                = 0
    START_SCENE         = 1
    PROTOTYPE_SCENE     = 2
    PLAY_GAME_SCENE     = 3

class IScene(object):
    def __init__(self, window):
        self.__window = window
        self.__sceneID = SceneID.NONE
    
    def draw(self):
        return False
    
    def update(self):
        return False

    def isExit(self):
        return True

    def isRunning(self):
        return not self.isExit()

    def getNextSceneID(self):
        #return SceneID.NONE
        return SceneID.NONE

class NoneScene(IScene):
    def __init__(self, window):
        super(NoneScene, self).__init__(window)



# タイマークラス作成中
import time

class Timer:
    def __init__(self):
        self.__state        = Timer.State(State.stoping)    # タイマーの状態を設定する
        self.__lastTime     = time.time()                   # 経過時間の計算の基準とする時刻を設定する  
        self.__elapsedTime  = 0.0                           # 経過時間を設定する
    
    # 現在の経過時間を取得する
    def getElapsedTimeMilli(self):
        # タイマーが動いている場合は経過時間を更新してから経過時間を返す
        if self.__state.isRunning():
            ''' '''
        # タイマーが止まっている場合は経過時間をそのまま帰す
        elif self.__state.isStoping():
            return __elapsedTime

    # タイマーをスタートする
    def start(self):
        if self.__state.isRunning():
            return
        self.__state.start()
        self.__lastTime = time.time()
    
    # タイマーを再開する
    def restart(self):
        # 既にタイマーが動いている場合は何もしない
        if self.__state.isRunning():
            return
        # タイマーが止まっているならば再開させる
        elif self.__state.isStoping():
            self.__state.running()

    # タイマーを止める
    def stop(self):
        self.__state.stoping()

    # タイマーのカウントを初期化する
    def reset(self):
        ''' '''

    class State:
        stoping = 0
        running  = 1
        def __init__(self, state = stoping):
            self.__state = state
        def start(self):
            self.__state = running
        def stop(self):
            self.__state = stoping
        def get():
            return self.__state()
        def isStoping(self):
            return self.__state == stoping
        def isRunning(self):
            return self.__state == running



