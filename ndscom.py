#!/usr/bin/python

import socket
import json
import os

class NdsCom():
	def __init__(self, host, port):
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def create_item(self, path):
		data = {}
		data['request'] = 'create_item'
		
		if not os.path.isfile(path):
			return 1, ''
		data['path'] = os.path.abspath(path)

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, ''
		else:
			return 0, result['uid']

	def delete_item(self, uid):
		data = {}
		data['request'] = 'delete_item'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1
		else:
			return 0

	def get_item(self, uid):
		data = {}
		data['request'] = 'get_item'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, {}
		else:
			return 0, result['item']

	def get_item_count(self):
		data = {}
		data['request'] = 'get_item_count'

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, 0
		return 0, result['item_count']

	def get_uids(self, maxNum):
		data = {}
		data['request'] = 'get_items'
		data['maxNum'] = maxNum
		
		result = self.doCom(data)
		if result['response'] != 0:
			return 1, {}
		return 0, result['

	def get_state(self, uid):
		data = {}
		data['request'] = 'get_state'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, ''
		return 0, result['state']

	def get_path(self, uid):
		data = {}
		data['request'] = 'get_path'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, ''
		return 0, result['path']

	def get_size(self, uid):
		data = {}
		data['request'] = 'get_size'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, 0
		return 0, result['size']

	def get_create_time(self, uid):
		data = {}
		data['request'] = 'get_create_time'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, ''
		return 0, result['create_time']

	def update_state(self, uid, state):
		data = {}
		data['request'] = 'update_state'
		data['uid'] = uid
		data['state'] = state

		result = self.doCom(data)
		if result['response'] != 0:
			return 1
		return 0

	def doCom(self, data):
		msg = json.dumps(data)
		self.s.sendto(msg, self.address)
		result,addr = self.s.recvfrom(40960)

		return json.loads(result)
