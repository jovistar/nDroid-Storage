#!/usr/bin/python

import MySQLdb

class DbManager():
	def __init__(self, dbHost, dbUser, dbPass, dbName):
		self.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
		self.dbCursor = self.dbCon.cursor()

	def create_table(self):
		self.drop_table()
		self.dbCursor.execute('CREATE TABLE storage(sid int auto_increment primary key not null, uid varchar(64) not null, path varchar(4096) not null, create_time varchar(128) not null, size int not null)')
		self.dbCon.commit()

	def drop_table(self):
		self.dbCursor.execute('DROP TABLE IF EXISTS storage')
		self.dbCon.commit()

	def create_item(self, uid, path, createTime, size):
		value = (0, uid, path, createTime, size)
		self.dbCursor.execute('insert into storage values(%s,%s,%s,%s,%s)', value)
		self.dbCon.commit()

	def update_item(self, uid, path, createTime, size):
		value = (path, createTime, size, uid)
		self.dbCursor.execute('update storage set path=%s,create_time=%s,size=%s where uid=%s', value)
		self.dbCon.commit()

	def delete_item(self, uid):
		self.dbCursor.execute('delete from storage where uid=%s', (uid,))
		self.dbCon.commit()

	def get_item(self, uid):
		count = self.dbCursor.execute('select * from storage where uid=%s', (uid,))
		if count:
			result = self.dbCursor.fetchone()
			value = {}
			value['sid'] = result[0]
			value['uid'] = result[1]
			value['path'] = result[2]
			value['create_time'] = result[3]
			value['size'] = int(result[4])
			return value
		else:
			return None

	def get_item_count(self):
		count = self.dbCursor.execute('select count(sid) from storage')
		if count:
			result = self.dbCursor.fetchone()
			return int(result[0])
		return 0

	def get_uids(self, start, num):
		if start < 0:
			start = 0
		if num < 0:
			num = -1
		count = self.dbCursor.execute('select uid from storage limit %s,%s', (start, num))
		if count:
			rows = self.dbCursor.fetchall()
			result = []
			for row in rows:
				result.append(row[0])

			return result
		else:
			return None

	def get_sid(self, uid):
		count = self.dbCursor.execute('select sid from storage where uid=%s', (uid,))
		if count:
			sid = self.dbCursor.fetchone()
			return int(sid[0])
		else:
			return None

	def get_path(self, uid):
		count = self.dbCursor.execute('select path from storage where uid=%s', (uid,))
		if count:
			path = self.dbCursor.fetchone()
			return path[0]
		else:
			return None

	def update_path(self, uid, path):
		value = (path, uid)
		self.dbCursor.execute('update storage set path=%s where uid=%s', value)
		self.dbCon.commit()

	def get_size(self, uid):
		count = self.dbCursor.execute('select size from storage where uid=%s', (uid,))
		if count:
			size = self.dbCursor.fetchone()
			return int(size[0])
		else:
			return None

	def update_size(self, uid, size):
		value = (size, uid)
		self.dbCursor.execute('update storage set size=%s where uid=%s', value)
		self.dbCon.commit()

	def get_create_time(self, uid):
		count = self.dbCursor.execute('select create_time from storage where uid=%s', (uid,))
		if count:
			created = self.dbCursor.fetchone()
			return created[0]
		else:
			return None

	def update_create_time(self, uid, createTime):
		value = (createTime, uid)
		self.dbCursor.execute('update storage set create_time=%s where uid=%s', value)
		self.dbCon.commit()

	def exists(self, uid):
		if self.get_sid(uid) != None:
			return True
		else:
			return False
