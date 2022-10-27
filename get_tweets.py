import tweepy
from tweepy.auth import OAuthHandler
from translate import get_translation

def get_full_tweets(query, num_tweets):
	API_KEY = ''
	API_SECRET_KEY = ''
	ACCESS_TOKEN = ''
	ACCESS_TOKEN_SECRET = ''

	auth = OAuthHandler(API_KEY, API_SECRET_KEY)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)
	query = query + ' -filter:retweets'

	infoTweets = api.search_tweets(q=query, count=num_tweets, tweet_mode='extended')
	tweets = []
	for tw in infoTweets:
		tweets.append(tw.full_text)
		
	return tweets
	
translated_tweets = []
tweets = get_full_tweets('#SDGs',50)

for tw in tweets:
	tr_tweet, language = get_translation(tw, 'en')
	if(language == ''):
		print('Error: ', tr_tweet)
	else:
		print('Idioma del tweet ',language, ': ', tr_tweet)
		translated_tweets.append(tr_tweet)
	
