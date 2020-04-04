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


		

if __name__ == "__main__":
	main()
