Requires househunt.py, searchresults.py, and mortgage.py in the working directory to function.

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
