import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np


import os
import requests



frame = pd.read_csv('./output/frame.csv')
users=frame['user_id'][:100].unique()

image = Image.open('icon.png')
st.image(image,use_column_width=True)
st.write("""
# Article Recommandation App
""")
st.write("""
## En entrée, cette App reçoit l'identifiant du lecteur et affiche les articles recommandés 
""")

userid = st.selectbox('Sélectioner un utilisateur', options=users)

#url = 'https://apptestfun.azurewebsites.net/api/httptrigger'
url = 'http://localhost:7071/api/HttpTrigger'
if st.button('Connect'):
    myobj = {'name': userid}
    x = requests.get(url, params = myobj)
    st.write("##  Nous vous recommandons les articles suivants : ")
    st.write(x.text)
   
   
  
   















