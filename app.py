"""
DiabAnalytics - Application principale
Moteur de collecte et d'analyse descriptive du diabète
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="DiabAnalytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import des modules
from utils import initialiser_csv, charger_donnees
from collecte import afficher_formulaire_collecte
from analyse import afficher_analyse
from affichage import afficher_accueil, afficher_conseils, afficher_donnees_brutes

# ============================================
# INITIALISATION
# ============================================

# Initialiser le fichier CSV
initialiser_csv()

# Charger les données
df = charger_donnees()

# Initialiser l'état de session si nécessaire
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# ============================================
# SIDEBAR (Navigation)
# ============================================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/diabetes.png", width=80)
    st.title("DiabAnalytics")
    st.caption("Collecte & analyse descriptive")
    st.markdown("---")
    
    # Boutons de navigation
    if st.button(" Accueil", use_container_width=True):
        st.session_state.page = "Accueil"
        st.rerun()
    
    if st.button(" Collecte patient", use_container_width=True):
        st.session_state.page = "Collecte"
        st.rerun()
    
    if st.button(" Analyse descriptive", use_container_width=True):
        st.session_state.page = "Analyse"
        st.rerun()
    
    if st.button(" Données brutes", use_container_width=True):
        st.session_state.page = "Données"
        st.rerun()
    
    if st.button(" Conseils & FAQ", use_container_width=True):
        st.session_state.page = "Conseils"
        st.rerun()
    
    st.markdown("---")
    st.caption("Version 1.0")
    st.caption("Moteur de collecte et d'analyse descriptive")

# ============================================
# AFFICHAGE DES PAGES
# ============================================

if st.session_state.page == "Accueil":
    afficher_accueil()

elif st.session_state.page == "Collecte":
    afficher_formulaire_collecte()
    
    # Afficher un résumé après la collecte
    df_actualise = charger_donnees()
    if len(df_actualise) > 0:
        st.markdown("---")
        st.markdown("###  Résumé rapide")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total patients", len(df_actualise))
        with col2:
            nb_eleve = len(df_actualise[df_actualise["risque"] == "Élevé"])
            st.metric("Risque élevé", nb_eleve)
        with col3:
            taux = round(nb_eleve / len(df_actualise) * 100, 1) if len(df_actualise) > 0 else 0
            st.metric("Taux", f"{taux}%")

elif st.session_state.page == "Analyse":
    afficher_analyse(df)

elif st.session_state.page == "Données":
    afficher_donnees_brutes(df)

elif st.session_state.page == "Conseils":
    afficher_conseils(df)

# ============================================
# PIED DE PAGE
# ============================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    DiabAnalytics - Outil de collecte et d'analyse descriptive du diabète<br>
     Ce logiciel n'est pas un dispositif médical. Consultez un médecin pour tout diagnostic.
    </div>
    """,
    unsafe_allow_html=True
)