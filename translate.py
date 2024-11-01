# from googletrans import Translator

from deep_translator import GoogleTranslator


def translate_text(text,lang):
    dest1='en'
    if lang == "English":
        return text
    elif lang== "Hindi":
        dest1='hi'
    elif lang== "Gujarati":
        dest1='gu'    
    elif lang=="Kannada":
        dest1='kn'    
    elif lang=="tamil":
        dest1="ta"    
    result = GoogleTranslator(source='en', target=dest1).translate(text)
    return result

# print(translate_text("hello i am sad","Hindi"))

