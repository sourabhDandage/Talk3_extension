import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import csv

#twitter app details
consumer_key = '6znc42S4TMrzalEefVuI66EkV'
consumer_secret = 'TGVNutbvFrYbjiejCwQyW4zhsgN1yb3pOCJaKzrK80IwTQskrx'
access_token = '923180591285026816-VAK2kggxKu8ccUDdXOL9AFB55836YnL'
access_secret = 'RSxHzmvaBUUuUrrUQdTrcwFWU9RXAZdDqC9aOSeackfyX'

data_dir = '../output'

#------------------
#basic code to get latest tweets, issue of response 420
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#for status in tweepy.Cursor(api.home_timeline).items(10):
#Process a single status
 #   print(status.text)

#----------------------------

#output in python.json file
# class MyListener(StreamListener):
#     def on_data(self, data):
#         try:
#             with open(data_dir + '/python.json', 'a') as f:
#                 f.write(data)
#                 return True
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True
#
#     def on_error(self, status):
#         print(status)
#         return True
#
#
# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#tinnitus'])


import json
from pprint import pprint

with open(data_dir + '/python.json') as data_file:
    data = json.load(data_file)

pprint(data["text"])

# Open/Create a file to append data
csvFile = open(data_dir +'/tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)


for tweet in tweepy.Cursor(api.search,q="#tinnitus",count=100,lang="en",since_id='2014-06-12').items():
                            print(tweet.created_at, tweet.text)
                            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])