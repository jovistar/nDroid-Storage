#!/usr/bin/python

import socket
import json

def test():
	address = ('127.0.0.1', 12321)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	data = {'request':'create', 'path':'/root/nDroid-Storage/s.apk'}
	msg = json.dumps(data)

	s.sendto(msg, address)
	result,addr = s.recvfrom(2048)
	print result

if __name__ == '__main__':
	test()
