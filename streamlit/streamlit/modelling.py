from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from ast import literal_eval
import pandas as pd
import numpy as np
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, ConceptsOptions, EmotionOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SentimentOptions

# !pip install textblob
# !pip install vaderSentiment
# !pip install watson_developer_cloud
# !pip install ibm_watson
# pip install --upgrade "ibm-watson>=5.1.0"

def get_textblob_score(tweet):
    return TextBlob(tweet).sentiment.polarity


def get_vader_score(tweet):
    analyser = SentimentIntensityAnalyzer()
    return float(analyser.polarity_scores(tweet)['compound'])


def get_ibm_score(tweet):
  # Credenciales nuevas
  nlu_apikey = "kVVp9_RBkUdyY9QltUQ6CNZC48mrT1CsfxdeTWKofT4P"
  nlu_url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/43171466-a5dc-47ac-97d7-d50661534772"

  authenticator = IAMAuthenticator(nlu_apikey)
  natural_language_undestanding = NaturalLanguageUnderstandingV1(
      version = '2020-08-01', 
      authenticator = authenticator
  )
  natural_language_undestanding.set_service_url(nlu_url)

  try: 
    aux = natural_language_undestanding.analyze(text=tweet, features=Features(keywords=KeywordsOptions(), 
                                                                entities=EntitiesOptions(), 
                                                                categories=CategoriesOptions(),
                                                                emotion=EmotionOptions(),
                                                                sentiment=SentimentOptions())).get_result()
    return aux
    
  except:
      return 9999


def sentiment_ibm(string):
    try:
        aux = literal_eval(string)
        x = float(aux['sentiment']['document']['score'])
    except:
        x = '9999'
    return x


def get_final_output(df):
    df['possitivity_textblob'] = df['text_limpio'].apply(lambda x: get_textblob_score(str(x)))
    df['possitivity_vader'] = df['text_limpio'].apply(lambda x: get_vader_score(str(x)))
    df['result_ibm'] = df['text_limpio'].apply(lambda x: get_ibm_score(str(x)))
    df['possitivity_ibm'] = df['result_ibm'].progress_apply(lambda x: sentiment_ibm(str(x)))
    # Eliminamos los que tienen un 9999 en result_ibm porque no están en inglés
    df = df[df['result_ibm'] !='9999']
    return df