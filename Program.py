from Suburb import Suburb
from Property import Property
from DomainCredentials import DomainCredentials
import json
import requests

SUBURBS = ["Kellyville"]
PROPERTY_TYPES = ["Townhouse", "House"]
DOMAIN_CREDENTIALS_FILENAME = "api_info.secret"
suburb_id_dict = {}
api_scopes = "api_addresslocators_read"

def get_domain_credentials():
	with open(DOMAIN_CREDENTIALS_FILENAME) as f:
		data = json.load(f)

	dc = DomainCredentials(data["api_info"]["client_id"], data["api_info"]["client_secret"])

	return dc

def get_auth_token(dc):
	response = requests.post('https://auth.domain.com.au/v1/connect/token', data = {'client_id':dc.client_id,"client_secret":dc.client_secret,"grant_type":"client_credentials","scope":api_scopes,"Content-Type":"text/json"})
	token=response.json()
	return token["access_token"]

def main():

	# Get your domain credentials
	dc = get_domain_credentials()

	# Get your auth token from Domain
	access_token = get_auth_token(dc)

	# Get all the Suburb IDs from SUBURBS list and store in a dictionary for later use
	for s in SUBURBS:
		url = "https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb="+s+"&state=NSW"
		auth = {"Authorization":"Bearer "+access_token}
		request = requests.get(url,headers=auth)
		r=request.json()
		suburb_id_dict[s] = r[0]["ids"][0]["id"]

	print(suburb_id_dict)



	suburb_obj_list = []

	for s in SUBURBS:
		suburb_obj_list.append(Suburb(s))




if __name__ == "__main__":
	main()
