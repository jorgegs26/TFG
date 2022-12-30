import tweepy
from tweepy.auth import OAuthHandler
import re
import emoji
from tqdm.auto import tqdm

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

# Función para obtener los tweets, el usuario y la fecha de creación en horario utc
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

    tweets = []
    
    print('Descargando', num_tweets, 'tweets en bloques de 100 en 100...')
    
    for i, tweet in enumerate(tqdm(tweepy.Cursor(api.search_tweets, q=query, result_type='mixed', tweet_mode='extended', count=100).items(num_tweets))):
        print('', end='\r')
        info = []
        text = delete_urls(tweet.full_text)
        text = delete_icons(text)
        info.append(text)
        info.append(tweet.user.screen_name)
        info.append(str(tweet.created_at))
        tweets.append(info)
        #print(i, tweet.id)
    print()
    
    print()
    
    return tweets # El formato de la lista será el siguiente: [[tweet,user,date],[tweet,user,date]...]

# Función para separar las frases de un párrafo. Esto es necesario para formar las entidades y relaciones del gráfico de conocimiento
def split_in_sentences(text):
    aux = text.replace('\n','.') # Sustituimos los saltos de línea por el caracter '.' ya que muchos usuarios separan sus frases solo con un intro
    splitted_text = aux.split('.')
    return splitted_text
