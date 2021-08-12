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

sentiment_analyzer_scores("@Uber_Support hi guys why all my trips this week is not being added towards my quest")

# El tema de las exclamaciones influye:
sentiment_analyzer_scores("Uber can’t die fast enough for my liking. It’s a grift, a scam, a money laundering exercise for the Saudi royal family, and it turned a stable regulated occupation (taxi drivers) into a hardscrabble gig economy hustle that impoverished ")
sentiment_analyzer_scores("Uber is fucked. I was out with friends yesterday, and we tried calling an Uber to my friend's place — $55, and we almost resigned to doing it, until I was like, why don't we hail a taxi? And it ended up being $15. Funny Uber's original selling point was being cheaper than taxi")
sentiment_analyzer_scores("This thing is super cool!!!")

# Más pruebas
sentiment_analyzer_scores("How do I get the racist Uber eats to stop emailing me? Reported them as spam a hundred times.")
sentiment_analyzer_scores("love uber drivers that move fast, like yeah bro we’re both tryna get somewhere")
sentiment_analyzer_scores("I just fucking hate uber surge pricing")

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