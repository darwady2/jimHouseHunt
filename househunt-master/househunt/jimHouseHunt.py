from househunt import House, Listing

"""

Testing with a house from a Zillow Park Ridge listing to see if it returns the mortgage, 
zestimate, etc.

Listing is here: https://goo.gl/zUCBh3

The get_zestimate and get_from_zillow methods need this info to work:
 - Street Address
 - Zip Code
 
Hardcoded our Zillow API code into househunt.py (X1-ZWz190v4m6e9e3_8b748). See var ZWSID around line 520. 
 
"""

h = House(street_address="1731 Manor Ln", city="Park Ridge", state="Illinois", zip_code="60068")
l = Listing(house=h)

#Return the Z-Estimate for the given listing.
l.get_zestimate()

zestimate = l.zestimate

print zestimate