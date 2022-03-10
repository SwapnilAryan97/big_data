import json
from socket import socket
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

WORDS = ['#bitcoin', '#cryptocurrency', '#crypto', '#litecoin', '#satoshi']

'''
Twitter Developer Account Credentials
'''
access_token = '1451764303-7Rlqo8WuxT6xaXyiy6l3IK3W6nlRACQr7SA3Yo5'
access_secret = 'PbAXMCErQRTRD0ZY3QWHKxme3uMdxmcR4qcTKgvGwNf0N'
consumer_key = '9rmQqOmCEJkNOEjSadQwbVsWx'
consumer_secret = 'p7YrR3Wihr2oXRwd9ZJHYVCeeFlaLADS0CrmRczDarsvCXIzS3'


class TweetStreamListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            message = json.loads(data)
            print(message['text'].encode('utf-8'))
            self.client_socket.send(message['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print('Error on_data : %s' % str(e))
        return True

    def on_error(self, status):
        print(status)
        '''
        For not killing the tweet stream
        '''
        return True


def sendData(c_socket):
    '''
    Create Auth object
    '''
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetStreamListener(c_socket))
    '''
    Custom Filter to pull all traffic for the said filters in english language in real time.
    '''
    twitter_stream.filter(languages=['en'],track=WORDS)


if __name__ == '__main__':
    '''
    Create a socket object
    '''
    s = socket()   
    '''
    Local machine name
    '''
    host = '127.0.0.1' 
    '''
    Reserve a port for the service.
    '''
    port = 9999    
    '''
    Bind to the port
    '''
    s.bind((host, port))       

    print('Listening on port: %s' % str(port))
    
    '''
    Waiting for client connection.
    '''
    s.listen(5) 
    '''
    Establish connection with client.
    '''
    c, address = s.accept()        

    print('Received request from: ' + str(address))

    sendData(c)
