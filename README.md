A simple program that scans Zillow and Redfin and returns results that will have an estimated net monthly income of a value, which you can set.

Instructions for use:

1. Make sure that househunt.py, searchresults.py, and mortgage.py are all in the working directory.

2. Create a Gmail Account and a Zillow API Key

3. Set your envars by running the following commands in Terminal (you'll need to do this each time you run the script):

export GMAIL_EMAIL='gmail@gmail.com'

export GMAIL_PASSWORD='xxxxxxxx'

export ZILLOW_API_KEY='yyyyyyyyy'

4. Fill out the email list, where you want the results, in line 46.

5. Set your other customizations in the main function, lines 71 onward.

6. Run the script.


#NOTES:

How to find the region ID for Redfin:

1. Do a search for the city (ie. Chicago)
2. You'll see a URL like this: https://www.redfin.com/city/29470/IL/Chicago
3. Region code in this example is 29470

To adjust the number of homes scanned, go to 'househunt.py', line 675 ('num_homes') and set the number there.
