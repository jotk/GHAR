
from realEstateAPI import homeInfo

class Property:
    def __init__(self, info, DBcon):
        #prop info
        self.id = None
        self.buyingPrice = None
        self.sellingPrice = None
        self.active = None
        self.buyDate = None
        self.sellDate = None
        self.avgRentalArea = None
        self.id_landlord = None
        self.streetAddress = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.propName = None
        self.imageName = None
        self.fullAddress = None
        self.monthlyRent = None
        self.monthlyMortgage = 0
        #lease on the property details
        # self.currentLease = None
        # self.leaseList = None
        self.sales = None
        self.initPropInfo(info)
        self.APIinfo = None
        self.getAPIinfo()

    def getAPIinfo(self):
        self.APIinfo = homeInfo(self.fullAddress.split())

    def initPropInfo(self, info):
        self.id = info["id_property"]
        if info["buyingPrice"] != None:
            self.buyingPrice = float(info["buyingPrice"])
        else:
            self.buyingPrice = None
        if info["sellingPrice"] != None:
            self.sellingPrice = float(info["sellingPrice"])
        else:
            self.sellingPrice = None
        self.active = info["active"]
        self.buyDate = info["buyDate"]
        self.sellDate = info["sellDate"]
        self.avgRentalArea = info["avgRentalArea"]
        self.id_landlord = info["id_landlord"]
        self.streetAddress = info["streetAddress"]
        self.city = info["city"]
        self.state = info["state"]
        self.zipcode = info["zipcode"]
        self.propName = info["propName"]
        self.imageName = info["imageName"]
        if info["monthlyMortgage"] != None:
            self.monthlyMortgage = float(info["monthlyMortgage"])
        else:
            self.monthlyMortgage = 0
        self.fullAddress = self.streetAddress + ", " + self.city + " " + self.state

