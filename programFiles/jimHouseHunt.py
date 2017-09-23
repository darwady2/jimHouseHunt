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

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *





def email_matches(matches):
	
	body = ''
	for index, listing in enumerate(matches):
		number = index + 1
		body += str(number) + ":\n" + str(listing) + "\n\n"
		print body
	
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	from_email = Email("darwady2@gmail.com")
	to_emails_list = ["jskuros@gmail.com", "darwady2@gmail.com", "dave.bremner2@gmail.com"]
	
	for email in to_emails_list:
		to_email = Email(email)
		subject = "Your Daily House Hunt Digest"
		content = Content("text/plain", body)
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)


def main():

    matches = []
    
    #Put region IDs for all regions to search in this list.
    regions = [29470] #29740 is Chicago. See top comments to add additional region IDs.
    
    #Set mortgage calculation details here.
    property_tax_rate = 0.0344 # 3.44% tax rate, median for Cook County.
    months = 360 # 30 year mortgage.
    interest = 0.04 # 4% rate.
    
    #Set property filters here.
    beds = 2  #Filters for at least 2 bedroom properties.
    home_type = 'Condo/Co-op'  #Available types: 'Single Family Residential'; 'Condo/Co-op'; 'Townhouse'
    
    #Set your income threshold here; for example, 100 will return homes calculated to make at least $100 per month in net income.
    threshold = 100
    
    #Below is the script to generate the listings.
    
    rf_api = RFAPI(region_ids=regions, load_listings=True, get_zestimates=False) 
    
    for listing in rf_api.listings:
    	if listing.house.home_type == home_type:
        	if listing.house.beds >= beds:
        		listing.get_zestimate()   #Gets Zestimate and RentZestimate for narrowed down list.
        		listing.get_monthly_mortgage(property_tax_rate = property_tax_rate, months = months, interest = interest, amount = listing.zestimate)
        		try:
        			monthly_income = listing.monthly_income(rent = listing.rentzestimate, mortgage = listing.monthly_mortgage)
        			if monthly_income > threshold:
        				matches.append(listing)
        		except:
        			pass
    print matches
    email_matches(matches)

    
if __name__ == '__main__':
    main()