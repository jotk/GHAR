
import requests, json
class homeInfo:
    def __init__(self):
        self.ownerName = None
        self.isOwnerOccupied = None #used to be isCorporate
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
        self.basement_finished_square_feet = None
        self.basement_unfinished_square_feet = None
        self.garage_square_feet = None
        self.building_type = None
        self.fireplace_count = None
        self.parking_type = None
        self.pool_type = None
        self.last_sell_date = None
        self.price = None
        self.last_seller = None
        self.value = None
        self.suggested_rental = None
        self.forecast_year = None
        self.market_value_change_year = None
        self.zipcode_plusfour = None
        self.secondName = None
        self.parking_spaces_count = None
        self.architecture_type = None
        self.construction_type = None
        self.heating_type = None
        self.ac_type = None
        self.unit_number = None
        self.quality = None
        self.condition = None
        self.assessment_land_value = None
        self.assessment_improvement_value = None
        self.assessment_total_value = None
        self.assessment_year = None
        self.market_assessment_year = None
        self.market_land_value = None
        self.market_improvement_value = None
        self.market_total_value = None
        self.deeds = []
        self.partial_baths = None
        self.value = None
        self.high_value = None
        self.low_value = None
        self.forecast_stan_dev =  None
        self.date_of_valuation = None
        self.APIkey = "NWhdlYsHrnLFYLWxPHRStxRyeCZjLn"
        #property

    def getFromDB(self, dbcon, propID):
        self.propertyInfo = json.loads(dbcon.getApiCallJSON(propID))
        self.initPropertyInfo(self.propertyInfo)

    def callApi(self, addressInList, dbcon, propid):
        self.homeName = addressInList[1] + " House" #extracts street address, should fix this so it takes into cons. 123 S. Ithaca type of case
        self.address = " ".join(addressInList)
        addressInUrl = "%20".join(addressInList)
        #self.APIcall = "https://api.estated.com/property/v3?token=" + self.APIkey + "&conjoined_address=" + addressInUrl
        #sandbox API below, line commented above is true API call
        self.APIcall = 'https://apis.estated.com/v4/property?token=NWhdlYsHrnLFYLWxPHRStxRyeCZjLn&combined_address=1280 Ithaca Dr,Boulder,CO 80305'
        response = requests.get(self.APIcall)
        data = response.json()
        if "error" in data:
            raise Exception("The address could not be found. Ensure that it is typed correctly. Otherwise, there is no information on property.")
        self.propertyInfo = data["data"]
        dbcon.setAPICallJSON(propid, json.dumps(data["data"]))
        self.initPropertyInfo(self.propertyInfo)

    def initPropertyInfo(self, props):
        self.initOwnerInfo(props["owner"])
        self.initAddressInfo(props["address"])
        self.initStructuresInfo(props["structure"])
        self.initAssessmentInfo(props["assessments"][0], props["market_assessments"][0])
        self.initSaleInfo(props["deeds"])
        self.initValuationInfo(props["valuation"])


    def initOwnerInfo(self, owner):
        self.ownerName = owner['name']
        self.secondName = owner['second_name']
        self.isOwnerOccupied = owner['owner_occupied'] # YES or NO value
        self.ownerAddress = (owner['formatted_street_address'] + ", "+ owner['city'] + ", ", owner['state'], " ", owner['zip_code'])

    def initAddressInfo(self, address):
        self.streetAddress = address['formatted_street_address']
        self.city = address['city']
        self.state = address['state']
        self.zipcode = address['zip_code']
        self.lat = address['latitude']
        self.long = address['longitude']
        self.zipcode_plusfour = address['zip_plus_four_code']
        self.unit_number = address['unit_number']
        self.address = self.streetAddress + ", " + self.city + ", " + self.state


    def initStructuresInfo(self, struct):
        self.year_built = struct["year_built"]
        self.rooms = struct["rooms_count"]
        self.bedrooms = struct["beds_count"]
        self.baths = struct["baths"]
        self.partial_baths = struct["partial_baths_count"]
        self.parking_type = struct['parking_type']
        self.parking_spaces_count = struct['parking_spaces_count']
        self.architecture_type = struct['architecture_type']
        self.construction_type = struct['construction_type']
        self.heating_type = struct['construction_type']
        self.ac_type = struct['air_conditioning_type']
        self.stories = struct["stories"]
        self.square_feet = struct["total_area_sq_ft"]
        # self.finished_square_feet = klsads
        for astruct in struct["other_areas"]:
            if astruct["type"] == "GARAGE":
                self.garage_square_feet = astruct["sq_ft"]
            elif astruct["type"] == "BASEMENT FINISHED":
                self.basement_finished_square_feet = astruct["sq_ft"]
            elif astruct["type"] == "BASEMENT UNFINISHED":
                self.basement_unfinished_square_feet = astruct["sq_ft"]
        self.fireplace_count = struct["fireplaces"]
        self.pool_type = struct["pool_type"]
        self.quality = struct['quality']
        self.condition = struct['condition']

    def initAssessmentInfo(self, asses, mark_asses):
        self.assessment_land_value = asses['land_value']
        self.assessment_improvement_value = asses['improvement_value']
        self.assessment_total_value = asses['total_value']
        self.assessment_year = asses["year"]
        self.market_assessment_year = mark_asses["year"]
        self.market_land_value = mark_asses["land_value"]
        self.market_improvement_value = mark_asses["improvement_value"]
        self.market_total_value = mark_asses['total_value']


    def initSaleInfo(self, sales): # latest sale only
        for asale in sales:
            tempinfo = {
                "document_type"            : asale["document_type"],
                "recording_date"           : asale["recording_date"],
                "original_contract_date"   : asale["original_contract_date"],
                "deed_book"                : asale["deed_book"],
                "deed_page"                : asale["deed_page"],
                "document_id"              : asale["document_id"],
                "sale_price"               : asale["sale_price"],
                "sale_price_description"   : asale["sale_price_description"],
                "transfer_tax"             : asale["transfer_tax"],
                "distressed_sale"          : asale["distressed_sale"],
                "real_estate_owned"        : asale["real_estate_owned"],
                "seller_first_name"        : asale["seller_first_name"],
                "seller_last_name"         : asale["seller_last_name"],
                "seller2_first_name"       : asale["seller2_first_name"],
                "seller2_last_name"        : asale["seller2_last_name"],
                "seller_address"           : asale["seller_address"],
                "seller_unit_number"       : asale["seller_unit_number"],
                "seller_city"              : asale["seller_city"],
                "seller_state"             : asale["seller_state"],
                "seller_zip_code"          : asale["seller_zip_code"],
                "seller_zip_plus_four_code": asale["seller_zip_plus_four_code"],
                "buyer_first_name"         : asale["buyer_first_name"],
                "buyer_last_name"          : asale["buyer_last_name"],
                "buyer2_first_name"        : asale["buyer2_first_name"],
                "buyer2_last_name"         : asale["buyer2_last_name"],
                "buyer_address"            : asale["buyer_address"],
                "buyer_unit_type"          : asale["buyer_unit_type"],
                "buyer_unit_number"        : asale["buyer_unit_number"],
                "buyer_city"               : asale["buyer_city"],
                "buyer_state"              : asale["buyer_state"],
                "buyer_zip_code"           : asale["buyer_zip_code"],
                "buyer_zip_plus_four_code" : asale["buyer_zip_plus_four_code"],
                "lender_name"              : asale["lender_name"],
                "lender_type"              : asale["lender_type"],
                "loan_amount"              : asale["loan_amount"],
                "loan_type"                : asale["loan_type"],
                "loan_due_date"            : asale["loan_due_date"],
                "loan_finance_type"        : asale["loan_finance_type"],
                "loan_interest_rate"       : asale["loan_interest_rate"]
            }
            self.deeds.append(tempinfo)

    def initValuationInfo(self, valuation):
        self.value = valuation['value']
        self.high_value = valuation["high"]
        self.low_value = valuation["low"]
        self.forecast_stan_dev = valuation["forecast_standard_deviation"]
        self.date_of_valuation = valuation["date"]

