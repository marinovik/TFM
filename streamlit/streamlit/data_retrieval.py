import os
import tweepy as tw
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from tqdm import tqdm
import streamlit as st
import openpyxl
import time


# Credenciales para el uso de la API
consumer_key= 'JFQSBpo6mDLNPSMMLFhWtQ292'
consumer_secret= 'BGOFWrICQmpul1nDTqkNPwLvgsy2MrxWVbViyZUBxo83MG2ihu'
access_token= '1267192889416847362-6V8ZXpbObheh2BOXtVPUMjjIZ6Xrz4'
access_token_secret= 'atrDg3MPQrxvCP5XSuF7z1H7PzHiovO2PgO1Nl8QbeP8t'

# Llamamos a la API
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Creamos una función que nos devuelve la información de los tweets que deseamos
# date indica la fecha a partir de de la cual empieza a extraer tweets. 
# Los tweets se extraen de más reciente a más antiguo. Por lo tanto esta fecha es "hasta". 
# La fecha "desde" la dejamos sin indicar.api_call


def api_tweets(key_words, language, date, n_tweets):
  result = tw.Cursor(api.search,
                    q=key_words,
                    lang=language,
                    until=date,
                    tweet_mode='extended').items(n_tweets)
  return result


def dataframe_creation(tweets, n_tweets):
    my_bar = st.progress(0)

    # Creamos un df vacío con las columnas que vamos a completar
    df = pd.DataFrame(columns=['text', 'created_at', 'created_at_time', 'created_at_hour', 'retweeted', 'retweet_count', 'favorite_count', 
                           'user_ verified', 'user_id', 'user_name', 'user_location', 'user_notificacion', 'user_followers', 'user_friends', 
                           'user_withheld_in_countries', 'mentions_in_tweet', 'is_reply', 'source_device', 'finished_tweet', 
                           'status_count', 'hashtags_text','hastags_indices', 'hastags_in_tweet'])

    i = 0
    for tweet in tweets:
        # Convertimos el json de cada uno de los tweets en un diccionario
        tweet_d = dict(tweet._json)

        # Creo un estado para coger el texto completo
        status = api.get_status(tweet_d['id'], tweet_mode="extended")
        try:
            text = status.retweeted_status.full_text
            rt = 'Si'
        except AttributeError:  # Not a Retweet
            text = status.full_text
            rt = 'No'

        # Creamos una variable que nos dice el número de menciones en el tweet
        try:
            mentions_in_tweet = len(tweet_d['entities']['user_mentions'])
        except:
            mentions_in_tweet = 0

        # Creamos una variable que nos dice si el tweet es una respuesta
        if tweet_d['in_reply_to_screen_name'] == None:
            reply = 'No'
        else:
            reply = tweet_d['in_reply_to_screen_name']

        # Cogemos la fecha del tweet y dividimos en día y hora
        fecha_completa = str(tweet_d['created_at'])
        fecha = fecha_completa.split(sep = ' ')
        texts_date = ' '.join(elemento for elemento in fecha[0:3])
        texts_time = fecha[3] 

        # Creamos una columna que corresponde con las horas, para representarla
        hora = fecha[3].split(sep = ':')
        texts_hour = int(hora[0])

        # Exportamos los hastag del tweet y las posiciones
        aux = list([i["text"] for i in tweet.entities['hashtags']]) 
        aux_pos = [i["indices"] for i in tweet.entities['hashtags']]

        # Creamos una fila con la información que queremos almacenar de cara al análisis
        new_row = {
            
        'text': text,

        'created_at': texts_date,
        'created_at_time': texts_time,
        'created_at_hour': texts_hour,

        'retweeted': rt,

        'retweet_count': tweet_d['retweet_count'],
        'favorite_count': tweet_d['favorite_count'],

        'user_verified': tweet_d['user']['verified'], # ---------------------- ALGO PASA CON ESTO, DEVUELVE TODO NaN
        'user_id': tweet_d['user']['id'],
        'user_name': tweet_d['user']['screen_name'],
        'user_location': tweet_d['user']['location'],
        'user_notificacion': tweet.user.notifications,
        'user_followers': tweet_d['user']['followers_count'],
        'user_friends': tweet_d['user']['friends_count'],
        'user_withheld_in_countries':  tweet.user.withheld_in_countries,

        'mentions_in_tweet': mentions_in_tweet,   
        'is_reply': reply,

        'source_device':tweet.source,
        'finished_tweet': tweet.truncated, # Si está incompleto el tweet (hilo)

        'status_count':tweet.user.statuses_count, # ¿QUÉ ES ESTO? interacciones del usuario tanto tweets como retweets 

        'hashtags_text': aux,
        'hastags_indices': aux_pos,
        'hastags_in_tweet': len(aux)

        }

        # Añadimos la info al dataframe en una nueva fila
        df.loc[i] = new_row
        i = i + 1
        j = (i / n_tweets)
        time.sleep(0.1)
        my_bar.progress(j)

    return df
