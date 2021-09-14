# !wget https://www.clarin.si/repository/xmlui/handle/11356/1048/allzip
# !unzip allzip
# !pip install emoji_extractor
# !pip install emoji
import pandas as pd
import re

from emoji_extractor.extract import Extractor

# Vamosa generar el diccionario de emoticonos 
def load_emoji_sentiment(path):
  # Cargamos el csv de emoji_sentiment
  emoji_sent_df = pd.read_csv(path,sep=",")
  # Calculamos los scores dividiendo el número de emojis negativos y entre el total
  emoji_sent_df["Negative"] = emoji_sent_df["Negative"]/emoji_sent_df["Occurrences"]
  emoji_sent_df["Neutral"] = emoji_sent_df["Neutral"]/emoji_sent_df["Occurrences"]
  emoji_sent_df["Positive"] = emoji_sent_df["Positive"]/emoji_sent_df["Occurrences"]
  # Transformamos a dict
  emoji_sent_df = emoji_sent_df.set_index('Emoji')
  emoji_dict = emoji_sent_df.to_dict(orient="index")
  return emoji_dict


# Función para extraer emojis del texto en formato lista
def extract_emojis(text):
  extract = Extractor()
  emojis = extract.count_emoji(text, check_first=False)
  emojis_list = [key for key, _ in emojis.most_common()]
  return emojis_list


# Calcula el sentimiento de los emojis de una lista utilizando el diccionario
# de emoji sentiment score generado previamente con la función load_emoji_sentiment()
# Se puede extraer el valor de positividad de los emojis con la option "positive"
# Se puede extraer el valor de neutralidad de los emojis con la option "neutral""  
# Se puede extraer el valor de e negatividad de los emojis con la option "negative""  

def get_emoji_sentiment(lista, emoji_sent_dict, option="positive"):
  output = 0
  for emoji in lista:
    try:
      if option == "positive":
        output = output + emoji_sent_dict[emoji]["Positive"]
      elif option =="negative":
        output = output + emoji_sent_dict[emoji]["Negative"]
      elif option =="neutral":
        output = output + emoji_sent_dict[emoji]["Neutral"]
    except Exception as e: 
      continue
  return output


# Eliminar los emojis de un texto. Esto es útil porque una vez extraido los emojis
# puede interesarnos tener un texto sin presencia de emojis para mejor análisis.
def clean_emoji(text):
    # Poner todos los comandos de http://www.unicode.org/Public/emoji/1.0/emoji-data.txt
    emoji_pattern = re.compile("["
        u"\U0001F300-\U0001F6FF"  # symbols & pictographs
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u'\u2600-\u26FF\u2700-\u27BF'
        u'\u2934' u'\u2935' u'\u2B05' u'\u2B06' u'\u2B07' u'\u2B1B' u'\u2B1C' 
        u'\u2B50' u'\u2B55' u'\u3030' u'\u303D' u'\u3297' u'\u3299' u'\u00A9'
        u'\u00AE' u'\u203C' u'\u2049' u'\u2122' u'\u2139' u'\u2194-\u2199' 
        u'\u21A9' u'\u21AA' u'\u231A' u'\u231B' u'\u2328' u'\u23CF'
        u'\u23E9-\u23F3' u'\u23F8' u'\u23F9' u'\u23FA' u'\u24C2' u'\u25AA'
        u'\u25AB' u'\u25B6' u'\u25C0' u'\u25FB' u'\u25FD' u'\u25FC' u'\u25FE'
        ']+', flags=re.UNICODE)
    string2 = re.sub(emoji_pattern,r' ',text)
    return string2

# Pasamos los emoji a Unicode

def emoji_to_unicode(lista_emojis, emoji_sent_dict):
  resultado = []
  if len(lista_emojis) == 0:
    return resultado
  else:
    for emoji in lista_emojis:
      if emoji in emoji_sent_dict:
        res = format(ord(emoji))
        resultado.append(res)
      else:
        resultado.append(' ')
    return resultado


def emoji_treatment(df):
    emoji_sent_dict =  load_emoji_sentiment(r'Emoji_Sentiment_Data_v1.0.csv')
    # Vamos a trabajar primero con los emojis
    df["emoji_list"] = df["text"].apply(lambda x: extract_emojis(x))
    df["sent_emoji_pos"] = df["emoji_list"].apply(lambda x: get_emoji_sentiment(x, emoji_sent_dict, "positive"))
    df["sent_emoji_neu"] = df["emoji_list"].apply(lambda x: get_emoji_sentiment(x, emoji_sent_dict, "neutral"))
    df["sent_emoji_neg"] = df["emoji_list"].apply(lambda x: get_emoji_sentiment(x, emoji_sent_dict, "negative"))

    # Creamos una variable unicode
    df['emoji_unicode'] = df["emoji_list"].progress_apply(lambda x: emoji_to_unicode(x, emoji_sent_dict))
    return df
