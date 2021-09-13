########################
# CARGA DE LIBRERIAS
########################

import streamlit as st
from streamlit_lottie import st_lottie
import numpy as np
import pandas as pd
import time
import datetime
import requests
import base64
from nlp import to_lower, tokenization, quitar_stopwords, quitar_puntuacion, en_core_web_sm, lematizar
from nltk.tokenize import word_tokenize
import io
from ast import literal_eval
from tqdm.autonotebook import tqdm
tqdm.pandas()

from data_retrieval import api, api_tweets, dataframe_creation
from cleaning import drop_unnamed, drop_cols_wo_value, num_cols_treatment, is_reply_treat, source_device_treat
from modelling import get_final_output
from location import location_treatment
from topic import get_topic
from variable_obj import calc_media, standarize
from emoji import emoji_treatment


###################################
# FORMATOS GENERALES APLICACION
###################################

# FORMATO DE PÁGINA CENTRAD0
#################################
st.set_page_config(layout="centered")

# SIDEBAR
###########
# @@@ Añadir otras opciones
# @@@ Redirección a los sitio
# sidebar_option = st.sidebar.selectbox("MENU (A implementar?)", ("Aplicación", "Sobre el proyecto"))

# IMAGEN DE FONDO
###################
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fgetjar.co.uk%2Fwp-content%2Fuploads%2F2018%2F07%2F4855789-white-background-images-1.jpg&f=1&nofb=1")
    }
    }
    </style>
    """,
    unsafe_allow_html=True
)

#############################
# TÍTULOS Y DESCRIPCIONES
#############################

# LOGO DE TWITTER
###################
def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

lottie_twitter = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_ayl5c9tf.json')
st_lottie(lottie_twitter, speed=0.75, height=180, key="initial")

st.title("APLICACIÓN UBER")
st.subheader("Bienvenido.")
st.write("Esta aplicación te permite obtener un análisis de sentimiento de forma interactiva")
with st.expander("Más información:"):
    st.write("""Como comprobará la aplicación es muy intuitiva. Por favor siga las instrucciones que \
                le proporcionamos en cada momento. El usuario comenzará rellenando las opciones que \
                consideré oportunas en el formulario; después deberá esperar a que se genere el modelado \
                y los entregables que haya requerido. Para saber en todo momento en que punto del proceso se encuentra, \
                se han creado una barras de progreso y checklists.
                """)

#####################################
# INPUT PARA EL RESTO DEL PROCESO
#####################################

# Dejamos por defecto search_words y lang
search_words = ("uber")
lang = "en"

# Submit button con forms para date y n_tweets
# Se limitan las fechas que podemos elegir a 7 días respecto a hoy
# if 'session' not in st.session_state:
#     st.session_state.session = 0 --> para guardar variables entre sesiones

today = datetime.date.today()
with st.form(key='my_form'):
    st.subheader("FORMULARIO OBTENCIÓN DE DATOS")
    col1, col2, col3 = st.columns((10, 1, 10))
    
    ## OBTENCIÓN DE DATOS
    with col1:
        # Desde cuándo queremos tweets
        date = st.date_input("Elija la fecha hasta la que quieras extraer tweets:",
                            min_value= (today - datetime.timedelta(days=7)),                                    # Limitacion de los dias aquí
                            max_value= today)
    with col2: pass
    with col3:
        # Número de tweets
        n_tweets = st.slider("Cuántos tweets quiere extraer:", max_value=10000, min_value=1, value=5, step=5)    # Se podrían modificar valores
        
    ## DESCARGA DE DATOS 
    statuses = st.radio(
        'Quieres obtener tus datos en a archivo?',
        ('Sí. Quisiera descargarlos en .csv', 'Sí. Quisiera descargarlos en .xslx', 'No. Estoy bien así')
        )

    st.write("__________________________________________________________________________________")
    
    ## M0DELIZACIÓN Y ENTREGABLES
    st.subheader("FORMULARIO MODELIZACIÓN Y ENTREGABLES")
    col1, col2 = st.columns((3, 2))
    with col1:
        statuses2 = st.radio(
            'Qué tipo de estudio quieres realizar?',
            ('Análisis de sentimiento', 'Análisis de sentimiento + Topic Modelling'))
    with col2:
        option2 = st.multiselect(
            'Qué librerías quieres seleccionar para ello?',
            ["VADER", "TEXTBLOB", "IBM WATSON"])
    option3 = st.multiselect(
    'Qué visualizaciones quieres de tu análisis?',
    ["DASHBOARD IN SITU MEDIANTE MATPLOTLIB", "DASHBOARD DE TABLEAU", "DASHBOARD DE POWERBI"])
    
    submit_button = st.form_submit_button(label='Enviar e Iniciar el Modelo')

with st.expander("Has seleccionado"):
    st.write("Has seleccionado realizar un {} empleando para ello las librerías {}.".format(statuses2, ", ".join(option2)))
    

# Hasta que no apretamos submit no continúa el programa
if submit_button:
    # Llamamos a la función de api_tweets (archivo data_retrieval.py)
    tweets = api_tweets(search_words, lang, date, n_tweets)

    st.write("__________________________________________________________________________________")

################################
    # CREACIÓN DEL DATAFRAME
################################

    # Llamamos a la función de dataframe_creation (archivo data_retrieval.py)
    st.subheader("CREACIÓN DE TU DATAFRAME")
    st.write("Creando tu DataFrame. Por favor espera...")

    df = dataframe_creation(tweets, n_tweets)
    st.dataframe(df)

    st.write("__________________________________________________________________________________")

#################################
    # LIMPIEZA DEL DATAFRAME
#################################

    # Hacer como una serie de check list para ver lo que se ha ido haciendo
    st.subheader("LIMPIEZA DE TU DATAFRAME")
    st.write("Limpiando tu DataFrame. Por favor espera...")

    st.markdown("""
                <style>
                .small-font {
                    font-size:16px;
                }
                </style>
                """, unsafe_allow_html=True)

    st.markdown('<p class="small-font">☑️ <i>Dropeadas variables unnamed</i></p>', unsafe_allow_html=True)
    df = drop_unnamed(df)

    st.markdown('<p class="small-font">☑️ <i>Dropeadas variables que no aportan información</i></p>', unsafe_allow_html=True)
    cols = ['user_ verified','user_withheld_in_countries','finished_tweet', 'created_at_time']
    df = drop_cols_wo_value(df, cols)

    st.markdown('<p class="small-font">☑️ <i>Eliminados outliers en variables numéricas</i></p>', unsafe_allow_html=True)
    num_cols = df[df.select_dtypes(['int64']).columns].keys()
    df = num_cols_treatment(df, num_cols)

    st.markdown('<p class="small-font">☑️ <i>Creada y tratada la variable de localización</i></p>', unsafe_allow_html=True)
    df = location_treatment(df)

    st.markdown('<p class="small-font">☑️ <i>Tratada la variable is_reply</i></p>', unsafe_allow_html=True)
    df = is_reply_treat(df)

    st.markdown('<p class="small-font">☑️ <i>Tratada la variable source_device_treat</i></p>', unsafe_allow_html=True)
    df = source_device_treat(df)

    st.dataframe(df)

###############################################################
    # DESCARGA DE FICHEROS PARA EL CASO QUE SE HAYA PEDID0
###############################################################

    def get_csv_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="datos_limpios.csv">Descarga archivo csv</a>'
        return href


    def get_excel_link(df):
        towrite = io.BytesIO()
        downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  
        b64 = base64.b64encode(towrite.read()).decode()
        href= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="datos_limpios.xlsx">Descarga archivo excel</a>'
        return href


    # If-statement to know what file do we need to download
    if statuses == "Sí. Quisiera descargarlos en .csv":
        st.markdown(get_csv_link(df), unsafe_allow_html=True)
    elif statuses == "Sí. Quisiera descargarlos en .xslx":
        st.markdown(get_excel_link(df), unsafe_allow_html=True)
    else:
        pass
    
    st.write("__________________________________________________________________________________")
    
##########################   
    # MODELADO
##########################

    st.subheader("MODELADO DE TUS DATOS")
    st.write("Modelando tus datos. Por favor espera...")

    my_bar2 = st.progress(0)
    i = 0

    # PROCESAMIENTO EMOJIS
    df = emoji_treatment(df) # Llamada a la función de emoji.py
    my_bar2.progress(0.2)
    time.sleep(0.2)

    # PROCESAMIENTO NLP

    df['text_limpio'] = df['text'].apply(lambda x: to_lower(x))

    df['text_limpio'] = df['text_limpio'].progress_apply(lambda x: tokenization(x))

    df['text_limpio'] = df['text_limpio'].progress_apply(lambda x: quitar_stopwords(x))

    df['text_limpio'] = df['text_limpio'].progress_apply(lambda x: quitar_puntuacion(x))

    df['text_limpio'] = df['text_limpio'].progress_apply(lambda x: lematizar(x))

    # Columna con el número de carácteres que tiene cada opinión
    df['caracteres'] = df['text_limpio'].apply(lambda x: len(x))

    # Columna con el número de tokens que tiene cada opinión
    df['tokens'] = df['text_limpio'].apply(lambda x: len(word_tokenize(x)))
    my_bar2.progress(0.3)
    time.sleep(0.2)

    # LIBRERIAS DE SENTIMIENTO DE ANÁLISIS
    # Habría que meter barra de progreso (no hay for loop): https://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations
    df = get_final_output(df)
    my_bar2.progress(0.5)
    time.sleep(0.2)

    # TOPIC
    if statuses2 == "Análisis de sentimiento + Topic Modelling":
        df['topic'] = df['result_ibm'].progress_apply(lambda x: get_topic(x))
    my_bar2.progress(0.6)
    time.sleep(0.2)

    df = df.loc[df['possitivity_ibm']!=9999]

    # ESTANDARIZADO
    df = standarize(df)
    my_bar2.progress(0.8)
    time.sleep(0.2)

    # CREACIÓN DE LA VARIABLE OBJETIVO
    sentimientos = ['textblob_norm','vader_norm','ibm_norm','emoji_norm']
    df['var_obj_cont'] = df[sentimientos].apply(lambda x: calc_media(x['textblob_norm'],x['vader_norm'],x['ibm_norm'],x['emoji_norm']),axis=1)
    my_bar2.progress(1.0)

    st.dataframe(df)

    # Descarga final 
    if statuses == "Sí. Quisiera descargarlos en .xslx":
        st.markdown(get_excel_link(df), unsafe_allow_html=True)
    else: # "Sí. Quisiera descargarlos en .csv" & "No. Estoy bien así"
        st.markdown(get_csv_link(df), unsafe_allow_html=True)

    st.write("__________________________________________________________________________________")

    # GENERACIÓN DE ENTREGABLES
    ##########################
    st.subheader("GENERACIÓN DE TUS DASHBOARDS")
    st.write("Creando tus dashboards. Por favor espera...")