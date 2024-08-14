from datetime import datetime as dt
from dotenv import load_dotenv
import json
import os
import pandas as pd
import subprocess
import tweepy
from TweetAnalyzer import TweetAnalyzer



# API credentials
load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

#Authenticate API
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Extract data from Twitter API

tweets = list(tweepy.Cursor(api.search_tweets,
                    q='chatgpt',
                    tweet_mode='extended',
                    lang='en').items(5))


###################### Tweet Fact ################################
tweet_data=[]
for tweet in tweets:
    retweet = False
    if tweet.full_text[0, 2] == 'RT': retweet = True
    tweet_dict = {
        'tweet_id': tweet.id,
        'tweet_text': tweet.full_text,
        'author_id': tweet.author.id,
        'retweet_count': tweet.retweet_count,
        'favorite_count': tweet.favorite_count,
        'created_at': tweet.created_at,
        'retweet': 'yes' if retweet else 'no',
        'tweet_url': "https://twitter.com/twitter/statuses/"+tweet.id_str
    }

    tweet_data.append(tweet_dict)
    
tweet_df = pd.DataFrame(tweet_data)

#print('Tweet Data: ')
#print(tweet_df.head())

############################### Time Dim #############################
time_data = []
for tweet in tweets:
    time_dict = {
        'tweet_id': tweet.id,
        'created_at': tweet.created_at,
        'date': tweet.created_at.strftime("%Y-%m-%d"),
        'day' : tweet.created_at.day,
        'month' : tweet.created_at.month,
        'year' : tweet.created_at.year,
        'day_of_week' : tweet.created_at.strftime("%A"),
        'time' : tweet.created_at.strftime("%H:%M:%S"),
        'hour' : tweet.created_at.hour,
        'minute' : tweet.created_at.minute,
        'second' : tweet.created_at.second
    }

    print("Here is a time_dict: ")
    print(time_dict)
    time_data.append(time_dict)

time_df = pd.DataFrame(time_data)

print('Time Data:')
print(time_df.head())

#################### User Dim #################################
user_data = []
for tweet in tweets:
    print(tweet.author.id)
    print(tweet.author.name)
    print(tweet.author.location)
    print('Followers\' count: ' + str(tweet.author.followers_count))
    print('statuses_count' + str(tweet.author.statuses_count))
    user_dict = {
        'user_id': tweet.author.id,
        'user_name': tweet.author.name,
        'location': tweet.author.location,
        'followers_count': tweet.author.followers_count,
        'statuses_count': tweet.author.statuses_count
    }

    print("Here is a user_dict: ")
    print(user_dict)
    user_data.append(user_dict)

user_df = pd.DataFrame(user_data)

#print('User Data:')
#print(user_df.head())


###################################### Sentiment Dim ##################################

analyzer = TweetAnalyzer(tweets)
sentiments = analyzer.analyze_tweets()

sentiment_data = []
for i in range(len(tweets)):
    tweet = tweets[i]
    sentiment = sentiments[i]
    sentiment_dict = {
        'tweet_id': tweet.id,
        'tweet_text': tweet.full_text,
        'negative': sentiment[0],
        'neutral': sentiment[1],
        'positive': sentiment[2],
        'score': (sentiment[2] - sentiment[0]) * (1 - sentiment[1])
    }

    '''A score of +1 very positive sentiment.
    A score between 0.5-1: positive sentiment.
    A score between 0-0.5: a slightly positive sentiment.
    A score of 0: neutral sentiment.
    A score between -0.5-0 : slightly negative sentiment.
    A score between -1_-0.5 :  negative sentiment.
    A score of -1:  very negative sentiment.'''

    print("Here is a sentiment_dict: ")
    print(sentiment_dict)
    sentiment_data.append(sentiment_dict)

sentiment_df = pd.DataFrame(sentiment_data)

#print('Sentiment Data:')
#print(sentiment_df.head())

################### Device Dim #######################
device_data = []
for tweet in tweets:

    source = tweet.source
    source_url = tweet.source_url
    os = 'Unknown'
    device = 'Unknown'
    _from = 'Unknown'
    if 'download' in source_url:
        _from = 'Mobile App'
        if 'android' in source_url:
            os = 'Android'
            device = 'Android Phone'
        elif 'iphone' in source_url:
            os = 'iOS'
            device = 'iPhone'
        elif 'ipad' in source_url:
            os = 'iOS'
            device = 'iPad'
    elif 'mobile' in source_url:
        device = 'SmartPhone'
        _from = 'Browser on Mobile'

    device_dict = {
        'tweet_id': tweet.id,
        'source': source,
        'source_url': source_url,
        'device_type': device,
        'from': _from,
        'operating_system': os
    }
    device_data.append(device_dict)

device_df = pd.DataFrame(device_data)

#print('Device Data:')
#print(device_df.head())

#################### Hashtag Dim #############################
hashtag_data = []
for tweet in tweets:
    for hashtag in tweet.entities['hashtags']:
        hashtag_dict = {
            'tweet_id': tweet.id,
            'hashtag_text': hashtag['text'].lower()
        }
        print("Here is a hashtag dict: " + str(hashtag_dict))
        hashtag_data.append(hashtag_dict)

hashtag_df = pd.DataFrame(hashtag_data)
print('Hashtag Data:')
print(hashtag_df.head())

##################### Location Dim ##############################
location_data = []
for tweet in tweets:
    if tweet.place is not None:
        location_dict = {
            'tweet_id': tweet.id,
            'city': tweet.place.name,
            'state': tweet.place.full_name.split(', ')[-2],
            'country': tweet.place.country,
            'geocode': tweet.place.bounding_box.coordinates[0][0]
        }
        #The geocode is: [longitude, latitude]
    else:
        location_dict = {
            'tweet_id': tweet.id,
            'city': None,
            'state': None,
            'country': None,
            'geocode': None
        }
    print('Here is a location dict: '+ str(location_dict))
    location_data.append(location_dict)

location_df = pd.DataFrame(location_data)
#print('Location Data:')
#print(location_df.head())

print('Export Script will start')
subprocess.call(['sh', './export_script.sh'])