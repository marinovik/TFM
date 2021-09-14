import re
import pycountry
import pandas as pd


def find_country(text, exceptions):
        x = 'NA'
        text = str(text).title()
        #buscar excepciones
        for i in exceptions:
            s = re.search(i[0], text)
            if s != None:
                x = i[1]
                break


def find_country(text, exceptions, us_states):
        x = 'NA'
        text = str(text).title()
        #buscar excepciones
        for i in exceptions:
            s = re.search(i[0], text)
            if s != None:
                x = i[1]
                break
        # buscar US States
        for i in us_states:
            s = re.search(i, text)
            if s != None:
                x = 'United States'
                break
        # buscar paises
        for country in pycountry.countries:
            if country.name in text:
                x = country.name
        return x


def get_country_name(code):
        try:
            return pycountry.countries.indices['alpha_2'][str(code)].name
        except:
            return '-'


def eliminar_tildes(texto):
        texto_limpio = re.sub('(á)|(Á)|(à)|(À)','a', texto)
        texto_limpio = re.sub('(é)|(É)|(è)|(È)','e', texto_limpio)
        texto_limpio = re.sub('(í)|(Í)|(ì)|(Ì)','i', texto_limpio)
        texto_limpio = re.sub('(ó)|(Ó)|(ò)|(Ò)','o', texto_limpio)
        texto_limpio = re.sub('(ú)|(Ú)|(ù)|(Ù)','u', texto_limpio)
        return texto_limpio


def find_city(text, list_cities):
    text = str(text).lower() # Paso a minusculas
    text = eliminar_tildes(text) # Eliminar tildes
    text = re.sub(r'[^\w\s]','',text) # Eliminar puntuacion
    text = text.split() # Lista con cada palabra para que no capture partes de palabras como ciudades

    try:
        for city in list_cities.City:
            if city in text:
                return city
                break
    except:
        return '-'


def city_to_country(city, list_cities):
    try:
        return list_cities[list_cities['City']==str(city)]['Country_name'].head(1).item()
    except:
        return '-'


def select_country(search_country_1, search_city_1_country):

        if search_country_1 == 'NA':
            return search_city_1_country
        else:
            return search_country_1


def location_treatment(df):
    df_locations = df[['user_location']]
    df.rename({'user_location': 'original_location'}, axis=1, inplace=True)

    exceptions = [('New\sYork', 'United States'), ('Los\sAngeles', 'United States'), 
                    ('San\sFrancisco', 'United States'), ('Buenos\sAires', 'Argentina'), 
                    ('Cape\sTown', 'South Africa'), ('San\sDiego', 'United States'), 
                    ('Rio\sDe\sJaneiro', 'Brazil'), ('Nyc', 'United States'),('Newyork', 'United States'), ('Ny', 'United States'), 
                    ('Washington\sDc', 'United States'), ('Scotland', 'United Kingdom'),
                    ('Wales', 'United Kingdom'),('England', 'United Kingdom'), ('Dc', 'United States'), 
                    ('Usa', 'United States'), ('Us', 'United States'), ('Uk', 'United Kingdom'), ('Queensland', 'Australia')]

    us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
    "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
    "Nebraska","Nevada","New\sHampshire","New\sJersey","New\sMexico","New\sYork","North\sCarolina","North\sDakota","Ohio","Oklahoma","Oregon","Pennsylvania",
    "Rhode\sIsland","South\sCarolina","South\sDakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West\sVirginia","Wisconsin","Wyoming", 
    'Al', 'Ak', 'Az', 'Ar', 'Ca', 'Co', 'Ct', 'Dc', 'De', 'Fl', 'Ga', 'Hi', 'Id', 'Il', 'In', 'Ia', 'Ks', 'Ky', 'La', 'Me', 'Md', 'Ma', 'Mi', 'Mn', 'Ms', 
    'Mo', 'Mt', 'Ne', 'Nv', 'Nh', 'Nj', 'Nm', 'Ny', 'Nc', 'Nd', 'Oh', 'Ok', 'Or', 'Pa', 'Ri', 'Sc', 'Sd', 'Tn', 'Tx', 'Ut', 'Vt', 'Va', 'Wa', 'Wv', 'Wi', 'Wy']
    
    df_locations['search_country_1'] = df['original_location'].apply(lambda x: find_country(x, exceptions, us_states))

    list_cities = pd.read_csv('worldcitiespop.csv')

    list_cities.drop(['Region'], inplace=True, axis=1)
    list_cities.sort_values(by='Population', ascending=False, inplace=True) 

    country_table = pd.DataFrame(list_cities.Country.unique(), columns=['code'])
    country_table['Country_name'] = country_table['code'].apply(lambda x: get_country_name(x))

    list_cities = pd.merge(list_cities, country_table, left_on='Country', right_on='code', how='left')
    list_cities.drop('code', axis=1, inplace=True)
    list_cities = list_cities[['Country', 'Country_name', 'City', 'AccentCity', 'Population', 'Latitude', 'Longitude']]

    df_locations['search_city_1'] = df['original_location'].progress_apply(lambda x: find_city(x, list_cities))
    df_locations['search_city_1_country'] = df_locations['search_city_1'].progress_apply(lambda x: city_to_country(x, list_cities))
        
    df_locations['country'] = df_locations[['search_country_1', 'search_city_1_country']].progress_apply(lambda x: select_country(*x), axis=1)

    df['user_location'] = df_locations['country']

    return df