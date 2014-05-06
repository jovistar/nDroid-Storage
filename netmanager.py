#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol
from ndlcom import NdlCom
from dbmanager import DbManager
from msgmanager import MsgManager
import ndutil
import os
import shutil

class NetManager(DatagramProtocol):
	def setLogger(self, ndlCom):
		self.ndlCom = ndlCom

	def setStorageDir(self, storageDir):
		self.storageDir = storageDir

	def setMsgManager(self, msgManager):
		self.msgManager = msgManager

	def setDbManager(self, dbManager):
		self.dbManager = dbManager

	def datagramReceived(self, data, (host, port)):
		self.ndlCom.doCom('Request from %s:%d' % (host, port))
		self.dispatch(data, host, port)

	def dispatch(self, data, host, port):
		retCode, result = self.msgManager.resRequest(data)
		if retCode != 0:
			self.ndlCom.doCom('Error Request')
		else:
			responseData = {}
			if result['request'] == 'create':
				self.ndlCom.doCom('Request: CREATE')
				if not os.path.isfile(result['path']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0

					uid = ndutil.getUid(result['path'])
					if self.dbManager.exists(uid):
						responseData['uid'] = uid
						os.remove(result['path'])
					else:
						size = ndutil.getSize(result['path'])
						created = ndutil.getCreated()
						
						fileExt = os.path.basename(result['path']).split('.', 1)
						newPath = '%s/%s.%s' % (self.storageDir, uid, fileExt[1])
						shutil.move(result['path'], newPath)
						path = ndutil.getAbstractPath(newPath)

						self.dbManager.create(uid, path, created, size)
						responseData['uid'] = uid
				
			if result['request'] == 'delete':
				self.ndlCom.doCom('Request: DELETE')
				if not self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					path = ndutil.getAbstractPath(self.dbManager.getPath(result['uid']))
					self.dbManager.delete(result['uid'])
					os.remove(path)

			if result['request'] == 'get':
				self.ndlCom.doCom('Request: GET')
				if not self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					responseData['path'] = ndutil.getAbstractPath(self.dbManager.getPath(result['uid']))

			msg = self.msgManager.genResponse(responseData)
			self.transport.write(msg, (host, port))
