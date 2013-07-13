'''
Created on Jun 2, 2013

@author: Collin
'''
import global_vars

class Layer:
    ''' represents a graphical layer '''
    
    def __init__(self, content): #, depth=global_vars.layerManager.getHighestDepth()): ##DEPTH SHOULD INITIATE ITSELF
        self.depth = global_vars.layerManager.getHighestDepth()
        self.content = content;
        self.render()
        
    def getPixel(self, x, y, returnsToManager=False):
        return self.content.getPixel(x, y, returnsToManager)
    
    def render(self):
        self.content.render()
        
    def kill(self):
        global_vars.eventManager.unsubscribe(self)