import pandas as pd
import streamlit as st

st.title("Convertisseur CSV vers OFX")

uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=["csv"])

if uploaded_file:
    try:
        # Charger le fichier avec utf-8, sinon essayer avec latin1
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        st.warning("Erreur d'encodage détectée. Tentative avec l'encodage 'latin1'...")
        df = pd.read_csv(uploaded_file, encoding='latin1')
    except pd.errors.EmptyDataError:
        st.error("Le fichier est vide ou ne contient aucune donnée.")
    else:
        # Vérifier si le fichier a des colonnes valides
        if df.empty or df.columns.size == 0:
            st.error("Le fichier ne contient aucune colonne.")
        else:
            st.success("Fichier chargé avec succès.")
            # Continuer avec la conversion vers OFX...
