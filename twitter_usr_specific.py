"""
Aditya Raj Gupta
18.04.19
"""

from tweepy import Cursor
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import twitter_credentials

class Twitter_client():
    def __init__(self,twitter_user=None):
        self.auth=Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)

        self.twitter_user=twitter_user

    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets    
    
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
         if (status==420):
             return false
         print(status)

class Twitter_Authenticator():

    def authenticate_twitter_app(self):
        auth=OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth  

"""
class TwitterStreamer():

 Class for streaming tweets

     def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
          #this method establishes connection and sets up stream
          listener=StdOutListener()
          auth=self.Twitter_Authenticator.authenticate_twitter_app()
          stream=Stream(auth, listener)

          #to capture tweets by hash tags
          stream.filter(track=hash_tag_list)



hash_tag_list=['aajtak','ndtv','cnn']
fetched_tweets_filename="fetched_tweets.json"
"""

client_list=['cnn','whitehouse','foxnews']
filename="usr_tweet_txt.txt"


with open(filename,'a') as tweets_file:
    for each_client in client_list:

        twitter_client=Twitter_client(each_client)
        tweets_list=twitter_client.get_user_timeline_tweets(5)
        print("\n"+each_client+"\n")
        print(tweets_list)
        print("\n....................inside file..........................\n")
        tweets_file.write("\n"+each_client+"\n")
        try:
            print("\nInside try 1\n")
            for each_tweet in tweets_list:
                json_object=json.dumps(each_tweet._json)
                converted_dict=json.loads(json_object)
                try:
                    print("\nInside try 2\n")
                    tweets_file.seek(0,2)
                    tweets_file.write(converted_dict['text'])
                except(e):
                    print("error in writing to file:"+e)
            print("\n")        
        except:
           print("errorr!!!!!!!")
tweets_file.close()            
