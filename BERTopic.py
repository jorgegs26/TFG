from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
import pymongo
import matplotlib.pyplot as plt

def get_tweets(name, mydb):
	print('Recuperando los tweets de la BBDD "TFG" de la colección ', name, '...')
	mycol = mydb[name]
	myresult = mycol.find()
	tweets = []
	date_tweets = []
	for data in myresult:
		tweets.append(data['tweet'])
		dt = data['date'].split('+')
		date_tweets.append(dt[0])

	return tweets, date_tweets


myclient = pymongo.MongoClient('mongodb://f-l3202-pc02.aulas.etsit.urjc.es:21500/')
mydb = myclient["TFG"]
tweets, timestamps = get_tweets('Rusia', mydb)

# Train the model
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(tweets)

# Calculate topics over time
topics_over_time = topic_model.topics_over_time(tweets, timestamps, nr_bins=20, datetime_format="%Y-%m-%d %H:%M:%S")
fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=20)

#plt.fig()

plt.plot(fig)

# Finally, save the model
#topic_model.save("my_model")
