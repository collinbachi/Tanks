'''
Created on Jun 2, 2013

Currently a useless layer of abstraction, but will gain responsibilities as the
game grows.

@author: Collin
'''
import global_vars

class Layer:
    ''' represents a graphical layer '''
    
    def __init__(self, content):

        self.depth = global_vars.layerManager.getHighestDepth()
        self.content = content;
        self.render()
        
    def getPixel(self, x, y, returnsToManager=False):

        return self.content.getPixel(x, y, returnsToManager)
    
    def render(self):

        self.content.render()
        
    def kill(self):

        global_vars.eventManager.unsubscribe(self)