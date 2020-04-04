from Suburb import Suburb
from Property import Property
import json
import requests

SUBURBS = ["Kellyville","Baulkham Hills"]
PROPERTY_TYPES = ["Townhouse", "House"]


def main():

	suburbObjList = []

	for s in SUBURBS:
		suburbObjList.append(Suburb(s))


		

if __name__ == "__main__":
	main()
