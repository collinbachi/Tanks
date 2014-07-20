'''
Created on Jan 19, 2013

This is the main game engine. It will handle the initialization of
pygame and the top level running of the game.

@author: Collin
'''
import pygame, sys, tank, terrain, global_vars
from pygame.locals import *
import time
import events
import controller
import hud
#import cProfile


eventManager = global_vars.eventManager
_fps = 0.05
_terrainImg = pygame.image.load('dirt.bmp')
_tankImg = pygame.image.load('tankorig.bmp')
_soldatImg = pygame.image.load('soldatsprite.bmp')
_numTanks = ('Tank', 'Tank', 'Tank', 'Soldat', 'Soldat')
_tankDimensions = _tankImg.get_rect()
_soldatDimensions = _soldatImg.get_rect()
fpsClock = pygame.time.Clock()
_turnTime = 5
background = global_vars.background
window = global_vars.window
pygame.display.set_caption('TANKS')
global_vars.layerManager.newSprite(background, background.get_rect())
terrainModel = terrain.Terrain(background.get_rect(), background.get_rect().height // 2)
global_vars.layerManager.newTerrain(_terrainImg, terrainModel)
oldTime = 0
turn = 0
global_vars.idLookup = [0] * len(_numTanks)
ctr = None

def init():
    ''' Initializes tanks, first function called '''

    for i in range(len(_numTanks)): 
        if _numTanks[i] == 'Tank':
            newTank = tank.Tank(_tankImg, pygame.Rect(50 + i * 50 + i * _tankDimensions.width, 
                terrainModel.maxHeight - _tankDimensions.height, _tankDimensions.width, _tankDimensions.height), terrainModel)
        elif _numTanks[i] == 'Soldat':
            newTank = tank.Soldat(_soldatImg, pygame.Rect(50 + i * 50 + i * (_soldatDimensions.width + 25), 
                terrainModel.maxHeight - _soldatDimensions.height, _soldatDimensions.width, _soldatDimensions.height), terrainModel)
        newTank.id = i
        global_vars.idLookup[i] = newTank
        global_vars.layerManager.newSprite(newTank)
    for i in range(50): 
        eventManager.post(events.Event(type = 'tick'))
    global ctr
    ctr = controller.Controller(turn)
    turnText = hud.TurnText('1', (50, 50))
    play()


def tick():
    ''' Calls functions that must be called once every frame '''

    eventManager.post(events.Event(type = 'tick'))


def play():
    '''
     Main game loop

     Accepts user input and posts relevant events, handles pause state, ticks engine, etc. 
     '''
    
    global oldTime
    global turn
    paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                if event.key == K_p:
                    paused ^= True
                if event.key == K_r:
                    global_vars.eventManager.post(events.Event(type='draw terrain'))
                if event.key == K_t:
                    global_vars.eventManager.post(events.Event(type='render tanks'))
                if event.key == K_RIGHT or event.key == K_d:
                    global_vars.eventManager.post(events.Event(type='right down'))
                if event.key == K_LEFT or event.key == K_a:
                    global_vars.eventManager.post(events.Event(type='left down'))
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    global_vars.eventManager.post(events.Event(type='right up'))
                if event.key == K_LEFT or event.key == K_a:
                    global_vars.eventManager.post(events.Event(type='left up'))
                
                    
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                e = events.Event(type = 'click', x = mousex, y = mousey)
                eventManager.post(e)
                turn = ctr.changeTurn()
                oldTime = time.time()

        if time.time() - oldTime > _fps:
            pygame.display.update()
            oldTime = time.time()
        else:
            while time.time() - oldTime < _fps:
                pass
        
        if not paused: 
            tick()

        
init()