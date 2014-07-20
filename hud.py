'''
Created on May 15, 2014

Module containing classes for the heads up display.

@author: Collin
'''
import pygame
import global_vars
pygame.font.init()

class Text:
	''' Generic text display '''

	def __init__(self, txt, pos, size=32):
		self.text = pygame.font.Font(None, size)
		self.pos = pos
		surf = self.text.render(txt, False, pygame.Color('black'), (0, 110, 0))
		surf = pygame.Surface.convert(surf)
		self.sprite = global_vars.layerManager.newSprite(surf, surf.get_rect())
		self.sprite.move(self.pos[0], self.pos[1])

	def update(self, txt):
		surf = self.text.render(txt, False, pygame.Color('black'), pygame.Color('white'))
		surf = pygame.Surface.convert(surf)
		'''surf.set_colorkey(pygame.Color('white'))
		global_vars.window.blit(surf, self.pos)
		return'''
		global_vars.layerManager.killSprite(self.sprite)
		self.sprite = global_vars.layerManager.newSprite(surf, surf.get_rect())
		self.sprite.TEXT_TEST = True
		self.sprite.move(self.pos[0], self.pos[1])

class TurnText(Text):
	''' Displays the turn number '''

	def __init__(self, txt, pos, size=32):
		global_vars.eventManager.subscribe(self, 'turn')
		Text.__init__(self, txt, pos, size)

	def processEvent(self, e):
		self.update('' + str(e.t + 1))

