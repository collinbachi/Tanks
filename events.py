'''
Created on Jan 31, 2013

@author: Collin
'''
import time
class EventManager:
    
    def __init__(self):
        
        self.subscriptions = {}
        self.eventLog = []
    
    
    def subscribe(self, o, type):
        
        self.eventLog.append('SUBSCRIBE: ' + str(o) + ' ' + type)
        if o in self.subscriptions:
            self.subscriptions[o].append(type)
            
        else:
            self.subscriptions[o] = [type]
            
            
    def unsubscribe(self, o):
        
        self.subscriptions = {key: value for key, value in self.subscriptions.items() if key != o}
        self.eventLog.append('UNSUBSCRIBE: ' + str(o))

            
    def post(self, e):
        
        self.eventLog.append('Post: ' + str(e))
        for o in self.subscriptions.keys():
            if e.type in self.subscriptions[o]:
                o.processEvent(e)
                
                
    def printLog(self, type = 'NONE'):
        
        for s in self.eventLog:
            if type == 'NONE' or s.find(type) == 0: print s


class EventUser:
    
    def processEvent(self, e):
        
        if e.type in self._eventMap:
            self._eventMap[e.type]()
            
            
class Event:
    ''' bag of instance variables set upon initialization '''
    
    def __init__(self, **kw):
        
        for key in kw:
            self.__dict__[key] = kw[key]
        if self.type == 'turn': pass #print 'event', self.t
    
                