#!/usr/bin/python

import MySQLdb

class DbManager():
	def __init__(self, dbHost, dbUser, dbPass, dbName):
		self.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
		self.dbCursor = self.dbCon.cursor()

	def create(self, uid, path, created, size):
		value = (0, uid, path, created, size)
		self.dbCursor.execute('insert into storage values(%s,%s,%s,%s,%s)', value)
		self.dbCon.commit()

	def delete(self, uid):
		self.dbCursor.execute('delete from storage where uid=%s', uid)
		self.dbCon.commit()

	def getAll(self, uid):
		count = self.dbCursor.execute('select * from storage where uid=%s', uid)
		if count:
			result = self.dbCursor.fetchone()
			return result
		else:
			return None

	def getId(self, uid):
		count = self.dbCursor.execute('select sid from storage where uid=%s', uid)
		if count:
			sid = self.dbCursor.fetchone()
			return sid[0]
		else:
			return None

	def getPath(self, uid):
		count = self.dbCursor.execute('select path from storage where uid=%s', uid)
		if count:
			path = self.dbCursor.fetchone()
			return path[0]
		else:
			return None

	def getSize(self, uid):
		count = self.dbCursor.execute('select size from storage where uid=%s', uid)
		if count:
			size = int(self.dbCursor.fetchone())
			return size[0]
		else:
			return None

	def getCreated(self):
		count = self.dbCursor.execute('select created from storage where uid=%s', uid)
		if count:
			created = self.dbCursor.fetchone()
			return created[0]
		else:
			return None

	def exists(self, uid):
		if self.getId(uid) != None:
			return True
		else:
			return False

