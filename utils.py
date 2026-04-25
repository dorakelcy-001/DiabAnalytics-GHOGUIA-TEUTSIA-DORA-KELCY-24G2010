"""
Fonctions utilitaires pour DiabAnalytics
Validation, calculs, détermination automatique du risque
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ============================================
# VALIDATION DES DONNÉES
# ============================================

def valider_age(age):
    """Vérifie que l'âge est valide (0-120)"""
    if age is None:
        return False, "L'âge est requis"
    if not isinstance(age, (int, float)):
        return False, "L'âge doit être un nombre"
    if age < 0 or age > 120:
        return False, "L'âge doit être compris entre 0 et 120 ans"
    return True, "OK"

def valider_taille(taille):
    """Vérifie que la taille est valide (50-250 cm)"""
    if taille is None:
        return True, "OK"  # Optionnel
    if taille < 50 or taille > 250:
        return False, "La taille doit être comprise entre 50 et 250 cm"
    return True, "OK"

def valider_poids(poids):
    """Vérifie que le poids est valide (10-300 kg)"""
    if poids is None:
        return True, "OK"  # Optionnel
    if poids < 10 or poids > 300:
        return False, "Le poids doit être compris entre 10 et 300 kg"
    return True, "OK"

def valider_glycemie(glycemie):
    """Vérifie que la glycémie est valide (0-500 mg/dL)"""
    if glycemie is None:
        return False, "La glycémie est requise"
    if glycemie < 0 or glycemie > 500:
        return False, "La glycémie doit être comprise entre 0 et 500 mg/dL"
    return True, "OK"

def valider_imc(imc):
    """Vérifie que l'IMC est valide (10-50)"""
    if imc is None:
        return True, "OK"
    if imc < 10 or imc > 50:
        return False, "L'IMC doit être compris entre 10 et 50"
    return True, "OK"

# ============================================
# CALCUL DE L'IMC
# ============================================

def calculer_imc(poids, taille):
    """Calcule l'IMC à partir du poids (kg) et taille (cm)"""
    if poids is None or taille is None:
        return None
    if taille <= 0 or poids <= 0:
        return None
    taille_m = taille / 100
    imc = poids / (taille_m ** 2)
    return round(imc, 1)

# ============================================
# DÉTERMINATION AUTOMATIQUE DU RISQUE DIABÈTE
# ============================================

def determiner_risque(glycemie, imc, sedentaire, activite_frequence, antecedents_familiaux):
    """
    Détermine automatiquement le risque de diabète
    Retourne : "Faible", "Modéré" ou "Élevé"
    """
    risque_score = 0
    
    # Règle 1 : Glycémie
    if glycemie is not None:
        if glycemie >= 126:
            risque_score += 50
        elif glycemie >= 100:
            risque_score += 25
    
    # Règle 2 : IMC
    if imc is not None:
        if imc > 30:
            risque_score += 30
        elif imc > 25:
            risque_score += 15
    
    # Règle 3 : Sédentarité
    if sedentaire == "Oui":
        risque_score += 20
    
    # Règle 4 : Activité physique
    if activite_frequence is not None:
        if activite_frequence == 0:
            risque_score += 15
        elif activite_frequence <= 1:
            risque_score += 10
        elif activite_frequence <= 2:
            risque_score += 5
    
    # Règle 5 : Antécédents familiaux
    if antecedents_familiaux == "Oui":
        risque_score += 20
    
    # Classification finale
    if risque_score >= 70:
        return "Élevé"
    elif risque_score >= 40:
        return "Modéré"
    else:
        return "Faible"

# ============================================
# GESTION DU FICHIER CSV
# ============================================

def initialiser_csv():
    """Crée le fichier CSV avec les bonnes colonnes s'il n'existe pas"""
    chemin = "data/patients.csv"
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(chemin):
        df = pd.DataFrame(columns=[
            "id", "date_saisie", "nom", "age", "sexe", "pays",
            "taille", "poids", "imc", "tour_taille",
            "glycemie", "tension_sys", "tension_dia",
            "activite_type", "activite_frequence", "activite_duree",
            "sedentaire", "alimentation_sucre", "alimentation_legumes",
            "antecedents_familiaux", "antecedents_personnels",
            "risque"
        ])
        df.to_csv(chemin, index=False)
    return chemin

def ajouter_patient(donnees):
    """Ajoute un nouveau patient dans le CSV"""
    chemin = "data/patients.csv"
    df = pd.read_csv(chemin)
    
    # Ajouter l'ID et la date
    nouveau_id = len(df) + 1
    donnees["id"] = nouveau_id
    donnees["date_saisie"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ajouter le risque automatique
    donnees["risque"] = determiner_risque(
        donnees.get("glycemie"),
        donnees.get("imc"),
        donnees.get("sedentaire"),
        donnees.get("activite_frequence", 0),
        donnees.get("antecedents_familiaux")
    )
    
    # Créer une nouvelle ligne
    nouvelle_ligne = pd.DataFrame([donnees])
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)
    df.to_csv(chemin, index=False)
    return nouveau_id

def charger_donnees():
    """Charge les données depuis le CSV"""
    chemin = "data/patients.csv"
    if os.path.exists(chemin):
        return pd.read_csv(chemin)
    else:
        initialiser_csv()
        return pd.read_csv(chemin)

# ============================================
# STATISTIQUES DESCRIPTIVES
# ============================================

def calculer_statistiques(df):
    """Calcule les statistiques descriptives de base"""
    stats = {}
    
    if len(df) > 0:
        stats["total"] = len(df)
        stats["diabetiques"] = len(df[df["risque"] == "Élevé"])
        stats["taux_diabete"] = round(stats["diabetiques"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0
        
        # Moyennes
        stats["age_moyen"] = round(df["age"].mean(), 1) if "age" in df else 0
        stats["glycemie_moyenne"] = round(df["glycemie"].mean(), 1) if "glycemie" in df else 0
        stats["imc_moyen"] = round(df["imc"].mean(), 1) if "imc" in df else 0
        
        # Médianes
        stats["age_median"] = round(df["age"].median(), 1) if "age" in df else 0
        stats["glycemie_median"] = round(df["glycemie"].median(), 1) if "glycemie" in df else 0
        
        # Écart-types
        stats["age_std"] = round(df["age"].std(), 1) if "age" in df else 0
        stats["glycemie_std"] = round(df["glycemie"].std(), 1) if "glycemie" in df else 0
    else:
        stats["total"] = 0
        stats["diabetiques"] = 0
        stats["taux_diabete"] = 0
        stats["age_moyen"] = 0
        stats["glycemie_moyenne"] = 0
        stats["imc_moyen"] = 0
    
    return stats