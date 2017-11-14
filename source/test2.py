import tweepy
from tweepy import OAuthHandler
import json
from collections import Counter
import sys



#twitter app details


#------------------
#basic code to get latest tweets, issue of response 420
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

counter = Counter()

with open("data/treatment_definitons.txt", "r") as fh:
    for line in fh:
        treatments = line.strip().split(",")
        name = treatments[0]
        print("==== {} ===".format(name))
        for treatment in treatments:
            sys.stderr.write("Treatment {}\n".format(treatment))
            searchQuery = 'tinnitus ' + treatment  # this is what we're searching for
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
                    if len(new_tweets) < tweetsPerQry:
                        sys.stderr.write("No more tweets found (D)\n")
                        break
                    sys.stderr.write("Downloaded {0} tweets\n".format(tweetCount))
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    sys.stderr.write("some error : " + str(e) + "\n")
                    break

            counter[name] += tweetCount
            sys.stderr.write("Downloaded {0} tweets for query {1}\n".format(tweetCount, searchQuery))

for treatment, count in counter.items():
    sys.stderr.write("{}: {}\n".format(treatment, count))
