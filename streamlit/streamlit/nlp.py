# Importamos pandas y numpy 
import pandas as pd
import numpy as np
from tqdm.autonotebook import tqdm
tqdm.pandas()
import string
import seaborn as sns
import matplotlib.pyplot as plt
import sys 
# import contractions  
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
# Instalamos spacy y su modelo pre-entrenado en inglés
import spacy
import en_core_web_sm

## !{sys.executable} -m pip install contractions
# !pip install spacy
# !python -m spacy download en_core_web_sm


def to_lower(text):
  return text.lower()


def tokenization(text):
  tokens = word_tokenize(text)
  return tokens


def quitar_stopwords(tokens):
  stop_words = set(stopwords.words('english'))
  filtered_sentence = [w for w in tokens if not w in stop_words]
  return filtered_sentence


def quitar_puntuacion(tokens):
  words = [word for word in tokens if word.isalnum()]
  return words


def lematizar(tokens):
  nlp = en_core_web_sm.load()
  sentence = ' '.join(tokens)
  mytokens = nlp(sentence)
  mytokens = [word.lemma_ if word.lemma_ != '-PRON-' else word.lower_ for word in mytokens]
  return ' '.join(mytokens)

