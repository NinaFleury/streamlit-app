import streamlit as st
import pandas as pd
import datetime

st.title("Convertisseur CSV vers OFX")

uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=["csv"])

if uploaded_file:
    try:
        # Charger le fichier CSV avec utf-8
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        st.warning("Erreur d'encodage détectée. Tentative avec l'encodage 'latin1'...")
        try:
            df = pd.read_csv(uploaded_file, encoding='latin1')
        except pd.errors.EmptyDataError:
            st.error("Le fichier est vide ou ne contient aucune colonne valide.")
            df = None
    except pd.errors.EmptyDataError:
        st.error("Le fichier est vide ou ne contient aucune colonne valide.")
        df = None

    # Vérifier que le fichier a été chargé avec succès
    if df is not None:
        if df.empty:
            st.error("Le fichier est vide.")
        else:
            st.success("Fichier chargé avec succès.")
            # Ajoutez ici votre logique de conversion vers OFX
