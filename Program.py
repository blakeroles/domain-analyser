# Import all required classes / libraries
from DomainCredentials import DomainCredentials
from SuburbStatisticCaller import SuburbStatisticCaller
from SuburbPerfData import SuburbPerfData
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Program parameters
SUBURBS = []
STATE = "NSW"
DOMAIN_CREDENTIALS_FILENAME = "api_info.secret"
JSON_CONFIG_FILENAME = "config.json"
JSON_DATA_FILENAME = "data.json"
suburb_id_dict = {}
api_scopes = "api_addresslocators_read api_suburbperformance_read api_locations_read"

# Program parameters for Suburb Performance Statistics
property_category = "house"
chronological_span = 3
t_plus_from = 1
t_plus_to = 24
bedrooms = 3 # Get all bedroom types if None

def read_suburbs_from_json_file(JSON_CONFIG_FILENAME):
	with open(JSON_CONFIG_FILENAME) as f:
		data = json.load(f)

	# Populate suburbs variable
	for d in data["Suburbs"]:
		SUBURBS.append(d["Name"])


def get_domain_credentials():
	with open(DOMAIN_CREDENTIALS_FILENAME) as f:
		data = json.load(f)

	dc = DomainCredentials(data["api_info"]["client_id"], data["api_info"]["client_secret"])

	return dc

def get_auth_token(dc):
	response = requests.post('https://auth.domain.com.au/v1/connect/token', data = {'client_id':dc.client_id,"client_secret":dc.client_secret,"grant_type":"client_credentials","scope":api_scopes,"Content-Type":"text/json"})
	token=response.json()
	return token["access_token"]

def send_request(access_token, url):
	auth = {"Authorization":"Bearer "+access_token}
	request = requests.get(url,headers=auth)
	r=request.json()
	return r

def get_suburb_ids(access_token):
	for s in SUBURBS:
		url = "https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb="+s+"&state=NSW"
		r = send_request(access_token, url)

		try:
			suburb_id_dict[s] = r[0]["ids"][0]["id"]
		except:
			print(s + " does not exist in Domain!")
		

def plot_median_values(suburb_perf_data_list):
	months = []
	years = []
	dates = []
	median_sold_prices = []
	suburb_name = ""
	for s in suburb_perf_data_list:
		months.append(s.month)
		years.append(s.year)
		dates.append(str(s.month) + '-' + str(s.year))
		median_sold_prices.append(s.median_sold_price)
		suburb_name = s.suburb_name

	plt.figure(figsize=(20, 4))
	plt.plot(dates, median_sold_prices)
	plt.xlabel("Month and Year")
	plt.ylabel("Median Sold Price ($)")
	plt.title(suburb_name + " Median Sold Price")
	plt.grid()
	plt.savefig("./Figures/Quarterly_Median_Sold_Prices/" + suburb_name + "_Median_Sold_Price.png")


def get_suburb_performance_statistics(suburb_id_dict, access_token):
	for skey in suburb_id_dict:
		suburb_perf_data_list = []
		ssc = SuburbStatisticCaller(STATE, suburb_id_dict[skey], property_category, chronological_span, t_plus_from, t_plus_to, bedrooms)
		
		if (bedrooms is None):
			url = "https://api.domain.com.au/v1/suburbPerformanceStatistics?state="+ssc.state+"&suburbId="+str(ssc.suburb_id)+"&PropertyCategory="+ssc.property_category+"&chronologicalSpan="+str(ssc.chronological_span)+"&tPlusFrom="+str(ssc.t_plus_from)+"&tPlusTo="+str(ssc.t_plus_to)
		else:
			url = "https://api.domain.com.au/v1/suburbPerformanceStatistics?state="+ssc.state+"&suburbId="+str(ssc.suburb_id)+"&PropertyCategory="+ssc.property_category+"&chronologicalSpan="+str(ssc.chronological_span)+"&tPlusFrom="+str(ssc.t_plus_from)+"&tPlusTo="+str(ssc.t_plus_to)+"&bedrooms="+str(ssc.bedrooms)
		
		r = send_request(access_token, url)
		for data in r["series"]["seriesInfo"]:
			suburb_perf_data_list.append(SuburbPerfData(suburb_id_dict[skey], skey, data["month"], data["year"], data["values"]["lowestSoldPrice"], data["values"]["highestSoldPrice"], data["values"]["medianSoldPrice"]))

		plot_median_values(suburb_perf_data_list)
			
def get_suburb_location_profiles(suburb_id_dict, access_token):
	for skey in suburb_id_dict:
		url = "https://api.domain.com.au/v1/locations/profiles/" + str(suburb_id_dict[skey])
		r = send_request(access_token, url)

def get_daily_suburb_information(suburb_id_dict, access_token):
	# Read in the data.json file first
	try:
		with open(JSON_DATA_FILENAME) as json_file:
			data = json.load(json_file)

		
	except:
		print("JSON File is empty - appending to file for the first time")
		get_daily_domain_suburb_information(suburb_id_dict, access_token)

def get_daily_domain_suburb_information(suburb_id_dict, access_token):
	# Get the date time object for use in the json file
	current_date = datetime.datetime.now()
	data = {}
	prop_cat = {}
	# Each entry will be in its own datetime
	current_date_for_json = str(current_date.day)+"-"+str(current_date.month)+"-"+str(current_date.year)+":"+str(current_date.hour)+"-"+str(current_date.minute)+"-"+str(current_date.second)
	data[current_date_for_json] = []
	for skey in suburb_id_dict:
		url = "https://api.domain.com.au/v1/locations/profiles/" + str(suburb_id_dict[skey])
		r = send_request(access_token, url)


		prop_cat['PropertyCategory'] = 'House'
		prop_cat['Bedrooms'] = 3
		
		data[current_date_for_json].append({
			'Suburb': skey,
			'PropertyCategories' : prop_cat
		})


		#data['PropertyCategories'] = prop_cat


		df = open(JSON_DATA_FILENAME, 'w')
		df.write(json.dumps(data, indent=4, sort_keys=True))
		df.close()




def test_json():
	data = {}
	data['people'] = []
	data['people'].append({
	    'name': { 'dob' : 'test', 'age' : '24'},
	    'website': 'stackabuse.com',
	    'from': 'Nebraska'
	})
	data['people'].append({
	    'name': { 'dob' : 'test', 'age' : '24'},
	    'website': 'google.com',
	    'from': 'Michigan'
	})
	data['people'].append({
	    'name': { 'dob' : 'test', 'age' : '24'},
	    'website': 'apple.com',
	    'from': 'Alabama'
	})

	#dataFile = open()
	#with open('data.txt', 'w') as outfile:
	#    json.dump(data, indent=4, sort_keys=True, outfile)	


def main():

	# Populate variables from config.json
	read_suburbs_from_json_file(JSON_CONFIG_FILENAME)

	# Get your domain credentials
	dc = get_domain_credentials()

	# Get your auth token from Domain
	access_token = get_auth_token(dc)

	# Get all the Suburb IDs from SUBURBS list and store in a dictionary for later use
	get_suburb_ids(access_token)

	# For each suburb in suburb_id_dict, get the property statistics	
	get_suburb_performance_statistics(suburb_id_dict, access_token)

	# For each suburb in suburb_id_dict, get the location profiles
	get_suburb_location_profiles(suburb_id_dict, access_token)

	# For each suburb, get daily information and store to a json file
	get_daily_suburb_information(suburb_id_dict, access_token)

	#test_json()

if __name__ == "__main__":
	main()
