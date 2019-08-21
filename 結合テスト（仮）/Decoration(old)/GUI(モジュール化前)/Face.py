# -*- coding: utf-8 -*-

class Face:
	def __init__(self):
		self.id    = 0
		self.x     = 0
		self.y     = 0
		self.width = 0
		self.emotionScores = {
				'neutral' : 0.0,
				'angry' : 0.0,
				'happiness' : 0.0,
				'unlucky' : 0.0,
				'sad' : 0.0,
				'grad' : 0.0,
				'pleasant' : 0.0,
				'enjoy' : 0.0,
		}


