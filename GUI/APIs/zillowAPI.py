
import zillow
import pprint
from geopy.distance import geodesic

class ZillowAPI:
	def __init__(self, apikey, ad, city, state, zipcode, COMPNUMBER=25):
		self.compnum = COMPNUMBER
		api = zillow.ValuationApi() # initialize api
		address = ad + "," + city + "," + state
		postal_code = str(zipcode)
		self.data = api.GetDeepSearchResults(apikey, address, postal_code).get_dict() # basic data retrieved from address
		self.city = self.data['full_address']['city']
		self.state = self.data['full_address']['state']
		self.region = self.data['local_realestate']['region_name']
		self.regionType = self.data['local_realestate']['region_type']
		self.homeType = self.data['extended_data']['usecode']
		self.zpid = self.data['zpid'] # home identifier assigned by zillow, needed for other api calls
		self.zestimate_data = api.GetZEstimate(apikey, self.zpid).get_dict() # retrieves zestimate details
		self.comps_data = api.GetDeepComps(apikey, self.zpid, count=COMPNUMBER)['comps'] # returns comps in the form of a dict
		self.pp = pprint.PrettyPrinter(indent=4)
		self.comps = []
		self.upper_val = None
		self.lower_val = None
		self.price = None
		self.comp_mean_weighted_sim = None
		self.comp_mean_weighted_dist = None
		self.comp_mean_weighted_sim_low = None
		self.comp_mean_weighted_dist_low = None
		self.comp_mean_weighted_sim_high = None
		self.comp_mean_weighted_dist_high = None
		self.comp_change_mean_weighted_sim = None
		self.comp_change_mean_weighted_dist = None
		self.change_30_days = None

	def printSearchResults(self):
		self.pp.pprint(self.data)

	def printCompsResults(self):
		self.pp.pprint(self.data)

	def initComps(self):
		for comp in self.comps_data:
			comp_dict = comp.get_dict()
			comp_coords = (float(comp_dict['full_address']['latitude']), float(comp_dict['full_address']['longitude']))
			cur_home_coords = (float(self.data['full_address']['latitude']), float(self.data['full_address']['longitude']))
			dist = geodesic(comp_coords, cur_home_coords).miles
			sim_score = float(comp_dict['similarity_score'])
			price = comp_dict['zestimate']['amount']
			if price is not None:
				price = float(price)
			else:
				price = 0
			upper_price = comp_dict['zestimate']['valuation_range_high']
			if upper_price is not None:
				upper_price = float(upper_price)
			else:
				upper_price = 0
			lower_price = comp_dict['zestimate']['valuation_range_low']
			if lower_price is not None:
				lower_price = float(lower_price)
			else:
				lower_price = 0
			change_30_days = comp_dict['zestimate']['amount_change_30days']
			if change_30_days is not None:
				change_30_days = float(change_30_days)
			else:
				change_30_days = 0
			comp_details = {'sim_score' : sim_score, 'dist' : dist, 'price' : price, 'upper_price' : upper_price , 'lower_price' : lower_price, "change" : change_30_days}
			self.comps.append(comp_details)

	def compsAnalysis(self):
		if self.comps == []:
			print('Must call initComps before analyzing')
			return -1
		tot_sim = 0
		tot_dist = 0
		tot_price_sim = 0
		tot_price_dist = 0
		tot_low_sim = 0
		tot_low_dist = 0
		tot_high_sim = 0
		tot_high_dist = 0
		tot_change_sim = 0
		tot_change_dist = 0
		for comp in self.comps:
			tot_sim = comp['sim_score'] + tot_sim
			tot_dist = comp['dist'] + tot_dist
			tot_price_sim = comp['price'] * comp['sim_score'] + tot_price_sim
			tot_price_dist = comp['price'] * comp['dist'] + tot_price_dist
			tot_low_sim = comp['lower_price'] * comp['sim_score'] + tot_low_sim
			tot_low_dist = comp['lower_price'] * comp['dist'] + tot_low_dist
			tot_high_sim = comp['upper_price'] * comp['sim_score'] + tot_high_sim
			tot_high_dist = comp['upper_price'] * comp['dist'] + tot_high_dist
			tot_change_sim = comp['change'] * comp['sim_score'] + tot_change_sim
			tot_change_dist = comp['change'] * comp['dist'] + tot_change_dist

		self.comp_change_mean_weighted_sim = round(tot_change_sim/(tot_sim),2)
		self.comp_change_mean_weighted_dist = round(tot_change_dist / (tot_dist) ,2)
		self.comp_mean_weighted_sim = round(tot_price_sim/(tot_sim), 2)
		self.comp_mean_weighted_dist = round(tot_price_dist / (tot_dist), 2)
		self.comp_mean_weighted_sim_low = round(tot_low_sim/(tot_sim), 2)
		self.comp_mean_weighted_dist_low = round(tot_low_dist/(tot_dist), 2)
		self.comp_mean_weighted_sim_high = round(tot_high_sim / (tot_sim), 2)
		self.comp_mean_weighted_dist_high = round(tot_high_dist / (tot_dist), 2)

	def initZestimate(self):
		self.upper_val = round(self.data['zestimate']['valuation_range_high'], 2)
		self.lower_val = round(self.data['zestimate']['valuation_range_low'], 2)
		self.price = round(self.data['zestimate']['amount'], 2)
		self.change_30_days = round(self.data['zestimate']['amount_change_30days'], 2)

if __name__=="__main__":
	it = ZillowAPI("X1-ZWz17njsl1wx6z_3mmvk", "1280 Ithaca dr", "Boulder", "CO", "80305", COMPNUMBER=5)
	it.initZestimate()
	it.initComps()
	it.compsAnalysis()
	print(it.comps)






