from get_tweets_Cursor import get_full_tweets
from translate import translate_list
import pymongo

# Función para borrar una BD
def delete_database(name, myclient):
	myclient.drop_database(name)

# Función para borrar una colección de la BD "TFG"
def delete_collection(name, mydb):
	mycol = mydb[name]
	mycol.drop()

# Función para insertar los tweets en la colección que se situa en la BD "TFG"
def insert_data(list_data, name, mydb):
	print('Guardando los tweets en la base de datos...')
	mycol = mydb[name]
	for record in list_data:
		if len(record) == 3:
			tweet = record[0]
			user = record[1]
			date = record[2]
			data = { "tweet": tweet, "user": user, "date": date }
			found_data = mycol.find(data) # Buscamos si existe un registro igual en la BD para evitar datos duplicados
			if len(list(found_data)) == 0:
				x = mycol.insert_one(data)

# SE TENDRÁ QUE SUSTITUIR ESTE MÉTODO EN EL GRAPH KNOWLEDGE
def print_bbdd(name, mydb):
	mycol = mydb[theme_of_search]
	myresult = mycol.find()
	for i in myresult:
		print(i)


# INDICAR QUERY QUE HAY QUE BUSCAR Y NUMERO DE TWEETS
theme_of_search = 'Rusia'
number_of_tweets = 1

tweets = get_full_tweets(theme_of_search, number_of_tweets)
translated_tweets = translate_list(tweets, 'en')
    
myclient = pymongo.MongoClient('mongodb://f-l2108-pc01.aulas.etsit.urjc.es:21502/')
mydb = myclient["TFG"]

insert_data(translated_tweets, theme_of_search, mydb)
