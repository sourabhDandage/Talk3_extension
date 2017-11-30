import tweepy
from tweepy import OAuthHandler
import json
import sys
import config


auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

searchQuery = 'tinnitus'   # this is what we're searching for
maxTweets = 10000000  # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
        else:
            new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                    max_id=str(max_id - 1))
        if not new_tweets:
            sys.stderr.write("No more tweets found\n")
            break
        for tweet in new_tweets:
            print(json.dumps(tweet._json) + '\n')
        tweetCount += len(new_tweets)
        # if len(new_tweets) < tweetsPerQry:
        #     sys.stderr.write("No more tweets found (D)\n")
        #     break
        sys.stderr.write("Downloaded {0} tweets\n".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        sys.stderr.write("some error : " + str(e) + "\n")
        break

sys.stderr.write("Downloaded {0} tweets for query {1}\n".format(tweetCount, searchQuery))
