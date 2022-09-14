import configparser
import tweepy
from textblob import TextBlob
import statistics
from typing import List
import preprocessor as p

# read config
config = configparser.ConfigParser()
config.read('config.ini')

CONSUMER_KEY = config['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = config['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_SECRET = config['twitter']['ACCESS_SECRET']

# authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def get_tweets(keyword: str) -> List[str]:
  all_tweets = []

  for tweet in api.search_tweets(q=keyword, lang='en', count=100):
    all_tweets.append(tweet.text)
  
  return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]:
  tweets_clean = []

  for tweet in all_tweets:
    tweets_clean.append(p.clean(tweet))
  
  return tweets_clean

def get_sentiment(all_tweets: List[str]) -> List[float]:
  sentiment_scores = []
  
  for tweet in all_tweets:
    blob = TextBlob(tweet)
    sentiment_scores.append(blob.sentiment.polarity)

  return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:
  tweets = get_tweets(keyword)
  tweets_clean = clean_tweets(tweets)
  sentiment_scores = get_sentiment(tweets_clean)

  average_score = statistics.mean(sentiment_scores)

  return average_score


if __name__ == '__main__':
  print("What does the world prefer?")
  first_answer = input()
  print("...or...?")
  second_answer = input()
  print("\n")

  first_score = generate_average_sentiment_score(first_answer)
  second_score = generate_average_sentiment_score(second_answer)

  if (first_score > second_score):
    print(f"The world prefers {first_answer} over {second_answer}!")
  else:
    print(f"The world prefers {second_answer} over {first_answer}!")
