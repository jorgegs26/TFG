from googletrans import Translator

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
	for text in listToTranslate:
		tr_text, language = get_translation(text, lang)
		if(language != ''):
			#print('Language src: ', language, '- Text: ', tr_text)
			translated_list.append(tr_text)
	return translated_list
