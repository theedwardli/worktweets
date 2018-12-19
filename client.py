import config
import re 
import json
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
    ''' 
    Generic Twitter Class
    '''
    def __init__(self): 
        ''' 
        Class constructor 
        '''
        # Keys and tokens from the Twitter Dev Console 
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        access_token = config.access_token
        access_token_secret = config.access_token_secret 

        # Attempt authentication 
        try: 
            # Create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # Set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # Create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
            using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
            using textblob's sentiment method 
        '''
        # Create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # Set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # Empty list to store parsed tweets 
        tweets = [] 

        try: 
            # Call Twitter API to fetch tweets
            fetched_tweets = tweepy.Cursor(self.api.search, q = query, tweet_mode = 'extended', include_rts = True).items(count)

            # Parsing tweets one by one 
            for tweet in fetched_tweets: 
                # Empty dictionary to store required params of a tweet 
                parsed_tweet = {} 

                if 'retweeted_status' in tweet._json:
                    parsed_tweet['text'] = tweet._json['retweeted_status']['full_text'].replace('\n', ' ')
                else:
                    parsed_tweet['text'] = tweet.full_text.replace('\n', ' ')
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text) 

                # Appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # If tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            # Return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # Print error (if any) 
            print("Error : " + str(e)) 

def main(): 
    # Creating object of TwitterClient Class 
    api = TwitterClient() 

    # Calling function to get all tweets
    tweets = api.get_tweets(query = 'work', count = 200) 

    # Write tweets to file
    with open('work_tweets.txt', 'a+') as f:
        for tweet in tweets:
            f.write("%s\n" % tweet['text'].encode('utf-8'))

    # Filter out the negative tweets from the list of all tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 

    # Write negative tweets to file
    with open('work_tweets_negative.txt', 'a+') as f:
        for tweet in ntweets:
            f.write("%s\n" % tweet['text'].encode('utf-8'))

if __name__ == "__main__": 
    # Calling main function 
    main() 
