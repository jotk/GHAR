#!/usr/bin/env python3

from property import Property

class Landlord:
    def __init__(self, userID, DBconnect):
        self.userID = userID
        self.DBconnect = DBconnect
        self.firstname = self.DBconnect.getFirstName(self.userID)
        self.lastname = self.DBconnect.getLastName(self.userID)
        self.listOfPropertyDicts = self.DBconnect.getPropertyListofDict(self.userID)
        self.properties = []
        for propInfoDict in self.listOfPropertyDicts:
            prop = Property()
            prop.initPropInfo(propInfoDict)
            prop.getAPIinfo(DBconnect)
            # prop.initZillowInfo("X1-ZWz17njsl1wx6z_3mmvk")
            self.properties.append(prop)

    def getFirstName(self):
        return self.firstname

    def getLastName(self):
        return self.lastname

    def getPropertyIDList(self):
        return self.propertyIDList

    def getProperties(self):
        return self.properties




