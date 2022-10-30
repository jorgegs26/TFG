import tweepy
from tweepy.auth import OAuthHandler
import re
import emoji

# Función para eliminar las urls de los tweets ya que estas no nos proporcionan información a la hora de obtener el gráfico de conocimiento
def delete_urls(text):
	url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' # Patron que siguen las urls

	urls = re.findall(url_pattern, text)
	for u in urls:
		aux = text.replace(u,'')
		text = aux
	return text

# Función para eliminar los emojis de los tweets ya que estos pueden interferir en la extracción de las relaciones y las entidades que haremos con NLP
def delete_icons(text):
    text = emoji.replace_emoji(text,replace='')
    return text

	
def get_full_tweets(query, num_tweets):
	# Credenciales de mi usuario
	API_KEY = 'IXldUsANj3w5xr8OXwVjclfQh'
	API_SECRET_KEY = 'QQoUqeOinEICmKnJN050uWFJgLV7AOEXSoOQAEfl1rmpJcEnCN'
	ACCESS_TOKEN = '463777233-Ho48lkuQMLPeJYzohTrvFz5ItKDLmO51Xg8MPPWT'
	ACCESS_TOKEN_SECRET = 'oqQI6g7PxvldOgTaMjrg52hOtgOeumdpxjG0VnzMVc6pf'

	auth = OAuthHandler(API_KEY, API_SECRET_KEY)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)
	query = query + ' -filter:retweets' # Añadimos el filtro para evitar recuperar rts, solo nos interesan tweets escritos para no obtener ningún duplicado

	# El result_type es para sacar los tweets que tienen mayor importancia en la reed
	# El tweet_mode es para recuperar el tweet completo
	infoTweets = api.search_tweets(q=query, count=num_tweets, tweet_mode='extended')
	tweets = []
	for tw in infoTweets:
		text = delete_urls(tw.full_text)
		text = delete_icons(text)
		tweets.append(text)
		
	return tweets

# Función para separar las frases de un párrafo. Esto es necesario para formar las entidades y relaciones del gráfico de conocimiento
def separar_en_oraciones(text):
	aux = text.replace('\n','.') # Sustituimos los saltos de línea por el caracter '.' ya que muchos usuarios separan sus frases solo con un intro
	splitted_text = aux.split('.')
	return splitted_text
