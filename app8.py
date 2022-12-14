import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import requests
import pickle
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from PIL import Image



# Configuraci贸n de p谩gina
st.set_page_config(page_title="Sistema de predicci贸n valor auto usado",page_icon="馃殫",layout="centered")

# Para subir la animaci贸n del sidebar
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Configuraci贸n p谩gina principal
st.title("Valuaci贸n Autos App")

#Llamando al modelo
def load_model():
    with open("regressor3.pkl", "rb") as file:
        data = pickle.load(file)
    return data

#def load_model():
#    data = joblib.load("regressor3.pkl")
#    return data

data = load_model()

model = data["model"]
norm = data["normalization"]

le_manufacturer = LabelEncoder()
le_cylinder = LabelEncoder()
le_transmission = LabelEncoder()
le_drive = LabelEncoder()
le_paint_color = LabelEncoder()


def app():
    
    manufacturers = ('Ford', 'Gmc', 'Chevrolet', 'Toyota', 'Jeep', 'Nissan', 'Honda',
       'Dodge', 'Chrysler', 'Ram', 'Mercedes-Benz', 'BMW', 'Volkswagen',
       'Mazda', 'Porsche', 'Lexus', 'Audi', 'Mitsubishi', 'Infiniti',
       'Kia', 'Hyundai', 'Fiat', 'Acura', 'Cadillac', 'Rover', 'Lincoln',
       'Jaguar', 'Volvo', 'Alfa-Romeo', 'Subaru', 'Pontiac', 'Saturn',
       'Mini', 'Buick', 'Harley-davidson', 'Mercury', 'Datsun',
       'Land Rover', 'Aston-Martin', 'Ferrari')
    cylinders = ('6 cylinders', '8 cylinders', '4 cylinders', '5 cylinders',
       '10 cylinders', '3 cylinders', '12 cylinders')
    transmissions = ('automatic', 'other', 'manual')
    drives = ('rwd', '4wd', 'fwd')
    paint_colors = ('black', 'silver', 'grey', 'red', 'blue', 'white', 'brown',
       'yellow', 'green', 'custom', 'orange', 'purple')
    
    form = st.form("my_form")
    manufacturer = form.selectbox('Marca: ', manufacturers)
    year = form.number_input("A帽o: ")
    odometer = form.number_input("Kilometraje: ") 
    cylinder = form.selectbox('Cilindrada: ', cylinders) 
    transmission = form.selectbox('Transmisi贸n: ', transmissions) 
    drive = form.selectbox('Tracci贸n: ', drives)
    paint_color = form.selectbox('Color: ', paint_colors)
    submit = form.form_submit_button("Iniciar valuaci贸n")
    
    if submit:
        X = np.array([[year, odometer, manufacturer, cylinder, transmission, drive, paint_color]])
        X[:, 2] = le_manufacturer.fit_transform(X[:, 2])
        X[:, 3] = le_cylinder.fit_transform(X[:, 3])
        X[:, 4] = le_transmission.fit_transform(X[:, 4])
        X[:, 5] = le_drive.fit_transform(X[:, 5])
        X[:, 6] = le_paint_color.fit_transform(X[:, 6])
        scaled_X = norm.transform(X)

        price = model.predict(scaled_X)
        actual_price = round(price[0])

        st.subheader(f"La valuaci贸n del auto es: {actual_price:,} dolares")

#Configuraci贸n del sidebar
lottie_book = load_lottieurl('https://assets5.lottiefiles.com/private_files/lf30_skwgamub.json')
with st.sidebar:
    st.title('Valuaci贸n Autos App')
    st.markdown("---")
my_button = st.sidebar.radio("Opciones",('Valuaci贸n autos', 'Parametros del trabajo'))
if my_button == 'Valuaci贸n autos':
    app()
with st.sidebar:
    st.markdown("---")
    st_lottie(lottie_book, speed=0.5, height=200, key="initial")
    st.markdown("---")
    st.caption("Grupo 2: CRodriguez Geier & JSantacecilia")
    #