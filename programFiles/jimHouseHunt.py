""" 
Hardcoded our Zillow API code into househunt.py (X1-ZWz190v4m6e9e3_8b748). See var ZWSID around line 520. 

How to find the region ID for Redfin:

1. Do a search for the city (ie. Chicago)
2. You'll see a URL like this: https://www.redfin.com/city/29470/IL/Chicago
3. Region code in this example is 29470

"""

#Requires househunt.py, searchresults.py, and mortgage.py in the working directory to function.
import mortgage

from househunt import House, Listing, ZillAPI, RFAPI

def email_matches(matches):
    pass

def main():
    matches = []
    rf_api = RFAPI(region_ids=[29470], load_listings=True, get_zestimates=False) #29740 is Chicago.
    
    #Below is a search for only 2 bedroom condos in the Chicagoland region, adding the monthly mortgage payment calculated from the Zestimate.
    for listing in rf_api.listings:
    	if listing.house.home_type == 'Condo/Co-op':
        	if listing.house.beds >= 2:       	#Old line: if listing.house.matches_search(beds=2):
        		listing.get_zestimate() #Gets Zestimate and RentZestimate for narrowed down list, then generates monthly mortgage payment from Zestimate.
        		try:
        			monthly_income = listing.monthly_income(rent=listing.rentzestimate, mortgage=listing.monthly_mortgage)
        			if monthly_income > 100:
        				matches.append(listing)
        		except:
        			pass
    print matches
    email_matches(matches)

    
if __name__ == '__main__':
    main()