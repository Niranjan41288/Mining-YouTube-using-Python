from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError #pip install google-api-python-client
from oauth2client.tools import argparser #pip install oauth2client
import pandas as pd #pip install pandas
import matplotlib as plt

from datetime import datetime # current time in python
now = datetime.now()
print now

import pymongo

try:
    conn=pymongo.MongoClient()
    print "Connected to Mongodb successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 
conn
 
# import mongodb library

from pymongo import MongoClient

client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.test_database

collection = db.test1_collection
    
print 'Hello'



# Set DEVELOPER_KEY to the API key value from the APIs & auth > REGISTERED apps
# tab of
# https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


# Get the API key from text file or pass directly to the variable

API_KEY = open("E:/Study_Materials/Mining_Youtube_data/API_KEY.txt","r")
API_KEY = API_KEY.read()

search_term = raw_input("Search for the channel: ")

print search_term

DEVELOPER_KEY = API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

argparser.add_argument("--q", help="Search term", default=search_term) #change the default to the search term you want to search
argparser.add_argument("--max-results", help="Max results", default=5) #default number of results which are returned. It can very from 0 - 50

args = argparser.parse_args()
options = args
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY) # Call the search.list method to retrieve results matching the specified

print "search term is"
print options.q

# query term.

search_response = youtube.search().list(
 q=options.q,
 type="channel",
 part="id,snippet",
 maxResults=options.max_results
).execute()



#print search_response
# Add each result to the appropriate list, and then display the lists of
# matching videos.
# Filter out channels, and playlists.

videos = {} # Create empty list to store the filtered result

posts = db.youtube53

for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#channel":
        #videos[search_result["id"]["channelId"]] = search_result["snippet"]["title"]
        channel_response = youtube.channelSections().list(
            channelId =search_result["id"]["channelId"],
            part="snippet",
            ).execute()

        #print "search_result"
        #print search_result["id"]["channelId"]

        videos_list_response = youtube.channels().list(
            id=search_result["id"]["channelId"],
            part='id,snippet,statistics,contentDetails'
            ).execute()

        #print channel_data

        for channel_data in  videos_list_response.get("items", []):
            print "channel_data"
            print channel_data["id"]
            for i in channel_response.get("items", []):
                relatedChannelid = i["id"]
                print "relatedChannelid"
                print relatedChannelid
                data ={}
                data['channelId'] = channel_data["id"]
                data['relatedChannelid'] = i["id"]
                #data['relatedPlaylists'] = video["contentDetails"]["relatedPlaylists"]
                data['commentCount'] = channel_data["statistics"]["commentCount"]
                data['viewCount'] = channel_data["statistics"]["viewCount"]
                data['videoCount'] = channel_data["statistics"]["videoCount"]
                data['subscriberCount'] = channel_data["statistics"]["subscriberCount"]
                data['publishedAt'] = channel_data["snippet"]["publishedAt"]
                data['title'] = channel_data["snippet"]["title"]
                #Insert process
                #print channel_data["id"]
                data['subscriberCount'] = ( int(data['viewCount']) // int(data['subscriberCount'] )) // 1000
                data['viewCount'] = int(data['viewCount']) // 100000
                posts.update({"relatedChannelid":data['relatedChannelid']},{"$set":{"channelId":data['channelId'], "commentCount":data['commentCount'],"subscriberCount":data['subscriberCount'],
                                            "viewCount":data['viewCount'],"videoCount":data['videoCount'],"publishedAt":data['publishedAt'],
                                            "title":data['title']}}, upsert=True)


# Print the result of firsrt two documents
##for d in posts.find()[:2]:
##	print d


# Print the result based on channel id 
for post in posts.find({"channelId": "UCIV1HCg0jW_9OuFCSX5gMIw"}):
    print post


