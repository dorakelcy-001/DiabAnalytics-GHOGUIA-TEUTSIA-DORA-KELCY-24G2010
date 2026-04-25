"""
Module d'affichage et conseils - DiabAnalytics
Page d'accueil, FAQ, conseils contextuels, données brutes
"""

import streamlit as st
import pandas as pd
from utils import calculer_statistiques

# ============================================
# PAGE D'ACCUEIL
# ============================================

def afficher_accueil():
    """Affiche la page d'accueil"""
    
    st.markdown("#  DiabAnalytics")
    st.markdown("## Moteur de collecte et d'analyse descriptive du diabète")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ###  Objectif
        
        DiabAnalytics vous permet de :
        - **Collecter** facilement les données patients
        - **Analyser** automatiquement les facteurs de risque
        - **Détecter** les profils à risque
        - **Conseiller** une prévention adaptée
        
        ###  Facteurs de risque du diabète
        
        - Âge > 45 ans
        - Surpoids (IMC > 25)
        - Sédentarité
        - Antécédents familiaux
        - Hypertension
        - Alimentation déséquilibrée
        """)
    
    with col2:
        st.markdown("""
        ### Ce que vous pouvez faire
        
        | Onglet | Fonction |
        |--------|----------|
        |  Collecte | Saisir un nouveau patient |
        |  Analyse | Visualiser les statistiques |
        |  Données | Consulter les données brutes |
        |  Conseils | FAQ et recommandations |
        
        ###  Rappel médical
        
        > Une glycémie à jeun ≥ 126 mg/dL (7.0 mmol/L) 
        > confirme le diagnostic de diabète.
        """)
        
        if st.button("Commencer une collecte", use_container_width=True):
            st.session_state.page = "Collecte"
            st.rerun()

# ============================================
# CONSEILS ET FAQ
# ============================================

def afficher_conseils(df):
    """Affiche la FAQ et les conseils contextuels"""
    
    st.markdown("##  Conseils & FAQ")
    
    # Conseils contextuels automatiques
    st.markdown("###  Conseils personnalisés")
    
    stats = calculer_statistiques(df)
    
    if len(df) > 0:
        if stats["taux_diabete"] > 30:
            st.error("🔴 **Alerte population** : Le taux de diabète dépasse 30% !")
        elif stats["taux_diabete"] > 15:
            st.warning("🟠 **Attention** : Le taux de diabète est supérieur à 15%.")
        else:
            st.success("🟢 **Bon point** : Le taux de diabète est maîtrisé.")
    else:
        st.info("📭 Ajoutez des patients pour recevoir des conseils.")
    
    st.markdown("---")
    
    # FAQ
    st.markdown("### Questions fréquentes")
    
    faq = {
        "Qu'est-ce que le diabète ?": "Le diabète est une maladie chronique caractérisée par un excès de sucre dans le sang.",
        "Quelle est la glycémie normale ?": "À jeun : 70-100 mg/dL. Entre 100-125 : pré-diabète. Au-delà de 126 : diabète.",
        "Comment prévenir le diabète ?": "Perdre 5-7% du poids, activité physique 30 min/jour, réduire les sucres.",
        "Quels aliments éviter ?": "Sodas, pâtisseries, pain blanc, riz blanc, plats préparés.",
        "Quels aliments privilégier ?": "Légumes verts, légumineuses, poissons gras, céréales complètes."
    }
    
    for question, reponse in faq.items():
        with st.expander(f"❓ {question}"):
            st.write(reponse)

# ============================================
# DONNÉES BRUTES
# ============================================

def afficher_donnees_brutes(df):
    """Affiche les données brutes avec pagination et export"""
    
    st.markdown("##  Données brutes")
    
    if len(df) == 0:
        st.info(" Aucune donnée disponible.")
        return
    
    # Recherche
    recherche = st.text_input(" Rechercher par nom", placeholder="Nom du patient...")
    
    # Filtrage
    df_affiche = df.copy()
    if recherche:
        df_affiche = df_affiche[df_affiche["nom"].str.contains(recherche, case=False, na=False)]
    
    # Affichage
    st.dataframe(df_affiche, use_container_width=True)
    st.caption(f"Total : {len(df_affiche)} patients")
    
    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=" Exporter toutes les données (CSV)",
        data=csv,
        file_name="diabanalytics_export.csv",
        mime="text/csv"
    )