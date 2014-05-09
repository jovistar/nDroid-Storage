#!/usr/bin/python

import json

class MsgManager():
	def resRequest(self, msg):
		data = json.loads(msg)
		cmds = ['create_item', 'delete_item', 'get_item', 'get_item_count', 'get_uids', 'get_path', 'get_size', 'get_create_time']

		if data['request'] == None:
			return 1, {}

		if data['request'] not in cmds:
			return 1, {}

		return 0, data

	def genResponse(self, data):
		return json.dumps(data)
