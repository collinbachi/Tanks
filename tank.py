'''
Created on Jan 19, 2013

Represents a player or cpu's tank.
Bullet class also included.

@author: Collin
'''
import events
import global_vars
import layermanager
import pygame

class Tank(events.EventUser, layermanager.Sprite):
    _gravity = 2
    _speed = 1
    _firePower = 15
    
    
    
    def __init__(self, image, rect, le):

        layermanager.Sprite.__init__(self, image, rect)
        self.eventManager = global_vars.eventManager
        self.eventManager.subscribe(self, 'tick')
        self.eventManager.subscribe(self, 'click')
        self.eventManager.subscribe(self, 'turn')
        self.eventManager.subscribe(self, 'render tanks')
        self.eventManager.subscribe(self, 'left')
        self.eventManager.subscribe(self, 'right')
        
        self.myRect = rect.copy()
        self.level = le
        self._eventMap = {'tick':    self.tick,
                          'render tanks': self.render,
                          'draw terrain': self.render}
        
        self.isTurn = False
        self.isMovingRight = False
        self.isMovingLeft = False
        self.turn = 0
        self.lastBullet = 0
        self.canFire = True
        
    def tick(self):
        self.fall()
        if not self.isTurn: self.isMovingLeft, self.isMovingRight = False, False
        if self.isMovingLeft:
            self.latMove(-self._speed)
        elif self.isMovingRight:
            self.latMove(self._speed)
        
        if self.myRect.top > 1000: self.kill()

    def fall(self):
        self.myRect.top += self._gravity
        while self.checkCollide(self.myRect): self.myRect.top -= 1
        self.move(self.myRect.left, self.myRect.top)
        
    def checkCollide(self, rect):
        return self.level.checkCollide(rect)
    
    def fire(self, x, y):
        if not self.canFire: return
        xmov = ((x - self.myRect.centerx) / self._firePower)
        ymov = ((y - self.myRect.centery) / self._firePower)
        b = Bullet(self.myRect.centerx, self.myRect.centery, xmov, ymov, self._gravity / 2, 20, self)
        self.lastBullet = b
        self.canFire = False
        return b

    def latMove(self, delta):
        newRect = self.myRect.copy()
        newRect.left += delta
        for jump in range(20):
            if not self.checkCollide(newRect):
                #print 'AYYYYYY'
                self.myRect = newRect
                return
            else:
                #print 'ohhh'
                newRect.top -= 1
    
    def processEvent(self, e):
        if e.type == 'click' and self.isTurn:
            self.fire(e.x, e.y)
        elif e.type == 'turn':
            self.turn = e.t
            self.isTurn = self.turn == self.id
            self.canFire = True
        elif e.type == 'left' and self.isTurn:
            self.isMovingLeft ^= True
            self.isMovingRight = False
        elif e.type == 'right' and self.isTurn:
            self.isMovingRight ^= True
            self.isMovingLeft = False
        else: events.EventUser.processEvent(self, e)
        
    #Returns last bullet, needs to be replaced when new view is created
    def getRecentBullet(self): 
        return self.lastBullet

class Soldat(Tank):
    ''' Variation of Tank '''

    def __init__(self, image, rect, le):
        Tank.__init__(self, image, rect, le)
        self._gravity = 2
        self._speed = 5
        self._firePower = 10

    def fire(self, x, y):
        if not self.canFire: return
        xmov = (x - self.myRect.centerx) / self._firePower
        ymov = (y - self.myRect.centery) / self._firePower
        b = Bullet(self.myRect.centerx, self.myRect.centery, xmov, ymov, 1, 5, self)
        self.lastBullet = b
        self.canFire = False
        return b

        
        
        
class Bullet(events.EventUser, layermanager.Sprite):
    def __init__(self, x, y, xm, ym, gm, xp, t):
        self._radius = 2

        mySurface = pygame.Surface((self._radius * 2, self._radius * 2))
        mySurface.fill(pygame.Color('white'))
        pygame.draw.circle(mySurface, pygame.Color('black'), (self._radius, self._radius), self._radius)
        pygame.draw.circle
        layermanager.Sprite.__init__(self, mySurface, pygame.Rect((x - self._radius, y - self._radius), (self._radius * 2, self._radius * 2)))
        
        
        self.eventManager = global_vars.eventManager
        self.eventManager.subscribe(self, 'tick')
        
        self.x = x
        self.y = y
        self.xmov = xm
        self.ymov = ym
        self.g = gm
        self.fakeTime = 0
        self.tank = t
        self.blast = xp
        self.alive = True
        self._eventMap = {'tick': self.tick}
    def tick(self):

        if not self.alive: 
            self.eventManager.unsubscribe(self)            
            print '<><><><><><><><><><><>'
            del self.tank.lastBullet
            return
        
        self.fakeTime += 1
        self.x += self.xmov
        self.ymov += self.g
        if self.ymov > 10: self.ymov = 10
        self.y += self.ymov
        
        self.move(self.x, self.y)
        
        #if self.xmov > 1: self.xmov = 1
        #if self.ymov > 1: self.ymov = 1
        collision = self.tank.level.checkBullet(self)
        if collision: 
            self.alive = False
            #print collision, '!!!!!!!!!!!', self.alive
        if self.fakeTime > 150: self.alive = False
        if not self.alive: 
            #print '109 BULLET LINE'
            self.eventManager.unsubscribe(self)
        if self.x > 1000 or self.x < -1000 or self.y > 1000 or self.y < -1000: self.kill()