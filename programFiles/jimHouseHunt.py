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
import gspread
from email.mime.text import MIMEText
from oauth2client.service_account import ServiceAccountCredentials
 

#Emails the matches to a list of users.
def email_matches(email_matches):
	
	body = ''
	for index, listing in enumerate(email_matches):
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
	
	print '\nEmailed results.'


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
		format.append(h.rentzestimate - h.monthly_mortgage)
		format.append(h.listing_url)
		entries.append(format)
		format = []	
	return entries


#Authorizes and opens the Google Sheet where the entries will be stored.
def open_sheet(sheet_name):
	# Use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	sheet = client.open(sheet_name).sheet1
	clear_sheet(sheet)
	return sheet


#Clears the Google Sheet.
def clear_sheet(sheet):
	r = sheet.row_count
	cell_list = sheet.range('A1:G' + str(r))
	for cell in cell_list:
		cell.value = ""
	sheet.update_cells(cell_list)
	

#Adds the titles to the Google Sheet.
def add_titles(sheet):
	titles = ['Address','List Price','Zestimate','Monthly Mortgage','Monthly Rent Estimate','Monthly income','Listing URL']
	cell_list = sheet.range('A1:G1')
	for i, cell in enumerate(cell_list):
		cell.value = titles[i]
	sheet.update_cells(cell_list)


#Creates a range for inserting the matches into the Google Sheet.
def range_creator(i):
	range = 'A' + str(i + 2) + ':G' + str(i + 2)
	return range


#Inserts the matches to the Google Sheet.
def insert_matches(sheet, entries):
	for i, entry in enumerate(entries):
		cellRange = range_creator(i)
		cell_list = sheet.range(cellRange)
		
		for j, cell in enumerate(cell_list):
			cell.value = entry[j]
			
		sheet.update_cells(cell_list) 
		
	
#Iterates through each home and places it in a row in sheets.
def matches_to_sheets(matches):
	entries = matches_to_list(matches)
	sheet = open_sheet('Testing House Entry Sheet')
	add_titles(sheet)
	insert_matches(sheet = sheet, entries = entries)
	print '\nAdded to Sheets.'


#Main program.
def main():

	sheet_match_list = []
	email_match_list = []
	
	#Put region IDs for all regions to search in this list.
	regions = [29470] #29740 is Chicago. See top comments to add additional region IDs.
	
	#Set mortgage calculation details here.
	property_tax_rate = 0.0344 # 3.44% tax rate, median for Cook County.
	months = 360 # 30 year mortgage.
	interest = 0.04 # 4% rate.
	
	#Set property filters here.
	beds = 2  #Filters for at least 2 bedroom properties.
	home_type = 'Condo/Co-op'  #Not being used, so we can see all home types. Uncomment line 73 if you want to use it. Available types: 'Single Family Residential'; 'Condo/Co-op'; 'Townhouse'
	
	#Set your income thresholds here; for example, 100 will return homes calculated to make at least $100 per month in net income. 
	sheet_threshold = 100 #This is how much income it would need to get populated to the Google Sheet.
	email_threshold = 500 #This is how much income it would need to get sent in an email.
	
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
					if monthly_income > email_threshold:
						email_match_list.append(listing)
					if monthly_income > sheet_threshold:
						sheet_match_list.append(listing)
				except:
					pass

	email_matches(email_match_list)
	matches_to_sheets(sheet_match_list)
	

if __name__ == '__main__':
	main()
