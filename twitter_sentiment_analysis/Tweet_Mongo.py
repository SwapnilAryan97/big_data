import json
from socket import socket
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from pymongo import MongoClient
from tweepy.streaming import StreamListener

MONGO_HOST = 'mongodb://localhost/twitterdb'

WORDS = ['#bitcoin', '#cryptocurrency', '#crypto', '#litecoin', '#satoshi', '#btc', '#BTC', '#ethereum', '#HODL']

'''
Twitter Developer Account Credentials
'''

access_token = '1451764303-7Rlqo8WuxT6xaXyiy6l3IK3W6nlRACQr7SA3Yo5'
access_secret = 'PbAXMCErQRTRD0ZY3QWHKxme3uMdxmcR4qcTKgvGwNf0N'
consumer_key = '9rmQqOmCEJkNOEjSadQwbVsWx'
consumer_secret = 'p7YrR3Wihr2oXRwd9ZJHYVCeeFlaLADS0CrmRczDarsvCXIzS3'


class Tweet_Stream_Listener(StreamListener):
    def on_error(self, status):
        print(status)
        '''
        For not killing the tweet stream
        '''
        return True

    def on_connect(self):
        print('Connected to Twitter streaming API.')

    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            '''
            Using MongoDB twitterdb database
            '''
            db = client.twitterdb
            datajson = json.loads(data)
            created_at = datajson['created_at']
            '''
            Message upon a tweet being collected
            '''
            print('Tweet collected at ' + str(created_at))
            db.twitter_search.insert(datajson)
        except Exception as e:
            print(e)

'''
Create Auth object
'''
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
'''
Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
'''
twitter_stream = Stream(auth, Tweet_Stream_Listener(api=tweepy.API(wait_on_rate_limit=True)))
'''
Custom Filter to pull all traffic for the said filters to be collected to MongoDB
'''
print('Tracking: ' + str(WORDS))
twitter_stream.filter(languages=['en'],track=WORDS)
