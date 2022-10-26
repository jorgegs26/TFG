import tweepy
from tweepy.auth import OAuthHandler
import json

def get_tweets(query, num_tweets):
	API_KEY = 'IXldUsANj3w5xr8OXwVjclfQh'
	API_SECRET_KEY = 'QQoUqeOinEICmKnJN050uWFJgLV7AOEXSoOQAEfl1rmpJcEnCN'
	ACCESS_TOKEN = '463777233-Ho48lkuQMLPeJYzohTrvFz5ItKDLmO51Xg8MPPWT'
	ACCESS_TOKEN_SECRET = 'oqQI6g7PxvldOgTaMjrg52hOtgOeumdpxjG0VnzMVc6pf'

	auth = OAuthHandler(API_KEY, API_SECRET_KEY)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)
	query = query + ' -filter:retweets'

	infoTweets = api.search_tweets(q=query, lang='en', count=num_tweets, tweet_mode='extended')
	tweets = []
	for tw in infoTweets:
		tweets.append(tw.full_text)
		
	return tweets
	

t = get_tweets('#SDGs',3)
for i in t:
	print(i + '\n')
