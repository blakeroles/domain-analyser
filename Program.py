from Suburb import Suburb
from Property import Property
from DomainCredentials import DomainCredentials
from SuburbStatisticCaller import SuburbStatisticCaller
import json
import requests

# Program parameters
SUBURBS = ["Kellyville"]
STATE = "NSW"
PROPERTY_TYPES = ["Townhouse", "House"]
DOMAIN_CREDENTIALS_FILENAME = "api_info.secret"
suburb_id_dict = {}
api_scopes = "api_addresslocators_read api_suburbperformance_read"

# Program parameters for Suburb Performance Statistics
property_category = "house"
chronological_span = 12
t_plus_from = 1
t_plus_to = 4
bedrooms = None # Get all bedroom types if None

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
		suburb_id_dict[s] = r[0]["ids"][0]["id"]

def get_suburb_performance_statistics(suburb_id_dict, access_token):
	for sid in suburb_id_dict.values():
		ssc = SuburbStatisticCaller(STATE, sid, property_category, chronological_span, t_plus_from, t_plus_to, bedrooms)
		
		if (bedrooms is None):
			url = "https://api.domain.com.au/v1/suburbPerformanceStatistics?state="+ssc.state+"&suburbId="+str(ssc.suburb_id)+"&PropertyCategory="+ssc.property_category+"&chronologicalSpan="+str(ssc.chronological_span)+"&tPlusFrom="+str(ssc.t_plus_from)+"&tPlusTo="+str(ssc.t_plus_to)
		else:
			url = "https://api.domain.com.au/v1/suburbPerformanceStatistics?state="+ssc.state+"&suburbId="+str(ssc.suburb_id)+"&PropertyCategory="+ssc.property_category+"&chronologicalSpan="+str(ssc.chronological_span)+"&tPlusFrom="+str(ssc.t_plus_from)+"&tPlusTo="+str(ssc.t_plus_to)+"&bedrooms="+str(ssc.bedrooms)
		
		r = send_request(access_token, url)
		print(r)



def main():

	# Get your domain credentials
	dc = get_domain_credentials()

	# Get your auth token from Domain
	access_token = get_auth_token(dc)

	# Get all the Suburb IDs from SUBURBS list and store in a dictionary for later use
	get_suburb_ids(access_token)

	# For each suburb in surburb_id_dict, get the property statistics	
	get_suburb_performance_statistics(suburb_id_dict, access_token)



	#print(suburb_id_dict)





	suburb_obj_list = []

	for s in SUBURBS:
		suburb_obj_list.append(Suburb(s))




if __name__ == "__main__":
	main()
