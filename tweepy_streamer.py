"""
Aditya Raj Gupta
17.04.19
"""


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import twitter_credentials

class StdOutListener(StreamListener):
     """
     class for writing tweets to a file
     """
     def __init__(self,fetched_tweets_filename="fetched_tweets.json"):
          self.fetched_tweets_filename=fetched_tweets_filename
     def on_data(self, data):
          try:
               print(data)
               converted_dict=json.loads(data)
               with open("tweets_from_json.txt",'a') as tweets_txt_file:
                    tweets_txt_file.write(converted_dict['text'])
                    tweets_txt_file.write("\n.....next tweet.....\n")
               with open(self.fetched_tweets_filename,'a') as tweets_filename:
                    tweets_filename.write(data)
               return True
          except BaseException as e:
               print("Error on data:%s" % str(e))
          return True
        
         
     def on_error(self,status):
         if status==420:
              return False
         print(status)

         
class TwitterStreamer():
     """
     Class for streaming tweets
     """
     def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
          #this method establishes connection and sets up stream
          listener=StdOutListener()
          auth=OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
          auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
          stream=Stream(auth, listener)
          stream.filter(track=hash_tag_list)



hash_tag_list=['aajtak','ndtv','cnn']
fetched_tweets_filename="fetched_tweets.json"

twitter_streamer_obj=TwitterStreamer()
twitter_streamer_obj.stream_tweets(fetched_tweets_filename,hash_tag_list)
