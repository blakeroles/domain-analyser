from Suburb import Suburb
from Property import Property
import json
import requests

SUBURBS = ["Kellyville","Baulkham Hills"]
PROPERTY_TYPES = ["Townhouse", "House"]
DOMAIN_CREDENTIALS_FILENAME = "api_info.secret"

def get_domain_credentials():
	



def main():

	suburb_obj_list = []

	for s in SUBURBS:
		suburb_obj_list.append(Suburb(s))


		

if __name__ == "__main__":
	main()
