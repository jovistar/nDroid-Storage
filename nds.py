#!/usr/bin/python

from cnfmanager import CnfManager
from dbmanager import DbManager
from msgmanager import MsgManager
from logger import Logger
from netmanager import NetManager
import ndutil

from twisted.internet import reactor

def nds_loop():
	ndutil.setTimezone()

	logger = Logger('LOGPRINT')
	logger.logger('Initiating')

	logger.logger('Loading Config')
	cnfManager = CnfManager()
	cnfManager.load('./nds.cnf')
	cnfData = cnfManager.getCnfData()

	ndutil.enableDir(cnfData['storageDir'])

	logger.logger('Connecting to DB')
	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])

	msgManager = MsgManager()

	netManager = NetManager()
	netManager.setStorageDir(cnfData['storageDir'])
	netManager.setLogger(logger)
	netManager.setDbManager(dbManager)
	netManager.setMsgManager(msgManager)

	reactor.listenUDP(cnfData['comPort'], netManager)
	logger.logger('Listening Com Port')
	reactor.run()


if __name__ == '__main__':
	nds_loop()
