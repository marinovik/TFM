import streamlit as st
from streamlit_lottie import st_lottie
import numpy as np
import pandas as pd
import time
import datetime
import requests
from data_retrieval import api, api_tweets, dataframe_creation
import base64
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from modelling import get_final_output, new_categorical_variable, scaler

# HOY
# Limpieza 
# Descarga

# FORMATO DE PÁGINA QUE OCUPE TOD0
####################################
st.set_page_config(layout="centered")


# SIDEBAR
###########
# @@@ Añadir otras opciones
# @@@ Redirección a los sitio
sidebar_option = st.sidebar.selectbox("MENU", ("Aplicación", "Sobre el proyecto"))


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


# TÍTULOS Y DESCRIPCIONES
###########################

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
st.write("Esta aplicación te permite obtener un sentimiento de análisis de forma interactiva")
with st.expander("Más información:"):
    st.write("""Como comprobará la aplicación es muy intuitiva. Por favor siga las isntrucciones que \
                le proporcionamos en cada momento. El usuario comenzará rellenando las opciones que \
                consideré oportunas en el formulario; después deberá esperar a que se genere el modelado \
                y los entregables que haya requerido. Para saber en todo momento en que punto se encuentra \
                el proceso se ha creado una barra de progreso.
                """)



# INPUT PARA EL RESTO DEL PROCESO
####################################

# Dejamos por defecto search_words y lang
search_words = ("uber")
lang = "en"

# Submit button con forms para date y n_tweets
# Se limitan las fechas que podemos elegir a 7 días respecto a hoy
today = datetime.date.today()
with st.form(key='my_form'):
    st.subheader("FORMULARIO OBTENCIÓN DE DATOS")
    col1, col2, col3 = st.columns((10, 1, 10))
    ## OBTENCIÓN DE DATOS
    

    with col1:
        # Desde cuándo queremos tweets
        date = st.date_input("Elija la fecha hasta la que quieras extraer tweets:",
                            min_value= (today - datetime.timedelta(days=7)),                                    # Limitacion de los dias aqui
                            max_value= today)
    with col3:
        # Número de tweets
        n_tweets = st.slider("Cuántos tweets quiere extraer:", max_value=5000, min_value=1, value=1, step=1)    # Se podrían modificar valores

    ## DESCARGA DE DATOS
    statuses = st.radio(
        'Quieres obtener tus datos en a archivo?',
        ('Sí. Quisiera descargarlos en .csv', 'Sí. Quisiera descargarlos en .xslx', 'No. Estoy bien así')
        )

    submit_button = st.form_submit_button(label='Submit') # Bool


# Hasta que no apretamos submit no continúa el probrama
if submit_button:
    # Llamamos a la función de api_tweets (archivo data_retrieval.py)
    tweets = api_tweets(search_words, lang, date, n_tweets)

    # CREACIÓN DEL DATAFRAME
    ##########################
    # @@@ Añadir una barra de progreso
    # Llamamos a la función de dataframe_creation (archivo data_retrieval.py)
    st.subheader("CREACIÓN DE TU DATAFRAME")
    st.write("Creando tu DataFrame. Por favor espera...")

    df = dataframe_creation(tweets, n_tweets)
    st.dataframe(df)

    # LIMPIEZA DEL DATAFRAME
    ##########################
    st.subheader("LIMPIEZA DE TU DATAFRAME")
    st.write("Limpiando tu DataFrame. Por favor espera...")
    # Hacer como una serie de check list para ver lo que se ha ido haciendo

    # https://stackoverflow.com/questions/69052648/redirecting-downloaded-file-to-users-downloads-folder-python
    import os
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads"
    DOWNLOAD_FOLDER

    # Botón de descarga
    with st.form(key='my_form2'):
        if statuses == "Sí. Quisiera descargarlos en .csv":
            descarga1 = st.form_submit_button(label='Descarga')
            descarga2 = False
            sin_descarga = False
        elif statuses == "Sí. Quisiera descargarlos en .xslx":
            descarga2 = st.form_submit_button(label='Descarga')
            descarga = False
            sin_descarga = False
        else:
            sin_descarga = True
    
        if descarga1 or descarga2 or sin_descarga:
            if descarga1:
                df.to_csv(DOWNLOAD_FOLDER + "Output.csv")
            elif descarga2:
                df.to_excel(DOWNLOAD_FOLDER + "/Output.xslx")
    
            # FORM MODELADO
            #################
            st.write("__________________________________________________________________________________")

            with st.form(key='my_form2'):
                st.subheader("FORMULARIO MODELIZACIÓN Y ENTREGABLES")
                col1, col2 = st.columns((3, 2))
                with col1:
                    stauses2 = st.radio(
                        'Qué tipo de estudio quieres realizar?',
                        ('Análisis de sentimiento', 'Análisis de sentimiento + Topic Modelling'))
                with col2:
                    option2 = st.multiselect(
                        'Qué librerías quieres seleccionar para ello?',
                        ["VADER", "TEXTBLOB", "IBM WATSON"])
                option3 = st.multiselect(
                'Qué visualizaciones quieres de tu análisis?',
                ["DASHBOARD IN SITU MEDIANTE MATPLOTLIB", "DASHBOARD DE TABLEAU", "DASHBOARD DE POWERBI"])
                
                submit_button2 = st.form_submit_button(label='Submit')

            st.write("Has seleccionado realizar un {} empleando para ello las librerías {}.".format(stauses2, option2)) # Que no aparezco como lista

            # MODELADO
            ##########################
            # Hay que meter barras de progreso: https://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations
            st.subheader("MODELADO DE TUS DATOS")
            st.write("Modeladando tus datos. Por favor espera...")
            df = get_final_output(df)
            st.dataframe(df[["text", "possitivity_textblob", "possitivity_vader", "possitivity_ibm"]])
            df = new_categorical_variable(df)
            st.dataframe(df[["text", "sentiment", "possitivity_textblob", "possitivity_vader", "possitivity_ibm"]])


            # GENERACIÓN DE ENTREGABLES
            ##########################
            st.subheader("GENERACIÓN DE TUS DASHBOARDS")
            st.write("Creando tus dashboards. Por favor espera...")