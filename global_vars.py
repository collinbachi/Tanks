'''
Created on Jan 31, 2013

Contains variables that must be used by multiple modules, especially singletons.

@author: Collin
'''
import events, layermanager, pygame, time

pygame.init()

fps = 25

eventManager = events.EventManager()
layerManager = layermanager.LayerManager();

background = pygame.image.load('cloud65.bmp')
window = pygame.display.set_mode((background.get_rect().width, background.get_rect().height))
idLookup = []
