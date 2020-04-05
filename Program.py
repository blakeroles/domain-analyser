from Suburb import Suburb
from Property import Property
from DomainCredentials import DomainCredentials
import json
import requests

SUBURBS = ["Kellyville","Baulkham Hills"]
PROPERTY_TYPES = ["Townhouse", "House"]
DOMAIN_CREDENTIALS_FILENAME = "api_info.secret"

def get_domain_credentials():
	with open(DOMAIN_CREDENTIALS_FILENAME) as f:
		data = json.load(f)

	dc = DomainCredentials(data["api_info"]["client_id"], data["api_info"]["client_secret"])

	return dc

def main():

	# Get your domain credentials
	dc = get_domain_credentials()


	suburb_obj_list = []

	for s in SUBURBS:
		suburb_obj_list.append(Suburb(s))


	# TESTING POST GET functionality
	# POST request for token
	response = requests.post('https://auth.domain.com.au/v1/connect/token', data = {'client_id':dc.client_id,"client_secret":dc.client_secret,"grant_type":"client_credentials","scope":"api_listings_read","Content-Type":"text/json"})
	token=response.json()
	access_token=token["access_token"]

	url = "https://api.domain.com.au/v1/addressLocators?searchLevel=Address&streetNumber=100&streetName=Harris&streetType=Street&suburb=Pyrmont&state=NSW&postcode=2009"
	auth = {"Authorization":"Bearer "+access_token}
	request = requests.get(url,headers=auth)
	r=request.json()
	print(r)

if __name__ == "__main__":
	main()
