import tweepy
from tweepy import OAuthHandler
import config
import logging
import json

out = "/home/ubuntu/Talk3_extension/data/tweets.jsonl"


class TinnitusStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        logging.warn("Stored message " + str(status.id))
        with open(out, "a") as fh:
            json.dump(status._json, fh)
            fh.write('\n')

    def on_error(self, status_code):
        logging.warn("Error: " + str(status_code))

        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

stream = tweepy.Stream(auth=api.auth, listener=TinnitusStreamListener())
stream.filter(track=["tinnitus", "tinitus", "hyperacusis"])
