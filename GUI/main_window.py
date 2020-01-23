#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMenu, QAction, QMainWindow, QApplication, QMenuBar, QScrollArea, QWidget
from propertyWidget import PropertyWidget
from PyQt5.QtCore import pyqtSignal, Qt
from main_widget import Main_widget


class MainWindow(QMainWindow):
    """
    Opens main widow with a widget for each property registered to account
    """
    def __init__(self, user, DBconnect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DBconnect = DBconnect
        self.user = user
        self.setWindowTitle("Welcome " + self.user.getFirstName().capitalize() + "!")
        self.properties = None
        self.mainMenu = None
        self.profile = None
        self.goToProfile = None
        self.signOut = None # action, connection in driver
        self.goToSite = None # action, connection in driver
        self.openInBrowser = None # action, connection in driver

        self.properties = self.user.getProperties() # list of property objects which is retrieved from the landlord object
        self.createMenuBar() # creates menu bar
        self.initWidget(self.properties)
        # self.createScrollBar() # creates the area for scrolling
        # self.showProperties() # creates and shows property widgets

    def createMenuBar(self):
        self.mainMenu = self.menuBar()  # Better var name?
        self.profile = self.mainMenu.addMenu("Profile")

        self.signOut = QAction("Sign Out")

        self.profile.addAction(self.signOut)

        self.goToSite = self.mainMenu.addMenu("Go to our site")
        self.openInBrowser = QAction("Open in Default Browser")
        self.goToSite.addAction(self.openInBrowser)

    def initWidget(self, props):
        self.mainWidget = Main_widget(props)
        self.setCentralWidget(self.mainWidget)


    # def createScrollBar(self):
    #     # Set self.scroll as QScrollArea to make window scrollable
    #     self.scroll = QScrollArea()
    #     # self.scroll = QWidget()
    #     self.setCentralWidget(self.scroll)

    #
    # def showProperties(self):
    #     self.properties = self.user.getProperties()  # list of property objects which is retrieved from the landlord object
    #     self.propertiesWidget = PropertyWidget(self.properties)
    #     self.propertiesWidget.createPropWidgets()
    #     # self.scroll.setWidget(self.propertiesWidget)
    #     self.setCentralWidget(self.propertiesWidget)



if __name__ == "__main__":
  app = QApplication([])
  mw = MainWindow("Dave", None)
  mw.show()
  exit(app.exec())