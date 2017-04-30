import tweepy
import json

from secrets import *

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth) 

import forecastio
api_key = "73670634fd8f73e49b11ba3497c4f12d" #put this in secrets
# Forecastio documentation says it requires long and lat info as well as the API key
# But I want the long and lat to be different every time (different cities)
# Plus I want the city name BUT I don't really want to enter this info manually

# So each time it wants to tweet it can pick from a list of cities
# Plug in long and lat
# Use forecastio to find temp at current time
# Tweet that out

# wordcitiespop.txt has all the info for cities around the world and their long and lat

# start by getting forcastio to take one long & lat and tweet out one weather? I guess? To see how that works