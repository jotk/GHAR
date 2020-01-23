import sys
import os

UP_ONE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DB"))
sys.path.append(UP_ONE_DIR)

from connectToDB import DBconnect


class GUIConnectToDB(DBconnect):
	def __init__(self, host, database, user, password):
		super().__init__(host, database, user, password)
