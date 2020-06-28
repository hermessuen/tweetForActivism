This project was inspired by the wave of protests supporting the Black Lives Matter movement that occured in the spring and summer of 2020. In an effort to stop the spread of misinformation and to use twitter for good, I applied for a Twitter development account. I then created the following files:

collectTweets.py:

This is the twitter bot that uses the Twitter streaming API to collect tweets made with the hashtag "blm", or "blacklivesmatter" in conjunction with words like "protest", "donate" and "sign". Running this program for just two days gave me access to more than 7000 tweets.

trainClassifier.py:

I used the tweets collected from "collectTweets.py" as training data for an SVM classifier. The SVM classifier was meant to distinguish between actionable information with non-actionable information. I created an Amazon Mechanical Turk Task to manually label the tweets I had collected. Once the tweets were labeled, I could use them for training. I was able to achieve ~ 97% accuracy on held out test data.

twitterBot.py:

Finally, I used the trained SVM classifier to create a twitterbot that tweets out every five minutes. It looks at the latest tweets containing references to "Black Lives Matter" and re-tweets them if they contain actionable information (i.e. where to protest, where to donate, etc). It also manually looks at certain twitter accoutns in the Boston area and examines their latest tweet to see if it contains useful information.


FURTHER IMPROVEMENTS:
As Ive examined the tweets the account automatically retweets, it has become clear that there is a major limitation to the program. Many people use twitter for false donations, false petitions, and other misinformation that at the surface is indistinguishable from actual actionable information. The bot is unable to pick up on this discrepancies, and further iterations will try to account for this 
