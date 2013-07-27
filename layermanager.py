'''
Created on May 31, 2013

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
    Maintains a reference to all layersList. Increments depth. Creates new
    layersList. Singleton.
    '''
    
    def __init__(self):
        #print 'assigned'
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
        self.layersList.append(terrainView)
        #print 'terrainView depth: ', terrainView.depth
        self.layersList = sorted(self.layersList, key=attrgetter('depth'), reverse=True)
        return terrainView
    
    def newSprite(self, image, rect=None):
        if not isinstance(image, Sprite):
            sprite = Sprite(image, rect)
        else: 
            #print 'input was a sprite'
            sprite = image
        self.layersList.append(sprite)
        #print 'sprite depth: ', self.layersList[len(self.layersList) - 1].depth
        self.layersList = sorted(self.layersList, key=attrgetter('depth'), reverse=True)

        return sprite
        
    
    
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
        #self.render()
        self.myPixels = pygame.PixelArray(self.image.copy())
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
        
        if p != pygame.Color('white'): # and p != 16777215:
            #print "p: {}".format(p) + " is not white: {}".format(pygame.Color('white'))
            return p
        elif returnsToManager: return pygame.Color('white')
        else: 
            #print " {} is the color".format(global_vars.layerManager.getPixel(x, y))
            return global_vars.layerManager.getPixel(x, y)
    
    def render(self):
        ''' draws sprite to screen '''
        
        #quick fix, will change when Sprite inherits from Layer
        #prevents background image from taking 10k years to load
        if self.rect.width < 100:
            pass
        else: 
            #print 'CHECKCKCKKCC'
            global_vars.window.blit(self.image, self.rect)
            return
        pix = pygame.PixelArray(self.image.copy())
        for i in range(self.rect.height):
            for j in range(self.rect.width):
                testp =  self.getPixel(self.rect.left + j, self.rect.top + i)
                pix[j][i] = testp
        blitSurface = pix.make_surface()
        del pix
        global_vars.window.blit(blitSurface, self.rect)
        
        
    def move(self, x, y):
        ''' redraws sprite when it moves '''
        
        if x == self.rect.left and y == self.rect.top: return
        tempImage = self.image
        self.image = self.image.copy()
        self.image.fill(pygame.Color('white'))
        self.render()
        self.image = tempImage
        self.rect.left = x
        self.rect.top = y
        
        self.render()
        #global_vars.render_buffer.push(self)

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

        #global_vars.eventManager.subscribe(self, 'tick')
        #self._eventMap = {'tick': self.animate}
        Sprite.__init__(self, self.imagesDict['idle0'], rect)
        self.lastName = 'idle0'
        self.frame = 0

    def cutImages(self, img, names):
        if len(names) == 1:
            tempSurface = pygame.image.load(img)
            self.__dict__[names[0]] = tempSurface
            #self.filesDict.set(img, eval('self.{}'.format(names[0]))) MAYBE
            if self.imagesDict == None:
                self.imagesDict = dict()
            self.imagesDict[names[0]] = tempSurface
        else:
            allImages = pygame.image.load(img)
            #print allImages.get_width() // len(names), allImages.get_height(), ' width/height'
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

    def animate(self, name = '', LOOP = True):
        self.frame += 1
        if name == '':
            name = self.lastName
        else:
            self.lastName = name

        try:
            st = name + str(self.frame)
            if st not in self.imagesDict.keys():
                if LOOP:
                    self.frame = 0
                    st = name + str(self.frame)
                else:
                    return True #Done
            self.image = self.imagesDict[st]
        except: 
            print 'animation error' + str(self)
            pass
        #self.render()
        return False

    def set_img(self, name):
        self.image = self.imagesDict[name]