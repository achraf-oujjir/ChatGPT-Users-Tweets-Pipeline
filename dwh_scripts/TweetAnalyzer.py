from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

class TweetAnalyzer:
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    labels = ['Negative', 'Neutral', 'Positive']

    def __init__(self, tweets_arr):
        self.tweets_arr = tweets_arr
        print('Tweets arr has been initialized!')

    def preprocess_tweets(self):
        tw_arr = self.tweets_arr
        preproc_tweets = []
        for tweet in tw_arr:
            tweet_words=[]
            for word in tweet.full_text.split(' '):
                if word.startswith('@') and len(word) > 1:
                    word = '@user'
                elif word.startswith('http') or word.startswith('www'):
                    word = 'http'
                tweet_words.append(word)
            proc_tweet = " ".join(tweet_words)
            preproc_tweets.append(proc_tweet)
        assert len(tw_arr) == len(preproc_tweets)
        print('Tweets have been preprocessed!')
        print(type(preproc_tweets))
        return preproc_tweets
    
    def analyze_tweets(self):
        preproc_tweets = self.preprocess_tweets()
        sentiments=[]
        print('Type of preproc_tweets: ', end=' ')
        print(type(preproc_tweets))
        for tweet in preproc_tweets:
            encoded_tweet = self.tokenizer(tweet, return_tensors='pt')
            output = TweetAnalyzer.model(**encoded_tweet)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            #print('Here are the scores: ' + str(scores))
            #sentiment = TweetAnalyzer.labels[scores.argmax()]
            #print('The sentiment for this tweet is: ' + sentiment)
            sentiments.append(scores)

        print('All sentiments have been analyzed!')
        return np.array(sentiments)
            
'''

tweets = ["@AchrafOujjir I'm loving this @ Casablanca !! 😊 https://www.google.com",
            "I hate this!!", "Awesome!", 'the earth revolves around the world']

analyzer = TweetAnalyzer(tweets)
sentiments = analyzer.analyze_tweets()
print('Tweets have been analyzed ')
print(sentiments)

'''
