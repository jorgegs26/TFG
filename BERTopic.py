from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
import pymongo
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def date_graph(dates):
    dates_to_plot = []
    num_of_dates = []
    for i in dates:
        dt = i.split()
        if dt[0] in dates_to_plot:
            pos = dates_to_plot.index(dt[0])
            aux = num_of_dates[pos]
            value = aux + 1
            num_of_dates[pos] = value
        else:
            dates_to_plot.append(dt[0])
            num_of_dates.append(1)
    
    x = np.array(dates_to_plot)
    y = np.array(num_of_dates)

    plt.plot(x,y)
    plt.show()

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
tweets, timestamps = get_tweets('SDGs', mydb)

# Train the model
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(tweets)

# Calculate topics over time
topics_over_time = topic_model.topics_over_time(tweets, timestamps, nr_bins=20, datetime_format="%Y-%m-%d %H:%M:%S")
fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=20)

#Topic word Scores
fig2 = topic_model.visualize_barchart()

#print(topic_model.get_topic_info())

#Gráficas
fig.show()
fig2.show()
date_graph(timestamps)
