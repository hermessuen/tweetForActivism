import tweepy
import pandas as pd
import re
import string
import demoji

storage_location = "C:\\Users\\hsuen\\OneDrive - MathWorks\\Desktop\\QuantTrading\\tweetBot\data\\BLMHashtag\\"

# authentication keys for your personal Developer Twitter account:
consumer_key = '#####'
consumer_secret = '#####'

# authentication keys for the account to tweet from:
access_token = '#####'
access_token_secret = '#####'

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)  # create the object to send out tweets


def is_reply(tweet):
    try:
        if (tweet.retweeted_status
                or tweet.in_reply_to_status_id
                or tweet.in_reply_to_status_id_str
                or tweet.in_reply_to_user_id
                or tweet.in_reply_to_user_id_str
                or tweet.in_reply_to_screen_name):
            return True
    except Exception as e:
        #print(e)
        return False


def process_csv_file(file):
    # pre-process the tweet
    tweets = pd.read_csv(file)
    new_tweets = []
    for idx, tweet in tweets.iterrows():
        new_tweet = tweet['BLM'].lower()  # everything lower case
        new_tweet = demoji.replace(new_tweet, " ")
        new_tweets.append(new_tweet)

    new_tweets = pd.DataFrame(new_tweets, columns=['BLM'])
    new_tweets.to_csv(file, index=False)


class MyStreamListener(tweepy.StreamListener):
    num_tweets = 0
    tweets = []
    tweets_per_file = 0
    num_files_exist = 0
    total_files = 0

    def update_self(self, tweets_per_file, num_files_exist, total_files):
        self.tweets_per_file = tweets_per_file
        self.num_files_exist = num_files_exist
        self.total_files = total_files

    # this function defines what we will do when a status comes through
    # we inherit the basic structure of the class from the tweepy library
    def on_status(self, status):
        # checks to see if this is a retweet or not
        # also return if the tweet is too short
        if is_reply(status) or len(status.text) < 15:
            return
        self.num_tweets += 1
        self.tweets.append(status.text)
        print('Adding tweet number {0}'.format(self.num_tweets))

        if self.num_tweets % self.tweets_per_file == 0:
            print('#####################')
            print('Writing tweets to a file')
            self.num_files_exist += 1
            tweets_pd = pd.DataFrame(self.tweets, columns=["BLM"])
            tweets_pd.to_csv(storage_location + "BLM" + "{0}.csv".format(self.num_files_exist), encoding='utf-8')
            self.num_tweets = 0
            self.tweets = []
            if self.num_files_exist > self.total_files:
                print('MAX NUMBER OF FILES REACHED')
                # returning False in any of the "on_data" methods disconnects the stream
                return False


def main():
    # CONSTANTS DEFINED HERE:
    tweets_per_file = 1000
    num_files = 0
    total_files = 10
    myStreamListener = MyStreamListener
    myStreamListener.update_self(myStreamListener, tweets_per_file, num_files, total_files)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener())
    while True:
        try:
            myStream.filter(track=['blm protest', 'blacklivesmatter protest', 'blacklivesmatter petition',
                                   'blacklivesmatter donate', 'blm donate', 'blacklivesmatter rally'], stall_warnings=True)
        except:
            continue

def format_csv_files():
    demoji.download_codes()
    location_files = 'C:\\Users\\hsuen\\OneDrive - MathWorks\\Desktop\\QuantTrading\\tweetBot\\data\\BLMHashtag\\'
    for x in range(7):
        num_file = x + 1
        print('Processing file {0}'.format(num_file))
        file_to_process = location_files + "BLM{0}.csv".format(num_file)
        process_csv_file(file_to_process)


if __name__ == '__main__':
    #main()
    format_csv_files()
