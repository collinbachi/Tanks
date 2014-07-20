'''
Created on May 31, 2013

Contains classes related to the view

@author: Collin
'''

import events;
import global_vars;
import pygame;
import layers;
import terrain_view
from operator import attrgetter

class LayerManager(events.EventUser):
    ''' 
    Maintains a reference to all layers. Increments depth. Creates new
    layers. Singleton.
    '''
    
    def __init__(self):

        self.depth = 0;
        self.layersList = []; #will be sorted high to low depth
        
    def getHighestDepth(self):

        self.depth += 1;
        return self.depth;
    
    def getPixel(self, x, y):

        for i in range(len(self.layersList)):
            p = self.layersList[i].getPixel(x, y, True)
            if p != pygame.Color('white'): 
                return p
        return pygame.Color('white')
    
    def newTerrain(self, image, terrain):

        terrainView = terrain_view.TerrainView(image, terrain)
        self.terrainView = terrainView
        #self.layersList.append(terrainView)
        #self.layersList = sorted(self.layersList, key=attrgetter('depth'), reverse=True)
        return terrainView
    
    def newSprite(self, image, rect=None):

        if not isinstance(image, Sprite):
            sprite = Sprite(image, rect)
        else: 
            sprite = image
        self.layersList.append(sprite)
        self.layersList = sorted(self.layersList, key=attrgetter('depth'), reverse=True)
        return sprite

    def killSprite(self, sprite):
        #return
        #sprite.move(1000, 1000)
        self.layersList.remove(sprite)
        global_vars.eventManager.unsubscribe(sprite)
        #del sprite
        
    
    
class Sprite(events.EventUser, layers.Layer):
    '''
    The basic moveable container for an animated object. Will handle
    rendering. Will be a parent class for characters, enemies, etc.
    Probably will handle animation. Should inherit from Layer.
    '''
    
    def __init__(self, image, rect):

        if isinstance(image, pygame.Surface): self.image = image
        elif image is None: pass
        else: self.image = pygame.image.load(image)
        self.rect = rect
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        self.myPixels = pygame.PixelArray(self.image.copy())
        self.image.set_colorkey(pygame.Color('white'))
        layers.Layer.__init__(self, self)
        
    def getPixel(self, x, y, returnsToManager=False):
        ''' 
        Returns the color of a pixel at the given (x, y) location. If
        this pixel is white, it recursively searches down layers until
        it finds the highest non-white pixel. Works with render. 
        '''
        
        if self.rect.collidepoint(x, y):
                p = self.image.get_at((x - self.rect.left, y - self.rect.top))
        else:
            if returnsToManager: return pygame.Color('white')
            else: return global_vars.layerManager.getPixel(x, y)
        
        if p != pygame.Color('white'):
            return p
        elif returnsToManager: return pygame.Color('white')
        else:
            #try: 
            #    if self.TEXT_TEST: print p, global_vars.layerManager.getPixel(x, y)
            #except: pass
            return global_vars.layerManager.getPixel(x, y)
    
    def render(self):
        ''' draws sprite to screen '''
        print 'render', self.rect.top
        
        #quick fix, will change when Sprite inherits from Layer
        #prevents background image from taking 10k years to load
        if self.rect.width < 100:
            #try: 
            #    if self.TEXT_TEST: print 'WORKINGHERE?'
            #except: pass
            pass
        else:      
            global_vars.window.blit(self.image, self.rect)
            return

        # FIXING render to use alpha colorkey #
        collisions = [sprite for sprite in global_vars.layerManager.layersList if sprite.rect.width < 100 and sprite.rect.colliderect(self.rect)]
        for sprite in collisions:
            global_vars.window.blit(sprite.image, sprite.rect)
        return
        #         WORKING     WORKING         #


        pix = pygame.PixelArray(self.image.copy())
        for i in range(self.rect.height):
            for j in range(self.rect.width):
                testp =  self.getPixel(self.rect.left + j, self.rect.top + i)
                pix[j][i] = testp
                #try: 
                #    if self.TEXT_TEST: print pix[j]
                #except: pass
        blitSurface = pix.make_surface()
        del pix
        global_vars.window.blit(blitSurface, self.rect)
        #try: 
        #    if self.TEXT_TEST: global_vars.window.blit(blitSurface, (250,250))
        #except: pass
        
    def wipe(self):
        ''' erases sprite '''

        global_vars.layerManager.terrainView.terrain.changed = self.rect
        global_vars.layerManager.terrainView.drawTerrain()
        self.image.fill(pygame.Color('white'))

    def move(self, x, y):
        ''' redraws sprite when it moves '''
        
        if x == self.rect.left and y == self.rect.top: return
        
        # wipe, draw background over rect
        global_vars.layerManager.terrainView.terrain.changed = self.rect
        global_vars.layerManager.terrainView.drawTerrain()

        # render a transparent rect, so that other objects caught in the wipe will rerender
        tempImage = self.image
        self.image = self.image.copy()
        self.image.fill(pygame.Color('white'))
        self.render()
        self.image = tempImage

        # render this at new location
        self.rect.left = x
        self.rect.top = y
        self.render()

class AnimatedSprite(Sprite):
    ''' An animated sprite '''

    def __init__(self, image, rect, filesDict):
        '''
        filesDict will contain a dictionary of file name -> list pairs where the list
        is a list of names corresponsing with frames. If there is more than one, the
        file will be sliced up. Ex:

        { "death_sprites.bmp": ["death0", "death1", "death2"] } will split the
        death_sprites.bmp file into three images, which can later be displayed
        for animation
        '''

        self.filesDict = filesDict
        self.imagesDict = None
        for key in self.filesDict:
            self.cutImages(key, self.filesDict.get(key))

        Sprite.__init__(self, self.imagesDict['idle0'], rect)

    def cutImages(self, img, names):
        ''' slices up an image into individual frames '''

        if len(names) == 1:
            tempSurface = pygame.image.load(img)
            self.__dict__[names[0]] = tempSurface
            if self.imagesDict == None:
                self.imagesDict = dict()
            self.imagesDict[names[0]] = tempSurface
        else:
            allImages = pygame.image.load(img)
            tempSurface = pygame.Surface((allImages.get_width() // len(names), allImages.get_height()))
            cutter = tempSurface.get_rect()
            if self.imagesDict == None:
                self.imagesDict = dict()
            for i, name in enumerate(names):
                cutter.left += cutter.width * i + 1
                tempSurface.blit(allImages, (0,0), area = cutter)
                tempSurfaceCopy = tempSurface.copy()
                self.__dict__[name] = tempSurfaceCopy
                self.imagesDict[name] = tempSurfaceCopy

    def animate(self, name):
        ''' updates the sprite's image to the next frame '''

        self.frame += 1
        try:
            st = name + str(self.frame)
            if st not in self.imagesDict.keys():
                self.frame = 0
                st = name + str(self.frame)
            self.image = self.imagesDict[st]
        except: 
            print 'animation error'
            pass

    def set_img(self, name):

        self.image = self.imagesDict[name]