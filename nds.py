#!/usr/bin/python

from cnfmanager import CnfManager
from dbmanager import DbManager
from msgmanager import MsgManager
from ndlcom import NdlCom
from netmanager import NetManager
import ndutil
import getopt
import sys
import os

from twisted.internet import reactor

def nds_loop(doInit):
	ndutil.setTimezone()

	ndlCom = NdlCom('nDroid-Storage', '127.0.0.1', 12322)
	ndlCom.doCom('Initiating')

	ndlCom.doCom('Loading Configuration')
	cnfManager = CnfManager()
	cnfManager.load('./nds.cnf')
	cnfData = cnfManager.getCnfData()

	ndutil.enableDir(cnfData['storageDir'])

	ndlCom.doCom('Connecting to DB')
	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])
	if doInit:
		dbManager.create_table()
		os.system('rm -fr %s/*' % cnfData['storageDir'])

	msgManager = MsgManager()

	netManager = NetManager()
	netManager.setStorageDir(cnfData['storageDir'])
	netManager.setFileMode(cnfData['fileMode'])
	netManager.setNdlCom(ndlCom)
	netManager.setDbManager(dbManager)
	netManager.setMsgManager(msgManager)

	reactor.listenUDP(cnfData['comPort'], netManager)
	ndlCom.doCom('Listening Com Port')
	reactor.run()

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'i')

	doInit = False

	for opt, arg in opts:
		if opt in ('-i'):
			doInit = True

	nds_loop(doInit)
