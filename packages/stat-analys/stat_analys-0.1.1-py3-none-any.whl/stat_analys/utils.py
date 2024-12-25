# stat_analys/utils.py
import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict, Union
import logging

def verifier_donnees(data: pd.Series) -> Tuple[bool, str]:
    """
    Vérifie la qualité des données avant l'analyse.
    """
    message = ""
    valid = True

    # Vérification des valeurs manquantes
    missing = data.isnull().sum()
    if missing > 0:
        message += f"ATTENTION: {missing} valeurs manquantes détectées. "
        valid = False

    # Vérification du nombre minimal d'observations pour les tests
    if len(data.dropna()) < 3:
        message += "Nombre d'observations insuffisant pour l'analyse statistique. "
        valid = False

    # Pour les données numériques, vérification des valeurs infinies
    if np.issubdtype(data.dtype, np.number):
        inf_count = np.isinf(data).sum()
        if inf_count > 0:
            message += f"ATTENTION: {inf_count} valeurs infinies détectées. "
            valid = False

    if not valid:
        message += "Les tests statistiques ne seront pas effectués sur ces données."

    return valid, message

def calculer_intervalle_confiance(
    data: pd.Series,
    niveau_confiance: float = 0.95
) -> Dict[str, Union[Tuple[float, float], None]]:
    """
    Calcule les intervalles de confiance pour la moyenne et l'écart-type.
    Retourne None si les calculs ne sont pas possibles.
    """
    try:
        n = len(data)
        if n < 2:
            return {
                "ic_moyenne": None,
                "ic_ecart_type": None
            }

        moyenne = np.mean(data)
        ecart_type = np.std(data, ddof=1)

        # Intervalle de confiance pour la moyenne
        t_value = stats.t.ppf((1 + niveau_confiance) / 2, df=n-1)
        marge_erreur = t_value * (ecart_type / np.sqrt(n))
        ic_moyenne = (moyenne - marge_erreur, moyenne + marge_erreur)

        # Intervalle de confiance pour l'écart-type
        chi2_lower = stats.chi2.ppf((1 - niveau_confiance) / 2, df=n-1)
        chi2_upper = stats.chi2.ppf((1 + niveau_confiance) / 2, df=n-1)
        ic_ecart_type = (
            np.sqrt((n-1) * ecart_type**2 / chi2_upper),
            np.sqrt((n-1) * ecart_type**2 / chi2_lower)
        )

        return {
            "ic_moyenne": ic_moyenne,
            "ic_ecart_type": ic_ecart_type
        }
    except Exception as e:
        logging.error(f"Erreur dans le calcul des intervalles de confiance: {str(e)}")
        return {
            "ic_moyenne": None,
            "ic_ecart_type": None
        }

def evaluer_normalite(
    resultats_tests: Dict[str, Dict[str, float]],
    n_echantillon: int = 0
) -> str:
    """
    Évalue si la distribution peut être considérée comme normale.
    """
    if n_echantillon < 3:
        return "Échantillon trop petit pour évaluer la normalité"

    try:
        tests_normaux = 0
        total_tests = 0

        # Shapiro-Wilk (pour n < 5000)
        if n_echantillon < 5000 and "shapiro" in resultats_tests:
            if resultats_tests["shapiro"]["p_value"] > 0.05:
                tests_normaux += 1
            total_tests += 1

        # Anderson-Darling
        if "anderson" in resultats_tests:
            if resultats_tests["anderson"]["statistique"] < resultats_tests["anderson"]["valeurs_critiques"][2]:
                tests_normaux += 1
            total_tests += 1

        # D'Agostino (pour n > 20)
        if n_echantillon > 20 and "dagostino" in resultats_tests:
            if resultats_tests["dagostino"]["p_value"] > 0.05:
                tests_normaux += 1
            total_tests += 1

        if total_tests == 0:
            return "Impossible d'évaluer la normalité"

        # Décision basée sur la majorité des tests
        prop_tests_normaux = tests_normaux / total_tests
        if prop_tests_normaux >= 0.5:
            return f"Normal (concordance: {prop_tests_normaux:.1%})"
        else:
            return f"Non Normal (concordance: {1-prop_tests_normaux:.1%})"

    except Exception as e:
        logging.error(f"Erreur dans l'évaluation de la normalité: {str(e)}")
        return "Erreur dans l'évaluation de la normalité"
