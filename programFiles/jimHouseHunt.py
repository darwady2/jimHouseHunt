""" 
Create a Gmail Account and a Zillow API Key, then set your envars by running the following commands in Terminal:
export GMAIL_EMAIL='gmail@gmail.com'
export GMAIL_PASSWORD='xxxxxxxx'
export ZILLOW_API_KEY='yyyyyyyyy'


How to find the region ID for Redfin:

1. Do a search for the city (ie. Chicago)
2. You'll see a URL like this: https://www.redfin.com/city/29470/IL/Chicago
3. Region code in this example is 29470


To adjust the number of homes scanned, go to 'househunt.py', line 675 ('num_homes') and set the number there. It's currently set at '10' but should probably be around 500 or so to get a meaningful search.

Create a Gmail Account and set your envars by running the following commands in Terminal:
export GMAIL_EMAIL='gmail@gmail.com'
export GMAIL_PASSWORD='xxxxxxxx'
export ZILLOW_API_KEY='yyyyyyyyy'

Fill out the email list and other customizations in the main function, lines 71 onward.

"""

#Requires househunt.py, searchresults.py, and mortgage.py in the working directory to function.
import mortgage

from househunt import House, Listing, ZillAPI, RFAPI

import os
import smtplib

from email.mime.text import MIMEText



def email_matches(matches):
	
	body = ''
	for index, listing in enumerate(matches):
		number = index + 1
		body += str(number) + ":\n" + str(listing) + "\n\n"
		
	#Set your email list here
	email_list = ['email1@gmail.com', 'email2@gmail.com']	

	fromaddr = os.environ.get('GMAIL_EMAIL')
	password = os.environ.get('GMAIL_PASSWORD')

	message = MIMEText(body)
	message['Subject'] = 'Daily HouseHunt Email'
	message['From'] = fromaddr
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(fromaddr, password)

	for toaddrs in email_list:
		response = server.sendmail(fromaddr, toaddrs, message.as_string())
		#print response
	
	server.quit()


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
    home_type = 'Condo/Co-op'  #Not being used, so we can see all home types. Uncomment line 73 if you want to use it. Available types: 'Single Family Residential'; 'Condo/Co-op'; 'Townhouse'
    
    #Set your income threshold here; for example, 100 will return homes calculated to make at least $100 per month in net income.
    threshold = 50
    
    #Below is the script to generate the listings.
    
    rf_api = RFAPI(region_ids=regions, load_listings=True, get_zestimates=False) 
    
    for index, listing in enumerate(rf_api.listings):
    	#if listing.house.home_type == home_type:
        	if listing.house.beds >= beds:
        		listing.get_zestimate()   #Gets Zestimate and RentZestimate for narrowed down list.
        		listing.get_monthly_mortgage(property_tax_rate = property_tax_rate, months = months, interest = interest, amount = listing.zestimate)
        		print 'Getting Listing #' + str(index + 1)
        		try:
        			monthly_income = listing.monthly_income(rent = listing.rentzestimate, mortgage = listing.monthly_mortgage)
        			if monthly_income > threshold:
        				matches.append(listing)
        		except:
        			pass
    #print matches
    email_matches(matches)

    
if __name__ == '__main__':
    main()
