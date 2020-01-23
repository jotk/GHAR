#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from logInWidget import LogInWidget
from PyQt5.QtCore import pyqtSignal
from functools import partial



class LogInWindow(QMainWindow):
    """ QMainWindow which shows the user a log-in interface
    Parameters:
    """
    user_found = pyqtSignal(int)
    def __init__(self, driver, DBconnect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = driver
        self.userID = None
        self.setWindowTitle("Log-In -- Property Data Extractor")
        #self.setFixedSize(350,130)
        # create log in widget
        self.li_widget = LogInWidget(DBconnect)
        self.setCentralWidget(self.li_widget)
        self.setGeometry(100, 100, 200, 100)
        # connect the submit click to a method in this class to validate
        self.li_widget.submit.clicked.connect(partial(self.submitClicked, self.li_widget.email, self.li_widget.password))


        # Connect submit button (LogInWidget) signal here to a method in this class


    def submitClicked(self, email, pwd):
        """ Checks if email is valid and is called through submit button from logInWidget
        Parameters: email (String), password (String)
        Return: none
        """
        validateLogin = self.li_widget.logInValid(email, pwd) # returns false here because email is empty, should be true
        print("validate Login = ", validateLogin)
        print("email and pwd in submitClicked: ", type(email), pwd)
        if validateLogin[0] == True:
            self.userID = validateLogin[1]
            #print("userID should be not none here: ", self.userID)
            #self.parent.logInSucceeded(self.userID)
            self.user_found.emit(self.userID)

    def logInSucc(self, idNum):
        """trash"""
        self.parent.openMainWindow(idNum)
        self.close()

    # def getUser(self):
    #     return self.userID
