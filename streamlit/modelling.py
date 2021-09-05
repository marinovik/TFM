from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import pandas as pd
import numpy as np
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, ConceptsOptions, EmotionOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SentimentOptions


def get_textblob_score(tweet):
    return TextBlob(tweet).sentiment.polarity


def get_vader_score(tweet):
    analyser = SentimentIntensityAnalyzer()
    return float(analyser.polarity_scores(tweet)['compound'])


nlu_apikey = "-AqVH2-6FPhc1fTcVHf9WHQXok1CCHul044GKRgQMi_a"
nlu_url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/07732151-0ad7-45f7-af60-85562116af50"

authenticator = IAMAuthenticator(nlu_apikey)
natural_language_undestanding = NaturalLanguageUnderstandingV1(version = '2020-08-01', 
                                                               authenticator = authenticator
)
natural_language_undestanding.set_service_url(nlu_url)


def get_ibm_score(tweet):
  try: 
    aux = natural_language_undestanding.analyze(text=tweet, features=Features(keywords=KeywordsOptions(), 
                                                            entities=EntitiesOptions(), 
                                                            categories=CategoriesOptions(),
                                                            emotion=EmotionOptions(),
                                                            sentiment=SentimentOptions())).get_result()['sentiment']['document']['score']
    return float(aux)
  except:
    return 9999


def media(num1,num2,num3):
  a = 1/3
  b = 1/3
  c = 1/3
  m = a*float(num1) + b*float(num2) + c*float(num3)
  return m
  

def get_final_output(df):
    df['possitivity_textblob'] = df['text'].apply(lambda x: get_textblob_score(x))
    df['possitivity_vader'] = df['text'].apply(lambda x: get_vader_score(x))
    df['possitivity_ibm'] = df['text'].apply(lambda x: get_ibm_score(x))
    return df


def scaler(numero):
    min = -1
    max = 1
    result = (numero - min) / (max - min)
    return result


def new_categorical_variable(df):
    variables = ['possitivity_textblob','possitivity_vader','possitivity_ibm']
    df['sentiment_mean'] = df[variables].apply(np.mean, axis=1)
    df['sentiment_norm'] = df['sentiment_mean'].apply(lambda x: scaler(x))
    bins = [0, .2, .4, .6, .8, 1.]
    # Definimos los nombres para cada categoría
    names = ["Muy negativo", "Negativo", "Neutro", "Positivo", "Muy positivo"]
    # Creamos la variable objetivo categórica
    df['sentiment'] = pd.cut(df['sentiment_norm'], bins, labels = names)
    return df
