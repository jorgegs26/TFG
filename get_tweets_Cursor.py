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
    API_KEY = ''
    API_SECRET_KEY = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''

    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	
    api = tweepy.API(auth)
    query = query + ' -filter:retweets' # Añadimos el filtro para evitar recuperar rts, solo nos interesan tweets escritos para no obtener ningún duplicado

    # El result_type es para sacar los tweets que tienen mayor importancia en la reed
    # El tweet_mode es para recuperar el tweet completo
    tweets = []
    num = int(num_tweets/100)+1
    tweets_to_search = num_tweets
    j = 0
    
    print('Descargando', num_tweets, 'tweets en bloques de 100 en 100...')
    
    for i in tqdm(range(num)):
    #while j < num:
        print('', end='\r')
        if(tweets_to_search >= 100):
            #print('El numero de tweets descargados es ', str(j), '/', str(num), ', descargando 100 más...')
            for i in tweepy.Cursor(api.search_tweets, q=query, count=100, tweet_mode='extended').items(100):
                info = []
                text = delete_urls(i.full_text)
                text = delete_icons(text)
                info.append(text)
                info.append(i.user.screen_name)
                info.append(str(i.created_at))
                tweets.append(info)
            j = j + 100
            tweets_to_search = tweets_to_search - 100
        else:
            #print('El numero de tweets descargados es ', str(j), '/', str(num), ', descargando los ', str(num-j), ' restantes...')
            for i in tweepy.Cursor(api.search_tweets, q=query, count=tweets_to_search, tweet_mode='extended').items(tweets_to_search):
                info = []
                text = delete_urls(i.full_text)
                text = delete_icons(text)
                info.append(text)
                info.append(i.user.screen_name)
                info.append(str(i.created_at))
                tweets.append(info)
            j = j + tweets_to_search
    
    print()
    
    return tweets # El formato de la lista será el siguiente: [[tweet,usuario,fecha],[tweet,usuario,fecha]...]

# Función para separar las frases de un párrafo. Esto es necesario para formar las entidades y relaciones del gráfico de conocimiento
def split_in_sentences(text):
    aux = text.replace('\n','.') # Sustituimos los saltos de línea por el caracter '.' ya que muchos usuarios separan sus frases solo con un intro
    splitted_text = aux.split('.')
    return splitted_text
