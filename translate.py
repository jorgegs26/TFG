# from urllib.parse import urlencode
# from urllib.request import urlopen, Request
# import re
# import json

# def get_google_translate(text, translate_lang, source_lang=None):
    # if source_lang == None:
        # source_lang= 'auto'
        
    # params = urlencode({'client':'t', 'tl':translate_lang, 'q':text.encode('utf-8'),'sl':source_lang})
    # http_headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)"}
    # request_object = Request('http://translate.google.com/translate_a/t?'+params, None, http_headers)
    
    # try:
        # response = urlopen(request_object)
        # string = re.sub(',,,|,,',',"0",', response.read())
        # n = json.loads(string)
        # translate_text = n[0][0][0]
        # res_source_lang = n[2]
        # return True, res_source_lang, translate_text    
    # except Exception as e:
        # return False, '', str(e)

from googletrans import Translator

def get_translation(text, lang):
	translator = Translator()
	try:
		info = translator.translate(text, dest=lang)
		return info.text, info.src
	except Exception as e:
		return str(e), ''
