from googletrans import Translator
from tqdm.auto import tqdm

# Función para traducir un texto proporcionado a un determinado idioma
def get_translation(text, lang):
	translator = Translator()
	try:
		info = translator.translate(text, dest=lang)
		return info.text, info.src
	except Exception as e:
		return str(e), ''
		
# Función para traducir una lista de textos a un determinado idioma
def translate_list(listToTranslate, lang):
    translated_list = []
    count = 0
    num = len(listToTranslate)
    print('Traduciendo', num, 'tweets...')
    error = 0
    
    for i in tqdm(range(num)):
        tweet = listToTranslate[count]
        info = []
        tr_text, language = get_translation(tweet[0], lang)
        print('', end='\r')
        if(language != ''):
            #print('Tweet nº: ', str(count) ,' - Idioma origen: ', language, ' - Texto: ', tr_text)
            info.append(tr_text)
            info.append(tweet[1])
            info.append(tweet[2])
            translated_list.append(info)
        else:
            error = error + 1
        count = count + 1
    
    if error != 0:
        print('Número de tweets no traducidos:', error)
    
    return translated_list # El formato de la lista será el siguiente: [[tweet_traducido,usuario,fecha],[tweet_traducido,usuario,fecha]...]
