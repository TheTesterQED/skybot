'''
A Google API key is required and retrieved from the bot config file.
Since December 1, 2011, the Google Translate API is a paid service only.
'''

import htmlentitydefs
import re
from datetime import datetime

from util import hook, http

from util.microsofttranslator import Translator, TranslateApiException

client_id = None
client_secret = None
access_token_time = None
translator = None

#japanese_re = (u'([\u3041-\u3096\u30A0-\u30FF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]+)', re.U)
japanese_re = (u'(.*[\u3041-\u3096\u30A0-\u30FF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]+.*)', re.U)
japanese_compiled_re = re.compile(u'([\u3041-\u3096\u30A0-\u30FF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]+)', re.U)

@hook.regex(*japanese_re)
def found_weeb(match, bot=None):
    pieces = re.split(japanese_compiled_re, match.group(0))
    print match.group(0)
    translated_text = ""
    for piece in pieces:
        if re.match(japanese_compiled_re, piece):
            translated_text += translate(piece, bot)
        else:
            translated_text += piece
    return "I tried translating this, master~ " + translated_text
	

def translate(inp, bot=None):
    # get secrets
    if not client_id or not client_secret:
	if not get_key(bot):
	    return

    # should refresh access token now and then
    if not access_token_time or (datetime.now() - access_token_time).seconds > 500:
        translator = Translator(client_id, client_secret)
    
    #args = inp.split(' ', 2)

    try:
        #if len(args) >= 2:
        #    if len(args) == 2:
        #        return translator.translate(args[1], from_lang=args[0], 'en')
        #    if len(args) >= 3:
        #        return bing_trans(args[2] ' ' + args[2], sl, 'en')
                #return bing_trans(args[2], sl, tl)
        # 1 thing
        return translator.translate(inp, 'en')
    except IOError, e:
        return e

    
def get_key(bot):
    global client_id
    global client_secret
    client_id = bot.config.get("api_keys", {}).get("bing_translate_client_id", None)
    client_secret = bot.config.get("api_keys", {}).get("bing_translate_client_secret", None)
    return client_secret

