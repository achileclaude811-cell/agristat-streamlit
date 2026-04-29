import streamlit as st
import sqlite3
import pandas as pd

st.title("🐄 AgriStat Pro")

# Formulaire de collecte
st.header("Nouvelle collecte")
nom = st.text_input("Nom de l'éleveur")
espece = st.selectbox("Espèce", ["Poulet","Canard","Porc","Bovin"])
effectif = st.number_input("Effectif total", min_value=0)

if st.button("Enregistrer"):
    st.success("Fiche enregistrée !")
