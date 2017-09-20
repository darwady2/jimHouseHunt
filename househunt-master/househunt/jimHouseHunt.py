from househunt import House, Listing, ZillAPI, RFAPI

"""

Testing with a house from a Zillow Park Ridge listing to see if it returns the mortgage, 
zestimate, etc.

Listing is here: https://goo.gl/zUCBh3

The get_zestimate and get_from_zillow methods need this info to work:
 - Street Address
 - Zip Code
 
Hardcoded our Zillow API code into househunt.py (X1-ZWz190v4m6e9e3_8b748). See var ZWSID around line 520. 
 
"""

#user_zip = raw_input("Please enter a 5 digit zip code to search Zillow. ") #60068 is Park Ridge Zip. Commented out for now.
user_zip = '60068'

h = House(zip_code=user_zip, street_address="1731 Manor Ln")
l = Listing(house=h)

"""
zillow = ZillAPI()
zillow_results = zillow.get_from_zillow(h)
zestimate = zillow.get_zestimate(zillow_results)
print zestimate
"""

""" How to find the region ID for Redfin:

1. Do a search for the city (ie. Chicago)
2. You'll see a URL like this: https://www.redfin.com/city/29470/IL/Chicago
3. Region code in this example is 29470

"""

def main():
    matches = []
    rf_api = RFAPI(region_ids=[29470], load_listings=True, get_zestimates=False)
    for listing in rf_api.listings:
        print listing
        if listing.house.matches_search(beds=2):
            listing.get_zestimate()
            matches.append(listing)
    #print rf_api.result_sets[0]["HOME TYPE"]
    #email_matches(matches)
    

if __name__ == '__main__':
    main()