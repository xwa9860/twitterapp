from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import twitterapp.services.twitter_config as config
from twitterapp.database import db_crud


class TwitterDataListener(StreamListener):

    def __init__(self, api=None):
        super(TwitterDataListener, self).__init__()
        self.num_tweets = 0


    def on_status(self, data):
        #try:
        self.num_tweets += 1
        if self.num_tweets < 2:
            db_crud.add_status_to_db(data)
            return True
        else:
            print('got 10 tweets, stopping the stream')
            return False
        #except:
        #    print('data logging error')
        #return True

    def on_error(self, status):
        print(status)
        return True


class TwitterDataStreamer:
    def __init__(self):
        self.auth = OAuthHandler(config.CONSUMER_KEY,
                                 config.CONSUMER_SECRET)
        self.auth.set_access_token(config.ACCESS_TOKEN,
                                   config.ACCESS_SECRET)
        self.api = API(self.auth)

    def stream(self, keywords):
        '''
        keywords: a list of keywords
        '''
        stream = Stream(self.auth, TwitterDataListener())
        stream.filter(track=keywords)