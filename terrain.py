'''
Created on Jan 19, 2013

Models the destructible terrain

@author: Collin
'''
import pygame, random
import math
import global_vars
import events

class Terrain:
    ''' models the destructible terrain '''

    def __init__(self, r, h, s=25):

        self.rect = r
        self.maxHeight = h
        self.smoothFactor = s
        self.ter = self.generateTerrain()
        self.changed = True
        
    def checkCollide(self, rect):
        ''' accepts a rectangle, checks if any point inside contains land '''

        try:
            for x in range(rect.left, rect.left + rect.width):
                for y in range(rect.top, rect.top + rect.height):
                    if y < 0 or x < 0: 
                        return True
                    if (self.ter[y][x] == 1):
                        return True
            return False
        except IndexError:
            return False
    
    def checkBullet(self, b):
        '''
        Checks if a bullet is colliding with land. If so, it designates a 
        rectangle around the collision point based on the bullet's blast
        radius to be rerendered by the next frame
        '''

        try:
            if b.y < 0 or b.x < 0: 
                lowy = b.y - b.blast - 1
                highy = b.y + b.blast + 1
                lowx = b.x - b.blast - 1
                highx = b.x + b.blast + 1
                if lowy < 0: lowy = 0
                if lowx < 0: lowx = 0
                if highy >= len(self.ter): highy = len(self.ter) 
                if highx >= len(self.ter[0]): highx = len(self.ter[0]) 
                if highy < lowy: highy = lowy + b.blast
                if highx < lowx: highx = lowx + b.blast
                self.changed = pygame.Rect(lowx, lowy, highx - lowx, highy - lowy)
                global_vars.eventManager.post(events.Event(type='impact', rect = self.changed))
                return True
            if self.ter[b.y][b.x] == 1:
                #Collision!
                lowy = b.y - b.blast - 1
                highy = b.y + b.blast + 1
                lowx = b.x - b.blast - 1
                highx = b.x + b.blast + 1
                if lowy < 0: lowy = 0
                if lowx < 0: lowx = 0
                if highy >= len(self.ter): highy = len(self.ter) 
                if highx >= len(self.ter[0]): highx = len(self.ter[0]) 
                
                for i in range(lowy, highy):
                    for j in range(lowx, highx):
                        if math.sqrt(math.pow(i - b.y, 2) + math.pow(j - b.x, 2)) < b.blast: 
                            self.ter[i][j] = 0

                self.changed = pygame.Rect(lowx, lowy, highx - lowx, highy - lowy)
                global_vars.eventManager.post(events.Event(type='impact', rect = self.changed))
                return True
        except IndexError: # Shouldn't happen?
            return True
        
    def generateTerrain(self):
        ''' 
        Generates terrain by assigning each column of pixels a random height, 
        and then repeatedly averaging with neighbors to smooth the terrain.
        '''
        
        heights = [random.choice(range(1, self.maxHeight)) for p in range(self.rect.width)]
        for i in range(len(heights)): heights[i] += round(math.sin(6 * 3.14 /len(heights) * i) * 30)
        
        #smoothes terrain
        for i in range(self.smoothFactor):
            for n in range(2, len(heights) - 1):
                heights[n] = sum(heights[n - 2: n + 3]) / 5 
        heights[0] = sum(heights[0:5]) / 5
        heights[1] = sum(heights[0:5]) / 5
        heights[len(heights) - 1] = sum(heights[len(heights) - 5: len(heights)]) / 5
        
        
        pixArray = [[0 for n in range(self.rect.width)] for i in range(self.rect.height)]
        
        for n in range(self.rect.height):
            for j in range(self.rect.width):
                if self.rect.height - n < heights[j]:
                    pixArray[n][j] = 1
                else: pixArray[n][j] = 0
                
        return pixArray
