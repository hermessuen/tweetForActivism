
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import svm
from sklearn.metrics import adjusted_rand_score
import tweepy
import string
import re
import pandas as pd
import time
import numpy as np

from sklearn.model_selection import train_test_split


categories = ["ForBLM", "AgainstBLM",
              "Action", "NonAction"]

search_words = "#blacklivesmatter"

num_documents_to_train = 1000
num_classes = 2

label_dictionary = {"Asking audience to donate to an organization": 1, "Does not contain actionable information": 0,
                    "Information about where and when to attend a protest": 1, "Asking you to sign a petition": 1}


def process_text(latest_tweet):
    # pre-process the tweet
    latest_tweet = latest_tweet.lower()  # everything lower case
    latest_tweet = re.sub(r'\d+', '', latest_tweet)  # remove numbers
    translator = str.maketrans('', '', string.punctuation)
    latest_tweet = latest_tweet.translate(translator)  # remove punctuation
    latest_tweet = latest_tweet.replace('.', '')  # remove all periods

    return latest_tweet


def train_classifier(documents):
    documents = pd.read_csv(documents)
    tweets = list(documents['BLM'])
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(tweets)

    # organize the training data
    labels = documents["Label"]
    labels = [label_dictionary[label] for label in labels]

    # split the data set between training & test
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.4, random_state=42, stratify=labels)


    model = svm.SVC(verbose=True, kernel='rbf', C=3) # the higher the- C value, the more GENERALIZABLE it will be
    model.fit(X, labels)

    # examine the accuracy
    predictions = model.predict(X_test)
    num_correct = predictions == y_test
    num_correct = np.sum(num_correct)
    acc = num_correct/len(y_test)
    print("Accuracy on training set is {0}".format(acc))


    return model, vectorizer


if __name__ == '__main__':
    storage_location = "C:\\Users\\hsuen\\OneDrive - MathWorks\\Desktop\\QuantTrading\\tweetBot\\data\\BLMHashtag\\BLM1.csv"
    storage_location = "C:\\Users\\hsuen\\Downloads\\Batch_4093555_batch_results.csv"
    model, vectorizer = train_classifier(storage_location)
