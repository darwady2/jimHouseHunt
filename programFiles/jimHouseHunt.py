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
import httplib2
import smtplib

from email.mime.text import MIMEText

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'jimHouseHunt'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def email_matches(matches):
	
	body = ''
	for index, listing in enumerate(matches):
		number = index + 1
		body += str(number) + ":\n" + str(listing) + "\n\n"
		
	#Set your email list here
	email_list = ['darwady2@gmail.com', 'jskuros@gmail.com']	

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



#Creates a list of lists, with each entry as a home and each subentry with the home's details.
def matches_to_list(matches):
	
	entries = []
	format = []
	
	for index, h in enumerate(matches):
		format.append(h.house)
		format.append(h.list_price)
		format.append(h.zestimate)
		format.append(h.monthly_mortgage)
		format.append(h.rentzestimate)
		format.append(h.listing_url)
		entries.append(format)
		format = []	
	
	return entries


def authorize_sheets():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	return service


#Iterates through each home and places it in a row in sheets.
def matches_to_sheets(matches):
	

	service = authorize_sheets()
	spreadsheetId = '1Ne-S5Nuzu5NrxoZV6S9ejf5oN3OU4fdadDn6oObeMAo' #Testing House Hunt Spreadsheet, Dan's Google Drive.
	entries = matches_to_list(matches)
	rangeName = 'Sheet1'
	value = entries[0][0]
	value_range_body = {"range":rangeName,"values":entries}
	result = service.spreadsheets().values().append(
		spreadsheetId = spreadsheetId, range = rangeName, body=value_range_body).execute()
	
	
	  
	"""
    rangeName = 'Class Data!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
	"""


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
    threshold = -10000
    
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
    matches_to_sheets(matches)
    #email_matches(matches)

    
if __name__ == '__main__':
    main()
