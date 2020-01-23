
from APIs.realEstateAPIv4 import homeInfo
from APIs.zillowAPI import ZillowAPI

class Property:
    """
    Holds info for the property and can initialize zillow and estated api info, can retrieve info from db given connection
    """
    def __init__(self):
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
        self.APIinfo = None
        self.zillowAnalysis = None

    def initZillowInfo(self, zid):
        if self.streetAddress != None and self.city != None and self.zipcode != None:
            self.zillowAnalysis = ZillowAPI(zid, self.streetAddress, self.city,  self.state, str(self.zipcode))
            self.zillowAnalysis.initComps() # try to extract data from the data returned by the api
            self.zillowAnalysis.initZestimate()
            self.zillowAnalysis.compsAnalysis()
        else:
            print("Initialize Property Info First")

    def getAPIinfo(self, dbcon):
        if self.id != None:
            if dbcon.hasAPIBeenCalled(self.id):
                self.APIinfo = homeInfo()
                self.APIinfo.getFromDB(dbcon, self.id)
            else:
                self.freshApiCall(dbcon) # calls api and saves it to the db
        else:
            print("Cannot get api info for a property with no ID set")

    def freshApiCall(self, dbcon):
        """
        Initiliazes the API call object based off the street address and dbcon.
        :param dbcon: postgresql db connection
        :return: nothing
        """
        self.APIinfo = homeInfo()
        if self.streetAddress != None:
            self.APIinfo.callApi(self.streetAddress, dbcon, self.id)
        else:
            print("Cannot call API for an address which is not set")

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

    def setInfo(self, streetAd, city, state, zipcode, propName):
        """
        Manually set the info for the class.
        :param streetAd: string
        :param city: string
        :param state: two letter string
        :param zipcode: int
        :param propName: string
        :return: nothing
        """
        self.streetAddress = streetAd
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.propName = propName


