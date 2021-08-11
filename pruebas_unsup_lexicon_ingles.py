import numpy as np
import pandas as pd

# Primero tenemos la opcion de vader
# Se trata de un lexicon 

# Instalar mediante pip si es necesario:
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

sentiment_analyzer_scores("This thing is not that bad")

# El tema de las exclamaciones influye:
sentiment_analyzer_scores("This thing is super cool!")
sentiment_analyzer_scores("This thing is super cool!!")
sentiment_analyzer_scores("This thing is super cool!!!")

# Más pruebas
sentiment_analyzer_scores("Food here is good.")
sentiment_analyzer_scores("Food here is horrible.")
sentiment_analyzer_scores("Food here is extremely good.")

# Frases compuestas
sentiment_analyzer_scores("Food here is extremely good but service is horrible.")

# Emotis
print(sentiment_analyzer_scores('I was 😄 yesterday, but today is a horrible day'))
print(sentiment_analyzer_scores('😊'))
print(sentiment_analyzer_scores('😥'))
print(sentiment_analyzer_scores('☹️'))
print(sentiment_analyzer_scores("Make sure you :) or :D today!"))

# Slangs
print(sentiment_analyzer_scores("Today SUX!"))
print(sentiment_analyzer_scores("Today only kinda sux! But I'll get by, lol"))