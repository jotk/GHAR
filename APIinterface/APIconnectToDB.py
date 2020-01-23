
import sys
sys.path.insert(0, '/Users/jotkaur/Desktop/LASPProject/DB')
#
from connectToDB import DBconnect

class APIConnectToDB(DBconnect):
	def __init__(self):
		super().__init__()
	def printServerSpec(self): #dont print the sql connection info because its command line interface
		pass
	def printDBSpec(self):
		pass
