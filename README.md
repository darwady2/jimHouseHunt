This is a simple program that scans Zillow and Redfin and returns results that will have an estimated net monthly income of a value, which you can set.

Instructions for use:

1. Make sure that househunt.py, searchresults.py, and mortgage.py are all in the working directory.

2. Create a Gmail Account and a Zillow API Key. You'll also need to enable gspread and get your own client_secret credentials (instructions on how to do that are in this article: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html).

3. Once you have your own client_secret.json file, update the path in line 101 to reflect where you put that file on your local machine.

4. Set your envars by running the following commands in Terminal (you'll need to do this each time you run the script):

export GMAIL_EMAIL='fromemail@gmail.com'
export GMAIL_PASSWORD='password'
export TO_EMAIL_1='toemail1@gmail.com’
export TO_EMAIL_2='toemail2@gmail.com’

5. Set any other customizations in the main function, lines 71 onward.

6. Run the script.


#NOTES:

How to find the region ID for Redfin:

1. Do a search for the city (ie. Chicago)
2. You'll see a URL like this: https://www.redfin.com/city/29470/IL/Chicago
3. Region code in this example is 29470

To adjust the number of homes scanned, go to 'househunt.py', line 675 ('num_homes') and set the number there.
