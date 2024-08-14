from datetime import datetime as dt
from decimal import Decimal
from dotenv import load_dotenv
import os
import pandas as pd
import re
import subprocess
import tweepy
from TweetAnalyzer import TweetAnalyzer


# API credentials
load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate API
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

tweets = list(
    tweepy.Cursor(
        api.search_tweets, q="chatgpt", tweet_mode="extended", lang="en"
    ).items(1300)
)


###################### Tweet Fact ################################
tweet_data = []
for tweet in tweets:
    retweet = False
    if tweet.full_text[0:2] == "RT":
        retweet = True
    if tweet.author.followers_count != 0:
        eng_rate = round(
            Decimal(
                (tweet.retweet_count + tweet.favorite_count)
                / tweet.author.followers_count
            ),
            2,
        )
    else:
        eng_rate = Decimal(0.00)

    tweet_dict = {  # create table tweets_fact (tw_id string, tw_text string, author_id string, retweet_count int, favorite_count int, created_at date, retweet boolean, tw_url string)
        "tweet_id": tweet.id,
        "tweet_text": tweet.full_text.replace("\n", " ")
        .replace("\t", " ")
        .replace(";", " ")
        .replace('"', " "),
        "author_id": tweet.author.id,
        "retweet_count": tweet.retweet_count,
        "favorite_count": tweet.favorite_count,
        "engagement_rate": eng_rate,
        "created_at": tweet.created_at,
        "retweet": retweet,
        "tweet_url": "https://twitter.com/twitter/statuses/" + tweet.id_str,
    }

    tweet_data.append(tweet_dict)

tweet_df = pd.DataFrame(tweet_data)
tweet_df.to_csv("twitter_data/tweet_fact.csv", index=False, sep="|")
print("tweet_fact done")

# print('Tweet Data: ')
# print(tweet_df.head())

############################### Time Dim #############################
time_data = []
for tweet in tweets:
    time_dict = {
        "tweet_id": tweet.id,
        "created_at": tweet.created_at,
        "date": tweet.created_at.strftime("%Y-%m-%d"),
        "day": tweet.created_at.day,
        "month": tweet.created_at.month,
        "year": tweet.created_at.year,
        "day_of_week": tweet.created_at.strftime("%A"),
        "time": tweet.created_at.strftime("%H:%M:%S"),
        "hour": tweet.created_at.hour,
        "minute": tweet.created_at.minute,
        "second": tweet.created_at.second,
    }

    # print("Here is a time_dict: ")
    # print(time_dict)
    time_data.append(time_dict)

time_df = pd.DataFrame(time_data)
time_df.to_csv("twitter_data/time_dim.csv", index=False, sep="|")
print("time_dim done")

# print('Time Data:')
# print(time_df.head())

#################### User Dim #################################
user_data = []
for tweet in tweets:
    """
    print(tweet.author.id)
    print(tweet.author.name)
    print(tweet.author.location)
    print('Followers\' count: ' + str(tweet.author.followers_count))
    print('statuses_count' + str(tweet.author.statuses_count))
    """

    user_dict = {
        "tweet_id": tweet.id,
        "user_id": tweet.author.id,
        "user_name": tweet.author.name,
        "location": tweet.author.location,
        "followers_count": tweet.author.followers_count,
        "statuses_count": tweet.author.statuses_count,
    }
    # print("Here is a user_dict: ")
    # print(user_dict)
    user_data.append(user_dict)

user_df = pd.DataFrame(user_data)
user_df.to_csv("twitter_data/user_dim.csv", index=False, sep="|")
print("user_dim done")
# print('User Data:')
# print(user_df.head())

###################################### Sentiment Dim ##################################

analyzer = TweetAnalyzer(tweets)
sentiments = analyzer.analyze_tweets()

def get_sentiment_label(score):
    
    '''
    A score of +1 very positive sentiment.
    A score between 0.5-1: positive sentiment.
    A score between 0-0.5: a slightly positive sentiment.
    A score of 0: neutral sentiment.
    A score between -0.5-0 : slightly negative sentiment.
    A score between -1_-0.5 :  negative sentiment.
    A score of -1:  very negative sentiment.
    
    Args:
        score (float): sentiment analysis score
    
    Returns:
        tuple: sentiment label and sub-label
    
    '''
    
    if score == 1:
        return ("positive", "very positive")
    elif 0.5 <= score < 1:
        return ("positive", "positive")
    elif 0 <= score < 0.5:
        return ("positive", "slightly positive")
    elif score == 0:
        return ("neutral", "neutral")
    elif -0.5 < score < 0:
        return ("negative", "slightly negative")
    elif -1 < score <= -0.5:
        return ("negative", "negative")
    elif score == -1:
        return ("negative", "very negative")

sentiment_data = []
for i in range(len(tweets)):
    tweet = tweets[i]
    sentiment = sentiments[i]
    score = round(
        Decimal(
            (sentiment[2].item() - sentiment[0].item()) * (1 - sentiment[1].item())
        ),
        2,
    )
    sentiment_dict = {
        "tweet_id": tweet.id,
        "tweet_text": tweet.full_text.replace("\n", " ")
        .replace("\t", " ")
        .replace(";", " ")
        .replace('"', " "),
        "score": score,
        "negative": round(Decimal(sentiment[0].item()), 2),
        "neutral": round(Decimal(sentiment[1].item()), 2),
        "positive": round(Decimal(sentiment[2].item()), 2),
        "general_sentiment": get_sentiment_label(score)[0],
        "sentiment": get_sentiment_label(score)[1],
    }

    # print("Here is a sentiment_dict: ")
    # print(sentiment_dict)
    sentiment_data.append(sentiment_dict)

sentiment_df = pd.DataFrame(sentiment_data)
sentiment_df.to_csv("twitter_data/sentiment_dim.csv", index=False, sep="|")
print("sentiment_dim done")

# print('Sentiment Data:')
# print(sentiment_df.head())

################### Device Dim #####################
device_data = []
for tweet in tweets:

    source = tweet.source
    source_url = tweet.source_url
    os = "Unknown"
    device = "Unknown"
    _from = "Unknown"
    if "download" in source_url:
        _from = "Mobile App"
        if "android" in source_url:
            os = "Android"
            device = "Android Phone"
        elif "iphone" in source_url:
            os = "iOS"
            device = "iPhone"
        elif "ipad" in source_url:
            os = "iOS"
            device = "iPad"
    elif "mobile" in source_url:
        device = "SmartPhone"
        _from = "Browser on Mobile"

    device_dict = {
        "tweet_id": tweet.id,
        "source": source,
        "source_url": source_url,
        "device_type": device,
        "from": _from,
        "operating_system": os,
    }
    device_data.append(device_dict)

device_df = pd.DataFrame(device_data)
device_df.to_csv("twitter_data/device_dim.csv", index=False, sep="|")
print("device_dim done")

# print('Device Data:')
# print(device_df.head())

############### Hashtag Dim #######################
hashtag_data = []
print("here are the hashtags: ")
for tweet in tweets:
    hashtags = re.findall(r"#(\w+)", str(tweet.full_text))
    print(hashtags)
    for hashtag in hashtags:
        hashtag_dict = {
            # create table hashtag_dim (tw_id string, hashtag string)
            "tweet_id": tweet.id,
            "hashtag": "#" + hashtag,
            "normalized_hashtag": hashtag.lower()
            .replace("_", "")
            .replace("-", "")
            .replace("#", ""),
        }
        # print("Here is a hashtag dict: " + str(hashtag_dict))
        hashtag_data.append(hashtag_dict)

hashtag_df = pd.DataFrame(hashtag_data)
hashtag_df.to_csv("twitter_data/hashtag_dim.csv", index=False, sep="|")
print("hashtag_dim done")

# print('Hashtag Data:')
# print(hashtag_df.head())


################ Location Dim ######################
location_data = []
for tweet in tweets:
    if tweet.place is not None:
        location_dict = {
            # create table location_dim (tw_id string, city string,
            # state string, country string, geocode string)
            "tweet_id": tweet.id,
            "user_location": tweet.author.location,
            "city": tweet.place.name,
            "state": tweet.place.full_name.split(", ")[-2],
            "country": tweet.place.country,
            "geocode": tweet.place.bounding_box.coordinates[0][0],
        }
        # The geocode is: [longitude, latitude]
    else:
        location_dict = {
            "tweet_id": tweet.id,
            "user_location": tweet.author.location,
            "city": None,
            "state": None,
            "country": None,
            "geocode": None,
        }
    # print('Here is a location dict: '+ str(location_dict))
    location_data.append(location_dict)

location_df = pd.DataFrame(location_data)
location_df.to_csv("twitter_data/location_dim.csv", index=False, sep="|")
print("location_dim done")

# print('Location Data:')
# print(location_df.head())

print("Export Script will start")
subprocess.call(["sh", "./export_script.sh"])