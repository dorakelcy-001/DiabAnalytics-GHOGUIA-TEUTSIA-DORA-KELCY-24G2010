"""
Module de collecte des données - DiabAnalytics
Formulaire complet pour la saisie des patients
"""

import streamlit as st
from utils import (
    valider_age, valider_taille, valider_poids, 
    valider_glycemie, calculer_imc, ajouter_patient
)

def afficher_formulaire_collecte():
    """Affiche le formulaire de collecte des données"""
    
    st.markdown("##  Nouvelle collecte patient")
    st.markdown("Remplissez tous les champs ci-dessous pour enregistrer un patient.")
    
    with st.form("formulaire_patient", clear_on_submit=True):
        st.markdown("###  Informations générales")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            nom = st.text_input("Nom du patient")
        with col2:
            age = st.number_input("Âge (ans)", min_value=0, max_value=120, value=30)
        with col3:
            sexe = st.selectbox("Sexe", ["Homme", "Femme", "Autre"])
        
        pays = st.selectbox("Pays", [
            "France", "Cameroun", "Sénégal", "Côte d'Ivoire", 
            "Algérie", "Maroc", "Tunisie", "RDC", "Madagascar", "Autre"
        ])
        
        st.markdown("###  Anthropométrie")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            taille = st.number_input("Taille (cm)", min_value=50, max_value=250, value=170)
        with col2:
            poids = st.number_input("Poids (kg)", min_value=10, max_value=300, value=70)
        with col3:
            tour_taille = st.number_input("Tour de taille (cm)", min_value=50, max_value=200, value=85)
        
        # Calcul automatique de l'IMC
        imc_calcule = calculer_imc(poids, taille)
        if imc_calcule:
            st.info(f"IMC calculé : **{imc_calcule}** ({interpreter_imc(imc_calcule)})")
        
        st.markdown("### Biologique")
        
        col1, col2 = st.columns(2)
        with col1:
            glycemie = st.number_input("Glycémie à jeun (mg/dL)", min_value=0, max_value=500, value=100)
        with col2:
            st.write("Tension artérielle")
            col_sys, col_dia = st.columns(2)
            with col_sys:
                tension_sys = st.number_input("Systolique", min_value=50, max_value=250, value=120)
            with col_dia:
                tension_dia = st.number_input("Diastolique", min_value=30, max_value=150, value=80)
        
        st.markdown("### 🏃 Activité physique")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            activite_type = st.selectbox("Type d'activité", [
                "Aucune", "Marche", "Course", "Natation", "Vélo", "Musculation", "Autre"
            ])
        with col2:
            activite_frequence = st.number_input("Fréquence (fois/semaine)", min_value=0, max_value=7, value=2)
        with col3:
            activite_duree = st.number_input("Durée (minutes/séance)", min_value=0, max_value=180, value=30)
        
        sedentaire = st.radio("Êtes-vous sédentaire ? (>6h assis par jour)", ["Non", "Oui"])
        
        st.markdown("### Alimentation")
        
        col1, col2 = st.columns(2)
        with col1:
            alimentation_sucre = st.select_slider(
                "Consommation de sucre rapide",
                options=["Faible", "Moyenne", "Élevée"]
            )
        with col2:
            alimentation_legumes = st.radio("Consommation de légumes", ["Jamais", "Rarement", "Parfois", "Souvent"])
        
        st.markdown("### 🧬 Antécédents")
        
        col1, col2 = st.columns(2)
        with col1:
            antecedents_familiaux = st.radio("Antécédents familiaux de diabète", ["Non", "Oui"])
        with col2:
            antecedents_personnels = st.multiselect(
                "Antécédents personnels",
                ["Diabète gestationnel", "Hypertension", "Cholestérol", "Surpoids/obésité"]
            )
        
        # Bouton de soumission
        submitted = st.form_submit_button(" Enregistrer le patient", use_container_width=True)
        
        if submitted:
            # Validation
            erreurs = []
            
            valid, msg = valider_age(age)
            if not valid: erreurs.append(msg)
            
            valid, msg = valider_glycemie(glycemie)
            if not valid: erreurs.append(msg)
            
            if erreurs:
                for err in erreurs:
                    st.error(f" {err}")
            else:
                # Préparer les données
                donnees = {
                    "nom": nom if nom else f"Patient_{len(charger_donnees())+1}",
                    "age": age,
                    "sexe": sexe,
                    "pays": pays,
                    "taille": taille,
                    "poids": poids,
                    "imc": imc_calcule,
                    "tour_taille": tour_taille,
                    "glycemie": glycemie,
                    "tension_sys": tension_sys,
                    "tension_dia": tension_dia,
                    "activite_type": activite_type,
                    "activite_frequence": activite_frequence,
                    "activite_duree": activite_duree,
                    "sedentaire": sedentaire,
                    "alimentation_sucre": alimentation_sucre,
                    "alimentation_legumes": alimentation_legumes,
                    "antecedents_familiaux": antecedents_familiaux,
                    "antecedents_personnels": ", ".join(antecedents_personnels) if antecedents_personnels else "Aucun"
                }
                
                # Ajouter à la base
                id_patient = ajouter_patient(donnees)
                
                # Récupérer le risque déterminé
                from utils import charger_donnees
                df = charger_donnees()
                risque = df[df["id"] == id_patient]["risque"].values[0]
                
                # Message de succès avec couleur
                if risque == "Élevé":
                    st.error(f" Patient ajouté avec ID {id_patient} - RISQUE ÉLEVÉ détecté !")
                elif risque == "Modéré":
                    st.warning(f" Patient ajouté avec ID {id_patient} - Risque MODÉRÉ")
                else:
                    st.success(f" Patient ajouté avec succès (ID: {id_patient}) - Risque FAIBLE")
                
                st.balloons()

def interpreter_imc(imc):
    """Interprète la valeur de l'IMC"""
    if imc < 18.5:
        return "Maigreur"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Surpoids"
    elif imc < 35:
        return "Obésité modérée"
    else:
        return "Obésité sévère"

def charger_donnees():
    """Charge les données (import local pour éviter les imports circulaires)"""
    from utils import charger_donnees as cd
    return cd()