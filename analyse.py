"""
Module d'analyse descriptive - DiabAnalytics
Version sans plotly (graphiques Streamlit natifs)
"""

import streamlit as st
import pandas as pd
from utils import calculer_statistiques

def afficher_analyse(df):
    """Affiche l'analyse descriptive complète"""
    
    st.markdown("##  Statistiques descriptives des données")
    
    if len(df) == 0:
        st.info("Aucune donnée disponible. Ajoutez des patients dans l'onglet Collecte.")
        return
    
    stats = calculer_statistiques(df)
    
    # KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(" Total patients", stats["total"])
    with col2:
        st.metric(" Diabétiques", stats["diabetiques"])
    with col3:
        st.metric(" Taux", f"{stats['taux_diabete']}%")
    with col4:
        st.metric(" Âge moyen", f"{stats['age_moyen']} ans")
    
    # Graphiques avec Streamlit (pas besoin de plotly)
    st.markdown("###  Distributions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Distribution des âges**")
        st.bar_chart(df["age"].value_counts().sort_index())
    
    with col2:
        st.markdown("**Distribution des glycémies**")
        st.bar_chart(df["glycemie"].value_counts().sort_index())
    
    # Tableau récapitulatif
    st.markdown("###  Récapitulatif")
    st.dataframe(df[["nom", "age", "glycemie", "imc", "risque"]])