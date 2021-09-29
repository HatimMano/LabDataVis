import streamlit as st
import numpy as np
import pandas as pd 
import time
import seaborn as sns
from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print ('Temps écoulé : {}'.format((end-start)*1000) + " ms")
        return result
    return wrapper

@timing
def histo(titre, df, b, rw, r, fig, column):
    st.title(titre)
    df[[column]].plot.hist(bins=b, rwidth= rw,range=r, figsize=fig,title= titre)
    st.pyplot()


@timing
#@st.cache(suppress_st_warning=True)
def lancement():

    x = st.sidebar.selectbox(
        'Voici les 2 databases',
        ('uber-raw-data', 'ny-trips-data')
    )

    if x == 'uber-raw-data':
        st.title('Données Uber')
        st.write('Trajets Uber quotidiens')
        df = pd.read_csv('uber-raw-data-apr14.csv', delimiter=',')

        agree = st.checkbox("Inspecter quelques valeurs des données")
        if agree:
            st.write(df.head())

        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        df['Date/Time'].apply(get_dom)
        df['day'] = df['Date/Time'].map(get_dom)
        df['hour'] = df['Date/Time'].map(get_hour)
        df['weekday']=df['Date/Time'].map(get_weekday)
        
        histo("Fréquence de course par heure sur une semaine", df,  30, 0.8, (0.5,23.5),(30,15), "hour")
        histo("Fréquence par heure", df, 24, 0.8, (-0.5,23.5), None, "weekday")  

    if x == 'ny-trips-data':
        st.title('New York Trips')
        st.write('Trajets Uber quotidiens à New York City')
        dff = pd.read_csv("ny-trips-data.csv")
        dff['tpep_pickup_datetime']=pd.to_datetime(dff["tpep_pickup_datetime"])
        dff['tpep_dropoff_datetime']=pd.to_datetime(dff["tpep_dropoff_datetime"])   
        dff['hour'] = dff['tpep_pickup_datetime'].map(get_hour)

        agree = st.checkbox("Inspecter quelques valeurs des données")
        if agree:
            st.write(dff.head())
        
        histo("Fréquence de course par heure en Avril 2014", dff, 24, 0.8, (-0.5,23.5), None, "hour")

        histo('Trajets par heure', dff, 24, 0.9, (-0.5,23.5), None,"hour")   
        

    st.write('Manowaraly_Hatim_LAB3')

def get_dom(dt):
        return dt.day
    
def get_weekday(dt):
    return dt.weekday()

def get_hour(dt):
    return dt.hour

def count_rows(rows):
    return len(rows)


lancement()
