# -*- coding: utf-8 -*-
import pygame

WINDOW_CAPTION    = u"non title"
WINDOW_WIDTH      = 640
WINDOW_HEIGHT     = 480
WINDOW_FONT_NAME  = u"notosansmonocjkjp"
WINDOW_FONT_SIZE  = 16
WINDOW_BGCOLOR    = (0, 0, 0)
WINDOW_FONT_COLOR = [255, 255, 255]

class Window:
	# コンストラクタ
	def __init__(
			self, 
			width = WINDOW_WIDTH, 
			height = WINDOW_HEIGHT, 
		):
		pygame.init()
		pygame.display.set_caption(u"OP2019")
		self.__windowCaption= WINDOW_CAPTION
		self.__width		= width
		self.__height		= height
		self.__screen 		= pygame.display.set_mode( (self.__width, self.__height) )
		self.__fontName 	= WINDOW_FONT_NAME
		self.__fontSize 	= WINDOW_FONT_SIZE
		self.__font 		= pygame.font.SysFont(self.__fontName, self.__fontSize)
		self.__fontColor	= WINDOW_FONT_COLOR
		self.__bgcolor 		= WINDOW_BGCOLOR
		#print(u"フォント：" + self.__fontName + u", 文字サイズ：" + str(self.__fontSize))

	# ウィンドウのキャプションを設定する 
	def setWindowCaption(self, windowCaption):
		uWindowCaption = windowCaption.encode('unicode-escape')
		self.__windowCaption = uWindowCaption
		pygame.display.set_caption(self.__windowCaption)
	

	# ウィンドウサイズを変更する 
	def changeWindowSize(self, width, height):
		self.__width	= width
		self.__height	= height
		self.__screen = pygame.display.set_mode( (self.__width, self.__height) )
	

	# フォントを設定する
	def setFont(self, fontName, fontSize = WINDOW_FONT_SIZE, fontColor = WINDOW_FONT_COLOR):
		self.__fontName  = fontName
		self.__fontSize  = fontSize
		self.__fontColor = fontColor
		self.__font 	 = pygame.font.SysFont(self.__fontName, self.__fontSize)

	# フォントサイズを設定する
	def setFontSize(self, fontSize):
		self.__fontSize  = fontSize
		self.__font 	 = pygame.font.SysFont(self.__fontName, self.__fontSize)

		

	# 画面更新時処理等の画面を塗りつぶす時の色を設定する
	def fill(self, bgcolor):
		self.__screen.fill(bgcolor)
	def fill(self):
		self.__screen.fill(self.__bgcolor)
	

	# バッファへ描画された内容を画面へ出力する
	# reverse が True の場合は左右反転させて出力する
	def flip(self, reverse = False):
		if reverse:
			screenR = pygame.transform.flip(self.__screen, True, False)
			self.drawImg(screenR, 0, 0)
		else:
			pygame.display.flip()
	
	# 現在の描画内容を左右反転させる
	def reverseScreen(self):
		screenR = pygame.transform.flip(self.__screen, True, False)
		self.drawImg(screenR, 0, 0)


	# 文字をウィンドウへ表示する
	def drawText(self, text, x, y, fontColor):
		uText = text.encode('unicode-escape')
		fontObj = self.__font.render(uText, True, fontColor)
		self.__screen.blit(fontObj, [x, y])
	def drawText(self, text, x, y):
		uText = text.encode('unicode-escape')
		fontObj = self.__font.render(uText, True, self.__fontColor)
		self.__screen.blit(fontObj, (x, y))
	

	# 画像をウィンドウへ表示する
	def drawImg(self, img, x, y):
		self.__screen.blit(img,(x, y))
	
	# 矩形を描画する
	# rgb   : 矩形の色(RGB)
	# rec   : 矩形の左上座標と右下座標を表すRect
	# width : 矩形の線の太さ（0の場合は矩形内を塗りつぶす）
	def drawRect(self, rgb = (0, 0, 0,), rect = pygame.Rect(0, 0, 10, 10), width = 0):
		pygame.draw.rect(self.__screen, rgb, rect, width)

	# ウィンドウの描画内容を保存する
	def saveDisp(self, filename):
		pygame.image.save(self.__screen, filename)

	# ウィンドウを閉じる
	def quit(self):
		pygame.quit()
	
	# ウィンドウの幅を取得する
	def getWidth(self):
		return self.__width

	# ウィンドウの高さを取得する
	def getHeight(self):
		return self.__height

	# 描画用のバッファーを取得する
	# あまりよろしくないメソッドなので極力使わないこと
	def getScreen(self):
		return self.__screen
