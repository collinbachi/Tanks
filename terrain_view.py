'''
Created on Jun 4, 2013

Handles the rendering of the terrain.

@author: Collin
'''

import global_vars
import layers
import pygame
import events
import time

class TerrainView(layers.Layer, events.EventUser):
    ''' Handles the rendering of the terrain '''
    
    def __init__(self, image, terrain):
        self.terrain = terrain
        self.image = image
        self.eventManager = global_vars.eventManager
        self.eventManager.subscribe(self, 'draw terrain')
        self.eventManager.subscribe(self, 'impact')
        layers.Layer.__init__(self, image)
        
    def processEvent(self, e):
        if e.type == 'draw terrain':
            self.drawTerrain(True)
        elif e.type == 'impact':
            self.drawTerrain()
        
    def getPixel(self, x, y, returnsToManager=False):
        try:
            if self.terrain.ter[y][x] == 0 and returnsToManager == False:
                return global_vars.layerManager.getPixel(x, y)
            elif self.terrain.ter[y][x] == 0 and returnsToManager == True:
                return pygame.Color('white')
            elif self.terrain.ter[y][x] == 1:
                return self.image.get_at((x, y))
        except:
            if returnsToManager:
                return pygame.Color('white')
            else: return global_vars.layerManager.getPixel(x, y)
    
    def render(self):
        self.drawTerrain(True)
        
    def drawTerrain(self, fullRedraw=False):
        ''' Draws terrain from info in terrain class '''

        if self.terrain.changed == False and fullRedraw == False: return
        
        pix = pygame.PixelArray(self.image.copy())
        if isinstance(self.terrain.changed, pygame.Rect) and fullRedraw == False:
            lowx = self.terrain.changed.left
            highx=self.terrain.changed.right
            lowy = self.terrain.changed.top
            highy = self.terrain.changed.bottom
            print 'REDRAW'
        else:
            lowx = 0
            highx=len(self.terrain.ter[0])
            lowy = 0
            highy = len(self.terrain.ter)
            print 'FULL REDRAW'
        
        startTime = time.time()
        for i in range(lowy, highy):
            for j in range(lowx, highx):
                if i < 0 or j < 0: 
                    print 'negatives'
                    return False
                if self.terrain.ter[i][j] == 0: pix[j][i] = global_vars.background.get_at((j, i))
                #SHOULD USE IMPLEMENTATION BELOW, but too slow. IDK what to do
                #pix[j][i] = global_vars.layerManager.getPixel(j, i)
                
                    
        print 'Redraw Time: ', time.time() - startTime
        
        pix = pix[lowx:highx, lowy:highy]
                    
        news = pix.make_surface()
        del pix
        global_vars.window.blit(news, pygame.Rect(lowx, lowy, highx - lowx, highy - lowy))   #global_vars.background.get_rect())
        self.terrain.changed = False
        global_vars.eventManager.post(events.Event(type='render tanks'))
                
                