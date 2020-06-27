from apscheduler.schedulers.blocking import BlockingScheduler
import tweepy
import re
import string
import pickle

# Load pre-trained SVM with its corresponding Word Vectorizer
with open('Models\\vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)

with open('Models\\model.pickle', 'rb') as f:
    model = pickle.load(f)

def process_text(latest_tweet):
    # pre-process the tweet
    latest_tweet = latest_tweet.lower()  # everything lower case
    latest_tweet = re.sub(r'\d+', '', latest_tweet)  # remove numbers
    translator = str.maketrans('', '', string.punctuation)
    latest_tweet = latest_tweet.translate(translator)  # remove punctuation
    latest_tweet = latest_tweet.replace('.', '')  # remove all periods

    return latest_tweet


def tweet_update():
    search_words = "#blacklivesmatter"
    importantBostonAccts = ['BlmBoston', 'ACLU_Mass', 'UCBoston',
                            'ViolenceNBoston', 'MassBailFund',
                            'LiveBoston617', 'BostonGlobe',
                            'SunriseBoston', 'AyannaPressley',
                            'BostonTweet']
    importantWords = ['donate', 'protest',
                      'AM', 'PM', 'vigil', 'petition',
                      'meeting', 'demonstration',
                      'march', 'assembly', 'pledge',
                      'next week', 'today', 'tomorrow']

    badWords = 'alllivesmatter'

    # authentication keys for your personal Developer Twitter account:
    consumer_key = '#####'
    consumer_secret = '#####'

    # authentication keys for the account to tweet from:
    access_token = '#####'
    access_token_secret = '#####'

    # Set up OAuth and integrate with API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_tweet = tweepy.API(auth)  # create the object to send out tweets

    # get the tweets
    for account in importantBostonAccts:
        print('Evaluating latest tweet for {0}'.format(account))
        to_retweet = False
        user = api_tweet.get_user(account)
        id_acct = user.id
        # get latest tweets
        tweets = api_tweet.user_timeline(id_acct)
        # latest tweet will be the first one
        latest_tweet = tweets[0].text
        latest_tweet = process_text(latest_tweet)


        # check to see if any of the relevant key words are inside the latest tweet
        for word in importantWords:
            if word in latest_tweet and badWords not in latest_tweet:
                to_retweet = True
                print('It has been evaluated to be an important tweet')

        if to_retweet:
            try:
                tweets[0].retweet()
                print('ReTweeted')

            except Exception as e:
                print('Tried but failed to retweet')
                print('The exception is : {0}'.format(str(e)))


        else:
            print('Not an important tweet, moving on to next account')

    print('==============================')
    print('EVALUATING TWEETS WITH HASHTAGS')
    # look at all recent tweets with hashtag blmprotest and see if any of them contain the word boston to narrow
    # down to specifically boston related things
    tweets = tweepy.Cursor(api_tweet.search, q=search_words, lang="en").items(100)
    for tweet in range(100):
        to_retweet = False
        curr_tweet = tweets.next()
        curr_tweet_text = process_text(curr_tweet.text)

        # use our pre-trained SVM to determine whether this tweet contains actionable information
        if model.predict(vectorizer([curr_tweet_text]))[0]:
            to_retweet = True

        if to_retweet:
            try:
                print('Important Tweet with hashtag')
                curr_tweet.retweet()
                print("Retweeted")
            except Exception as e:
                print('Important but Failed ')
                print('Failed because: {0}'.format(str(e)))
        else:
            print('Tweet not important')

    print('DONE')

sched = BlockingScheduler()
sched.add_job(tweet_update, 'cron', minute='*/5')
sched.start()
