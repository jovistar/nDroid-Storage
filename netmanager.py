#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol
from ndlcom import NdlCom
from dbmanager import DbManager
from msgmanager import MsgManager
import ndutil
import os
import shutil

class NetManager(DatagramProtocol):
	def setNdlCom(self, ndlCom):
		self.ndlCom = ndlCom

	def setStorageDir(self, storageDir):
		self.storageDir = storageDir

	def setMsgManager(self, msgManager):
		self.msgManager = msgManager

	def setDbManager(self, dbManager):
		self.dbManager = dbManager

	def datagramReceived(self, data, (host, port)):
		retCode, result = self.msgManager.resRequest(data)
		if retCode != 0:
			self.ndlCom.doCom('Bad Request From %s:%d' % (host, port))
		else:
			responseData = None
			self.ndlCom.doCom('Request: %s From %s:%d' % (result['request'], host, port))
			if result['request'] == 'create_item':
				responseData = self.dispatch_create_item(result['path'])
			elif result['request'] == 'delete_item':
				responseData = self.dispatch_delete_item(result['uid'])
			elif result['request'] == 'get_item':
				responseData = self.dispatch_get_item(result['uid'])
			elif result['request'] == 'get_item_count':
				responseData = self.dispatch_get_item_count()
			elif result['request'] == 'get_uids':
				responseData = self.dispatch_get_uids(result['start'], result['num'])
			elif result['request'] == 'get_path':
				responseData = self.dispatch_get_path(result['uid'])
			elif result['request'] == 'get_size':
				responseData = self.dispatch_get_size(result['uid'])
			elif result['request'] == 'get_create_time':
				responseData = self.dispatch_get_create_time(result['uid'])

			msg = self.msgManager.genResponse(responseData)
			self.transport.write(msg, (host, port))

	def dispatch_create_item(self, path):
		responseData = {}
		if not os.path.isfile(path):
			responseData['response'] = 1
		else:
			responseData['response'] = 0

			uid = ndutil.getUid(path)
			if self.dbManager.exists(uid):
				responseData['uid'] = uid
				os.remove(path)
			else:
				size = ndutil.getSize(path) / 1024
				createTime = ndutil.getCreated()
						
				fileExt = os.path.basename(path).split('.', 1)
				dirPath = self.enable_storage_dir(self.storageDir, uid)
				newPath = '%s/%s.%s' % (dirPath, uid, fileExt[1])
				shutil.copyfile(path, newPath)
				path = ndutil.getAbstractPath(newPath)

				self.dbManager.create_item(uid, path, createTime, size)
				responseData['uid'] = uid
		return responseData

	def enable_storage_dir(self, storageDir, uid):
		dirPath = '%s/%s/%s/%s/%s' % ( storageDir, uid[0:4], uid[4:8], uid[8:12], uid[12:16])
		ndutil.enableDir(dirPath)
		return dirPath

	def dispatch_delete_item(self, uid):
		responseData = {}
		if not self.dbManager.exists(uid):
			responseData['response'] = 1
		else:
			responseData['response'] = 0
			path = ndutil.getAbstractPath(self.dbManager.get_path(uid))
			self.dbManager.delete_item(uid)
			os.remove(path)
		return responseData

	def dispatch_get_item(self, uid):
		responseData = {}
		if not self.dbManager.exists(uid):
			responseData['response'] = 1
		else:
			result = self.dbManager.get_item(uid)
			if result == None:
				responseData['response'] = 1
			else:
				responseData['response'] = 0
				responseData['item'] = result
		return responseData

	def dispatch_get_item_count(self):
		responseData = {}
		result = self.dbManager.get_item_count()
		responseData['response'] = 0
		responseData['item_count'] = result
		return responseData

	def dispatch_get_uids(self, start, num):
		responseData = {}
		result = self.dbManager.get_uids(start, num)
		if result == None:
			responseData['response'] = 1
		else:
			responseData['response'] = 0
			responseData['uids'] = result
		return responseData

	def dispatch_get_path(self, uid):
		responseData = {}
		result = self.dbManager.get_path(uid)
		if result == None:
			responseData['response'] = 1
		else:
			responseData['response'] = 0
			responseData['path'] = result
		return responseData

	def dispatch_get_size(self, uid):
		responseData = {}
		result = self.dbManager.get_size(uid)
		if result == None:
			responseData['response'] = 1
		else:
			responseData['response'] = 0
			responseData['size'] = result
		return responseData

	def dispatch_get_create_time(self, uid):
		responseData = {}
		result = self.dbManager.get_create_time(uid)
		if result == None:
			responseData['response'] = 1
		else:
			responseData['response'] = 0
			responseData['create_time'] = result
		return responseData
