
import requests
class homeInfo:
    def __init__(self, addressInList):
        self.homeName = addressInList[1] + " House" #extracts street address, should fix this so it takes into cons. 123 S. Ithaca type of case
        self.address = " ".join(addressInList)
        addressInUrl = "%20".join(addressInList)
        self.APIkey = "Izf4LJCSsPKkcrpqgQvnPwWChFHICX"
        self.APIcall = "https://api.estated.com/property/v3?token=" + self.APIkey + "&conjoined_address=" + addressInUrl
        #sandbox API below, line commented above is true API call
        #self.APIcall = "https://sandbox.estated.com/property/v3?token=Izf4LJCSsPKkcrpqgQvnPwWChFHICX&conjoined_address=3832+Jason+St,Denver,CO+80211"
        response = requests.get(self.APIcall)
        data = response.json()
        if data["success"] == False:
            raise Exception("The address could not be found. Ensure that it is typed correctly. Otherwise, there is no information on property.")
        self.ownerName = None
        self.isCorporate = None
        self.ownerAddress = None
        self.streetAddress = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.lat = None
        self.long = None
        self.year_built = None
        self.rooms = None
        self.bedrooms = None
        self.baths = None
        self.stories = None
        self.square_feet = None
        self.finished_square_feet = None
        self.basement_square_feet = None
        self.garage_square_feet = None
        self.building_type = None
        self.fireplace_count = None
        self.parking_type = None
        self.pool_type = None
        self.land_value = None
        self.improvement_value = None
        self.total_value = None
        self.appraised_value = None
        self.last_sell_date = None
        self.price = None
        self.last_seller = None
        self.sales = []
        self.value = None
        self.suggested_rental = None
        self.forecast_year = None
        self.market_value_change_year = None
        self.elem_school = None
        self.elem_low_grade = None
        self.elem_high_grade = None
        self.sec_school = None
        self.sec_low_grade = None
        self.sec_high_grade = None
        #property
        self.propertyInfo = data["properties"][0]
        self.initPropertyInfo(self.propertyInfo)


    def initPropertyInfo(self, props):
        self.initOwnerInfo(props["owners"][0])
        self.initAddressInfo(props["addresses"][0])
        self.initGeocodingInfo(props["geocoding"])
        self.initStructuresInfo(props["structures"][0])
        self.initAssessmentInfo(props["assessments"][0])
        self.initLatestSaleInfo(props["sales"][0])
        self.initAllSaleInfo(props["sales"])
        self.initValuationInfo(props["valuation"])
        self.initElemSchoolInfo(props["geographies"]["school_elementary"])
        self.initSecSchoolInfo(props["geographies"]["school_secondary"])
        self.neighborhood = props["geographies"]["neighborhood"]

    def initOwnerInfo(self, owner):
        self.ownerName = owner['name']
        self.isCorporate = owner['corporate_flag']
        self.ownerAddress = (owner['address'] + ", "+ owner['city'] + ", ", owner['state'], " ", owner['zip_code'])

    def initAddressInfo(self, address):
        self.streetAddress = address['formatted_street_address']
        self.city = address['city']
        self.state = address['state']
        self.zipcode = address['zip_code']

    def initGeocodingInfo(self, geo):
        self.lat = geo["street"]["latitude"]
        self.long = geo["street"]["longitude"]

    def initStructuresInfo(self, struct):
        self.year_built = struct["year_built"]
        self.rooms = struct["rooms_count"]
        self.bedrooms = struct["beds_count"]
        self.baths = struct["baths_count"]
        self.stories = struct["stories_count"]
        self.square_feet = struct["total_size"]
        self.finished_square_feet = struct["finished_size"]
        self.basement_square_feet = struct["basement_size"]
        self.garage_square_feet = struct["garage_size"]
        self.building_type = struct["building_type"]
        self.fireplace_count = struct["fireplace_count"]
        self.parking_type = struct["parking_type"]
        self.pool_type = struct["pool_type"]

    def initAssessmentInfo(self, asses):
        self.land_value = asses['land']
        self.improvement_value = asses['improvement']
        self.total_value = asses['total']
        self.appraised_value = asses['appraised_total']

    def initLatestSaleInfo(self, sale): # latest sale only
        self.last_sell_date = sale['date']
        self.price = sale['price']
        self.last_seller = sale['seller']

    def initAllSaleInfo(self):


    def initValuationInfo(self, valuation):
        self.value = valuation['value']
        self.suggested_rental = valuation['suggested_rental']
        self.forecast_year =  valuation['forecast_1_year']
        self.market_value_change_year = valuation["market_value_change_year"]

    def initElemSchoolInfo(self, school):
        self.elem_school = school['name']
        self.elem_low_grade = school['low_grade']
        self.elem_high_grade = school['high_grade']

    def initSecSchoolInfo(self, school):
        self.sec_school = school['name']
        self.sec_low_grade = school['low_grade']
        self.sec_high_grade = school['high_grade']

