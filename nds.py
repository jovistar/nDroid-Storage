#!/usr/bin/python

from cnfmanager import CnfManager
from dbmanager import DbManager
from msgmanager import MsgManager
from ndlcom import NdlCom
from netmanager import NetManager
import ndutil

from twisted.internet import reactor

def nds_loop():
	ndutil.setTimezone()

	ndlCom = NdlCom('nDroid-Storage', '127.0.0.1', 12322)
	ndlCom.doCom('Initiating')

	ndlCom.doCom('Loading Config')
	cnfManager = CnfManager()
	cnfManager.load('./nds.cnf')
	cnfData = cnfManager.getCnfData()

	ndutil.enableDir(cnfData['storageDir'])

	ndlCom.doCom('Connecting to DB')
	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])

	msgManager = MsgManager()

	netManager = NetManager()
	netManager.setStorageDir(cnfData['storageDir'])
	netManager.setNdlCom(ndlCom)
	netManager.setDbManager(dbManager)
	netManager.setMsgManager(msgManager)

	reactor.listenUDP(cnfData['comPort'], netManager)
	ndlCom.doCom('Listening Com Port')
	reactor.run()


if __name__ == '__main__':
	nds_loop()
