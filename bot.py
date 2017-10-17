import tweepy
import json
import linecache
import string
import requests
import random
import datetime
import gzip
import shutil

import forecastio

from tweepy.streaming import StreamListener

from secrets import *


#  SET KEYS AND TOKENS #
auth = tweepy.OAuthHandler('C_KEY', 'C_SECRET')  #added os.environ to hopefully read the config vars as added on heroku but not tested
auth.set_access_token('A_TOKEN', 'A_TOKEN_SECRET')  
api = tweepy.API('auth')



# EXTRACT INFORMATION FROM WORLDCITIESPOP.TXT #
randomnum = random.randrange(2, 3173959, 1) 

line = linecache.getline("worldcitiespop.txt", randomnum)
print line

line = line.replace("\n", "")

cityarr = string.split(line, ",")

city = cityarr[2]
latitude = cityarr[5]
longitude = cityarr[6]

country = cityarr[0]



# BUILD URL AND GET JSON INFO FROM DARK SKY #
url = "https://api.darksky.net/forecast/" + forecastio_api_key + "/" + latitude + "," + longitude + "?units=uk2"

weather = requests.get(url).json()



# CONVERT ISO CODES TO COUNTRY NAMES #
countrynames_json = open("names.json").read()

countrynames = json.loads(countrynames_json)

iso = country.upper()

isoconversion = countrynames.get(iso)



# CONVERT UNIX TIMESTAMP TO HUMAN READABLE TIME #
timestamp = weather["currently"]["time"]

value = datetime.datetime.fromtimestamp(timestamp)

time = (value.strftime('%I:%M%p'))



# CONVERT ICON DATA POINT TO EMOJI #
iconinfo = {
	"clear-day" : u"\u2600", 
	"clear-night" : u"\U0001F303", 
	"rain" : u"\u2614",
	"snow" : u"\u2744", 
	"sleet" : u"\u2744", 
	"wind" : u"\U0001F343", 
	"fog" : u"\U0001F301", 
	"cloudy" : u"\u2601", 
	"partly-cloudy-day" : u"\u26C5", 
	"partly-cloudy-night" : u"\u26C5" 
}

weatheremoji = iconinfo.get(weather["currently"]["icon"])

if weatheremoji == None:
 weatheremoji = u"\u2600"



# CONVERT TEMP FROM FAHRENHEIT TO CELSIUS #
celtemp = int(round(weather["currently"]["temperature"]))

fahrtemp = int(round((celtemp * 1.8) + 32))



# WRITE TWEET AND SUBMIT TO TWITTER ACCOUNT #
tweet = city + ", " + isoconversion + " " + time + ": " + weather["currently"]["summary"] + " " + str(fahrtemp) + u"°F" + "/" + str(celtemp) + u"°C" + " " + weatheremoji #the u prefix allows unicode symbol

print tweet

api.update_status(status=tweet)






