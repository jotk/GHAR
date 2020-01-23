#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication
import webbrowser

from log_in_window import LogInWindow
from main_window import MainWindow
from DB.herokuPostgresDBConnect import DBconnect

from landlord import Landlord


class driver:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.DBconnection = None
        self.user = None
        self.login = None
        self.mw = None
        self.stylesheet = """
        QMainWindow{
            background-color: #97CBE1;
        }
        QLabel{
            color: #031523;
        }
        QLineEdit{
            background-color: #C4F3C4;
        }
        QPushButton{
            background-color: #031523;
            color: white;
        }
        QPixMap{
            box-shadow: 10px 10px 5px #B8F9C3;
        }
        """
        self.app.setStyleSheet(self.stylesheet)

    def createDBConnect(self, host='laspjot.cc3mhnvgoaaz.us-east-2.rds.amazonaws.com', database='proj', user='admin', password='welcome123'):
        if self.DBconnection == None:
            try:
                self.DBconnection = DBconnect(host, database, user, password)
            except:
                print("Cannot connect to DB.")
                self.closeApp()
        else:
            print("DB connection already exists")



    def openLoginWindow(self):
        self.login = LogInWindow(self, self.DBconnection)
        self.login.li_widget.newuser.clicked.connect(self.makeNewUser)
        self.login.user_found.connect(self.openMainWindow)
        self.login.show()  # self.login.exec()
        #self.user = self.login.getUser()
        # Get email and password from logIn and set class variables

    def makeNewUser(self):
        webbrowser.open('https://ghar-property-manager.herokuapp.com/signup')

    def getApp(self):
        return self.app

    def openMainWindow(self, userID):
        if self.login != None:
            self.login.close()
        self.user = Landlord(userID, self.DBconnection)
        self.mw = MainWindow(self.user, self.DBconnection)
        #slots
        self.mw.signOut.triggered.connect(self.logOut) #logout when "sign out" is clicked in mw's menu bar

        self.mw.openInBrowser.triggered.connect(self.openSite)
        self.mw.mainWidget.propertiesWidget.closeOut.clicked.connect(self.mw.close)
        self.mw.mainWidget.propertiesWidget.goToSite.clicked.connect(self.openSite)
        self.mw.show()

    def openSite(self):
        """
        Opens the GHAR homepage
        :return:
        """
        webbrowser.open('https://ghar-property-manager.herokuapp.com/home')

    def logOut(self):
        self.user = None
        self.mw.close()
        self.mw = None
        self.openLoginWindow()

    def runApp(self):
        self.app.exec()
        if self.DBconnection != None:
            self.DBconnection.closeConnection()


def main():
    myApp = driver()
    myApp.createDBConnect(host="localhost", database="mydb", user="root", password="lol")
    myApp.openLoginWindow()
    exit(myApp.runApp())

if __name__ == "__main__":
    main()
