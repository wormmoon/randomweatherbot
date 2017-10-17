# -*- coding: utf-8 -*-

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

#print C_KEY
#print C_SECRET
#print A_TOKEN
#print A_TOKEN_SECRET

#Set keys and tokens
auth = tweepy.OAuthHandler('C_KEY', 'C_SECRET')  #added os.environ to hopefully read the config vars as added on heroku but not tested
auth.set_access_token('A_TOKEN', 'A_TOKEN_SECRET')  
api = tweepy.API('auth')




# Extract information from world cities data file
randomnum = random.randrange(2, 3173959, 1) 

line = linecache.getline("worldcitiespop.txt", randomnum)
print line

line = line.replace("\n", "")

cityarr = string.split(line, ",")

city = cityarr[2]
latitude = cityarr[5]
longitude = cityarr[6]

country = cityarr[0]


# Get random country from Tim's server 
# randomcountry = requests.get("https://x35.me/api/randomcountry").json()

# city = randomcountry["data"]["AccentCity"]
# latitude = randomcountry["data"]["Latitude"]
# longitude = randomcountry["data"]["Longitude"]






# Build URL and get json information from forcastio
url = "https://api.darksky.net/forecast/" + forecastio_api_key + "/" + latitude + "," + longitude + "?units=uk2"

#print url

weather = requests.get(url).json()

#print weather






# Convert iso codes to country names
countrynames_json = open("names.json").read()

countrynames = json.loads(countrynames_json)

iso = country.upper()

isoconversion = countrynames.get(iso)

print (isoconversion)




# Convert UNIX timestamp to human readable time
timestamp = weather["currently"]["time"]

value = datetime.datetime.fromtimestamp(timestamp)

time = (value.strftime('%I:%M%p'))





# Convert icon data point to emojis
# 'summary' has millions of possible values so icon is best to use if using emojis in tweets
iconinfo = {
	"clear-day" : u"\u2600", #U+2600	\xE2\x98\x80
	"clear-night" : u"\U0001F303", #U+1F303	\xF0\x9F\x8C\x83 longer unicodes need fixing
	"rain" : u"\u2614", #U+2614	\xE2\x98\x94
	"snow" : u"\u2744", #U+2744	\xE2\x9D\x84
	"sleet" : u"\u2744", #U+2744	\xE2\x9D\x84
	"wind" : u"\U0001F343", #U+1F343	\xF0\x9F\x8D\x83
	"fog" : u"\U0001F301", #	U+1F301	\xF0\x9F\x8C\x81
	"cloudy" : u"\u2601", #U+2601	\xE2\x98\x81
	"partly-cloudy-day" : u"\u26C5", #U+26C5	\xE2\x9B\x85
	"partly-cloudy-night" : u"\u26C5" #U+26C5	\xE2\x9B\x85
}

weatheremoji = iconinfo.get(weather["currently"]["icon"])

if weatheremoji == None:
 weatheremoji = u"\u2600" #U+2600	\xE2\x98\x80





# Convert temp from fahrenheit to celsius
celtemp = int(round(weather["currently"]["temperature"]))

fahrtemp = int(round((celtemp * 1.8) + 32))

print (fahrtemp)
print (celtemp)






# Write and submit tweet to twitter account
tweet = city + ", " + isoconversion + " " + time + ": " + weather["currently"]["summary"] + " " + str(fahrtemp) + u"°F" + "/" + str(celtemp) + u"°C" + " " + weatheremoji #the u prefix allows unicode symbol

print tweet

api.update_status(status=tweet)


# HEROKU::::::::::
#git push heroku master gives error 'failed to push some refs to git@heroku.com:randomweatherbot.git' - have added buildpack - also fatal:sha1 file '<stdout>' write error: Broken pipe and fatal: The remote end hung up unexpectedly



