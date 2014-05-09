#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
	def load(self, cnfFile):
		if not os.path.isfile(cnfFile):
			cnfFile = './nds.cnf'

		cf = ConfigParser.ConfigParser()
		cf.read(cnfFile)

		self.cnfData = {}
		self.cnfData['storageDir'] = cf.get('dir', 'storageDir')
		if cf.get('set', 'fileMode') == 'move':
			self.cnfData['fileMode'] = 'move'
		else:
			self.cnfData['fileMode'] = 'copy'
		self.cnfData['dbHost'] = cf.get('db', 'dbHost')
		self.cnfData['dbUser'] = cf.get('db', 'dbUser')
		self.cnfData['dbPass'] = cf.get('db', 'dbPass')
		self.cnfData['dbName'] = cf.get('db', 'dbName')
		self.cnfData['comPort'] = int(cf.get('com', 'comPort'))

	def getCnfData(self):
		return self.cnfData
