'''
Created on May 15, 2014

This is a controller.

@author: Collin
'''
import global_vars
import events

class Controller:
	''' A controller '''

	def __init__(self, turn):
		self.eventManager = global_vars.eventManager
		self.turn = turn
		self.actor = global_vars.idLookup[self.turn]

	def changeTurn(self):
		self.turn += 1
		if self.turn == len(global_vars.idLookup): self.turn = 0
		try:
			while not self.eventManager.isMember(global_vars.idLookup[self.turn]):
				self.turn += 1
		except: self.changeTurn()
		e = events.Event(type = 'turn', t = self.turn)
		self.eventManager.post(e)
		return self.turn