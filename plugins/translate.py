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

########### from http://effbot.org/zone/re-sub.htm#unescape-html #############
'''

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)

##############################################################################

def bing_trans(text, slang, tlang):
    url = 'https://www.googleapis.com/language/translate/v2'
    parsed = http.get_json(
        url, key=api_key, q=text, source=slang, target=tlang)
    if not 200 <= parsed['responseStatus'] < 300:
        raise IOError('error with the translation server: %d: %s' % (
            parsed['responseStatus'], parsed['responseDetails']))
    if not slang:
        return unescape('(%(detectedSourceLanguage)s) %(translatedText)s' %
                        (parsed['responseData']['data']['translations'][0]))
    return unescape('%(translatedText)s' % parsed['responseData']['data']['translations'][0])


def match_language(fragment):
    fragment = fragment.lower()
    for short, _ in lang_pairs:
        if fragment in short.lower().split():
            return short.split()[0]

    for short, full in lang_pairs:
        if fragment in full.lower():
            return short.split()[0]

    return None
'''

@hook.command
def translate(inp, bot=None):
    '.translate [source language [target language]] <sentence> -- translates' \
        ' <sentence> from source language (default autodetect) to target' \
        ' language (default English) using Bing Translate' \
        ' Blah blah Im lazy just does autodetect to English right now'

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

languages = []

'''languages = 'ja fr de ko ru zh'.split()
language_pairs = zip(languages[:-1], languages[1:])


lang_pairs = [
    ("no", "Norwegian"),
    ("it", "Italian"),
    ("ht", "Haitian Creole"),
    ("af", "Afrikaans"),
    ("sq", "Albanian"),
    ("ar", "Arabic"),
    ("hy", "Armenian"),
    ("az", "Azerbaijani"),
    ("eu", "Basque"),
    ("be", "Belarusian"),
    ("bg", "Bulgarian"),
    ("ca", "Catalan"),
    ("zh-CN zh", "Chinese"),
    ("hr", "Croatian"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("nl", "Dutch"),
    ("en", "English"),
    ("et", "Estonian"),
    ("tl", "Filipino"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("gl", "Galician"),
    ("ka", "Georgian"),
    ("de", "German"),
    ("el", "Greek"),
    ("ht", "Haitian Creole"),
    ("iw", "Hebrew"),
    ("hi", "Hindi"),
    ("hu", "Hungarian"),
    ("is", "Icelandic"),
    ("id", "Indonesian"),
    ("ga", "Irish"),
    ("it", "Italian"),
    ("ja jp jpn", "Japanese"),
    ("ko", "Korean"),
    ("lv", "Latvian"),
    ("lt", "Lithuanian"),
    ("mk", "Macedonian"),
    ("ms", "Malay"),
    ("mt", "Maltese"),
    ("no", "Norwegian"),
    ("fa", "Persian"),
    ("pl", "Polish"),
    ("pt", "Portuguese"),
    ("ro", "Romanian"),
    ("ru", "Russian"),
    ("sr", "Serbian"),
    ("sk", "Slovak"),
    ("sl", "Slovenian"),
    ("es", "Spanish"),
    ("sw", "Swahili"),
    ("sv", "Swedish"),
    ("th", "Thai"),
    ("tr", "Turkish"),
    ("uk", "Ukrainian"),
    ("ur", "Urdu"),
    ("vi", "Vietnamese"),
    ("cy", "Welsh"),
    ("yi", "Yiddish")
]
'''
