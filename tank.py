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
import bresenham
import math

class Tank(events.EventUser, layermanager.AnimatedSprite):
    _gravity = 2
    _speed = 1
    _firePower = 15
    
    
    
    def __init__(self, image, rect, le):

        filesDict = {'tankorig.bmp': ['idle0']}
        layermanager.AnimatedSprite.__init__(self, image, rect, filesDict)
        self.init(image, rect, le)
        
    def init(self, image, rect, le):

        self.eventManager = global_vars.eventManager
        self.eventManager.subscribe(self, 'tick')
        self.eventManager.subscribe(self, 'click')
        self.eventManager.subscribe(self, 'turn')
        self.eventManager.subscribe(self, 'render tanks')
        self.eventManager.subscribe(self, 'left down')
        self.eventManager.subscribe(self, 'right down')
        self.eventManager.subscribe(self, 'left up')
        self.eventManager.subscribe(self, 'right up')
        
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
        ''' updates status every frame '''

        self.fall()
        if not self.isTurn: self.isMovingLeft, self.isMovingRight = False, False
        if self.isMovingLeft:
            self.latMove(-self._speed)
        elif self.isMovingRight:
            self.latMove(self._speed)
        
        if self.myRect.top > 550: self.kill()

    def fall(self):
        ''' implements gravity '''

        self.myRect.top += self._gravity
        while self.checkCollide(self.myRect): self.myRect.top -= 1
        self.move(self.myRect.left, self.myRect.top)
        
    def checkCollide(self, rect):

        return self.level.checkCollide(rect)
    
    def fire(self, x, y):
        ''' creates and initializes a bullet at the tank's location '''

        if not self.canFire: return
        xmov = ((x - self.myRect.centerx) / self._firePower)
        ymov = ((y - self.myRect.centery) / self._firePower)
        b = Bullet(self.myRect.centerx, self.myRect.centery, xmov, ymov, self._gravity / 2, 20, self)
        self.lastBullet = b
        self.canFire = False
        return b

    def latMove(self, delta):
        ''' moves the tank laterally '''

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
        ''' calls functions and updates variables based on event posts '''

        if e.type == 'click' and self.isTurn:
            self.fire(e.x, e.y)
        elif e.type == 'turn':
            self.turn = e.t
            self.isTurn = self.turn == self.id
            self.canFire = True
        elif e.type == 'left down' and self.isTurn:
            self.isMovingLeft = True
            self.isMovingRight = False
        elif e.type == 'right down' and self.isTurn:
            self.isMovingRight = True
            self.isMovingLeft = False
        elif e.type == 'left up' and self.isTurn:
            self.isMovingLeft = False
        elif e.type == 'right up' and self.isTurn:
            self.isMovingRight = False
        else: events.EventUser.processEvent(self, e)
        
    def getRecentBullet(self): 
        ''' outdated workaround - no longer used '''

        return self.lastBullet


class Soldat(Tank):
    ''' Variation of Tank '''

    def __init__(self, image, rect, le):

        filesDict = {'soldier_left.bmp': ['left0', 'idle0', 'left1'],
                     'soldier_right.bmp': ['right1', 'idle1', 'right0']}
        layermanager.AnimatedSprite.__init__(self, image, rect, filesDict)
        self.init(image, rect, le)
        self._gravity = 2
        self._speed = 5
        self._firePower = 35
        self.frame = 0

    def fire(self, x, y):
        ''' creates and initializes a bullet '''

        if not self.canFire: return
        dx = x - self.myRect.centerx
        dy = y - self.myRect.centery
        dist = math.hypot(dx, dy)
        xmov = int(round(1.0 * dx / dist * self._firePower))
        ymov = int(round(1.0 * dy / dist * self._firePower))
        b = Bullet(self.myRect.centerx, self.myRect.centery, xmov, ymov, 1, 5, self, 2)
        self.lastBullet = b
        self.canFire = False
        return b

    def tick(self):
        ''' updates every frame '''

        if self.isMovingLeft:
            self.animate('left')
        elif self.isMovingRight:
            self.animate('right')
        Tank.tick(self)

    def processEvent(self, e):
        ''' handles event posts '''

        if e.type == 'left up' and self.isTurn:
            self.set_img('idle0')
        elif e.type == 'right up' and self.isTurn:
            self.set_img('idle1')
        
        Tank.processEvent(self, e)

        
class Bullet(events.EventUser, layermanager.Sprite):
    ''' bullets fired by Tanks and Soldats '''

    def __init__(self, x, y, xm, ym, gm, xp, t, r=4):

        self._radius = r

        mySurface = pygame.Surface((self._radius * 2, self._radius * 2))
        mySurface.fill(pygame.Color('white'))
        pygame.draw.circle(mySurface, pygame.Color('black'), (self._radius, self._radius), self._radius)
        pygame.draw.circle
        layermanager.Sprite.__init__(self, mySurface, 
            pygame.Rect((x - self._radius, y - self._radius), 
                (self._radius * 2, self._radius * 2)))
        #print self.image, self.rect, ' is a bullet'
        global_vars.layerManager.newSprite(self)
        
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
        ''' 
        Updates every frame and moves the bullet. Also checks for collision,
        corrects for collisions that occur in between frames, and removes
        the bullet when it is no longer needed. 
        '''

        if not self.alive: 
            self.eventManager.unsubscribe(self)            
            del self.tank.lastBullet
            return

        self.lastx = self.x
        self.lasty = self.y

        self.fakeTime += 1
        self.x += self.xmov
        self.ymov += self.g
        if self.ymov > 10: self.ymov = 10
        self.y += self.ymov
        
        #Bug 2 Fix with bresenham's line alg
        try:
            for cord in bresenham.line((self.lastx, self.lasty), (self.x, self.y)):
                if self.tank.level.ter[cord[1]][cord[0]] == 1:
                    self.y = cord[1]
                    self.x = cord[0]
                    break
        except: pass

        self.move(self.x, self.y)
        
        collision = self.tank.level.checkBullet(self)
        if collision: 
            self.alive = False
        if self.fakeTime > 150: self.alive = False
        if not self.alive: 
            self.eventManager.unsubscribe(self)
            self.wipe()
        if self.x > 1000 or self.x < -1000 or self.y > 1000 or self.y < -1000: 
            self.eventManager.unsubscribe(self)