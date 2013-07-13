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
import cProfile


eventManager = global_vars.eventManager
_fps = 0.05
_terrainImg = pygame.image.load('dirt.bmp')
_tankImg = pygame.image.load('tanksprites.bmp')
_soldatImg = pygame.image.load('soldatsprite.bmp')
_numTanks = ('Tank', 'Tank', 'Tank', 'Soldat', 'Soldat')
_tankDimensions = _tankImg.get_rect()  #pygame.Rect(0, 0, 37, 27)
_soldatDimensions = _soldatImg.get_rect()
fpsClock = pygame.time.Clock()
_turnTime = 5
background = global_vars.background    #background = _backImg
window = global_vars.window     #window = pygame.display.set_mode((background.get_rect().width, background.get_rect().height))
print background.get_rect().width, background.get_rect().height
pygame.display.set_caption('TANKS')
global_vars.layerManager.newSprite(background, background.get_rect())
terrainModel = terrain.Terrain(background.get_rect(), background.get_rect().height // 2)
global_vars.layerManager.newTerrain(_terrainImg, terrainModel)
oldTime = 0
turn = 0

    


def init():
    ''' Initializes tanks, first function called '''

    for i in range(len(_numTanks)): 
        if _numTanks[i] == 'Tank':
            newTank = tank.Tank(_tankImg, pygame.Rect(50 + i * 50 + i * _tankDimensions.width, 
                terrainModel.maxHeight - _tankDimensions.height, _tankDimensions.width, _tankDimensions.height), terrainModel)
        elif _numTanks[i] == 'Soldat':
            newTank = tank.Soldat(_soldatImg, pygame.Rect(50 + i * 50 + i * _soldatDimensions.width, 
                terrainModel.maxHeight - _soldatDimensions.height, _soldatDimensions.width, _soldatDimensions.height), terrainModel)
        newTank.id = i
        global_vars.layerManager.newSprite(newTank)
    for i in range(50): 
        eventManager.post(events.Event(type = 'tick'))
    play()


def tick():
    '''calls functions that must be called once every frame'''

    eventManager.post(events.Event(type = 'tick'))
    eventManager.post(events.Event(type = 'rtick'))


def play():
    ''' Main game loop '''
    
    global oldTime
    global turn
    paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                if event.key == K_p:
                    paused ^= True
                if event.key == K_r:
                    global_vars.eventManager.post(events.Event(type='draw terrain'))
                if event.key == K_t:
                    global_vars.eventManager.post(events.Event(type='render tanks'))
                if event.key == K_RIGHT:
                    global_vars.eventManager.post(events.Event(type='right'))
                if event.key == K_LEFT:
                    global_vars.eventManager.post(events.Event(type='left'))
                
                    
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                e = events.Event(type = 'click', x = mousex, y = mousey)
                eventManager.post(e)
                e = events.Event(type = 'turn', t = turn)            
                turn += 1
                #print 'TURNCHANGE', turn
                if turn == len(_numTanks): turn = 0
                oldTime = time.time()
                eventManager.post(e)

        if time.time() - oldTime > _fps:

            '''
            e = events.Event(type = 'turn', t = turn)
            turn += 1
           # print 'TURNCHANGE', turn
            if turn == _numTanks: turn = 0
            
            oldTime = time.time()
            eventManager.post(e)
            '''
            pygame.display.update()
            oldTime = time.time()
        else:
            while time.time() - oldTime < _fps:
                pass
        
        
        if not paused: 
            tick()


        #fpsClock.tick(_fps)

cProfile.run("init()")
        
init()
        