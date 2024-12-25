# stat_analys/advanced_univariate_stat.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import (
    shapiro, anderson, normaltest, skew, kurtosis,
    levene, bartlett, fligner, norm, t, kstest
)
from typing import Union, Dict, List, Optional, Tuple
from sklearn.linear_model import HuberRegressor
from tabulate import tabulate
from dataclasses import dataclass
import logging
import warnings
from collections import defaultdict
from .configuration import ConfigurationPlot
from .utils import verifier_donnees, calculer_intervalle_confiance, evaluer_normalite
from .visualizations import (
    creer_visualisation_seaborn_numerique,
    creer_visualisation_seaborn_categorielle,
    creer_visualisation_plotly_numerique,
    creer_visualisation_plotly_categorielle
)

warnings.filterwarnings("ignore")

class AdvancedUnivariateStat:
    """
    Classe principale pour l'analyse statistique univariée avancée.

    Attributes:
        config (ConfigurationPlot): Configuration des paramètres de visualisation.

    Methods:
        analyse_statistique_avancee(df, colonnes=None, afficher_plots=True, **kwargs):
            Analyse statistique avancée des variables avec visualisations multiples.
    """
    def __init__(self, config: Optional[ConfigurationPlot] = None):
        self.config = config or ConfigurationPlot()
        self._setup_visuals()
        self._setup_logging()

    def _setup_visuals(self):
        sns.set_style(self.config.theme_seaborn)
        sns.set_palette(self.config.palette)
        plt.rcParams['font.size'] = self.config.taille_police

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _calculer_statistiques(self, data: pd.Series) -> Dict:
        """
        Calcul des statistiques descriptives et tests avancés.
        """
        resultats = {}
        resultats["data"] = data  # Ajout des données originales pour les statistiques de base

        if np.issubdtype(data.dtype, np.number):
            # Statistiques descriptives
            desc = data.describe()
            resultats["stats_descriptives"] = desc.to_dict()

            # Intervalles de confiance
            ic = calculer_intervalle_confiance(
                data.dropna(),
                self.config.niveau_confiance
            )
            resultats["intervalles_confiance"] = ic

            # Tests de normalité
            clean_data = data.dropna()

            # Shapiro-Wilk
            stat_sw, p_sw = shapiro(clean_data)
            # Anderson-Darling
            stat_ad = anderson(clean_data)
            # D'Agostino-Pearson
            stat_dp, p_dp = normaltest(clean_data)
            # Kolmogorov-Smirnov
            stat_ks, p_ks = kstest(clean_data, 'norm')
            # Lilliefors

            tests_normalite = {
                "shapiro": {"statistique": stat_sw, "p_value": p_sw, "avantages": "Puissant et précis", "inconvénients": "Moins adapté aux grands échantillons", "conditions": "Échantillons de petite et moyenne taille"},
                "anderson": {"statistique": stat_ad.statistic, "valeurs_critiques": stat_ad.critical_values, "p_value": None, "avantages": "Sensible aux écarts dans les queues de la distribution", "inconvénients": "Peut être moins puissant pour les échantillons de petite taille", "conditions": "Échantillons de toutes tailles"},
                "dagostino": {"statistique": stat_dp, "p_value": p_dp, "avantages": "Détecte les asymétries et variations d'aplatissement", "inconvénients": "Moins puissant que le test de Shapiro-Wilk", "conditions": "Échantillons de toutes tailles"},
                "kolmogorov": {"statistique": stat_ks, "p_value": p_ks, "avantages": "Peut être utilisé pour des échantillons plus importants", "inconvénients": "Moins puissant que le test de Shapiro-Wilk", "conditions": "Échantillons de toutes tailles"},
            }

            resultats["tests_normalite"] = tests_normalite
            resultats["conclusion_normalite"] = evaluer_normalite(tests_normalite, len(clean_data))

            # Skewness et Kurtosis avec intervalles de confiance
            n = len(clean_data)
            se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
            se_kurtosis = np.sqrt(24 * n * (n - 1) ** 2 / ((n - 3) * (n - 2) * (n + 3) * (n + 5)))

            sk = skew(clean_data)
            kt = kurtosis(clean_data)

            z_value = stats.norm.ppf((1 + self.config.niveau_confiance) / 2)

            resultats["forme"] = {
                "skewness": {
                    "valeur": sk,
                    "ic": (sk - z_value * se_skewness, sk + z_value * se_skewness)
                },
                "kurtosis": {
                    "valeur": kt,
                    "ic": (kt - z_value * se_kurtosis, kt + z_value * se_kurtosis)
                }
            }

            # Interprétation de la distribution
            asymetrie = "Quasi symétrique" if abs(sk) < 0.5 else "Asymétrie négative (queue à gauche)" if sk < 0 else "Asymétrie positive (queue à droite)"
            aplatissement = "Mésocurtique (normale)" if abs(kt) < 3 else "Leptocurtique (pointue)" if kt > 3 else "Platycurtique (aplatie)"
            resultats["interpretation_distribution"] = {
                "Asymétrie": asymetrie,
                "Aplatissement": aplatissement
            }

        else:
            # Pour les variables catégorielles
            freq = data.value_counts()
            prop = data.value_counts(normalize=True)
            n = len(data)

            # Intervalles de confiance pour les proportions (méthode Wilson)
            ic_proportions = {}
            for categorie in freq.index:
                p_hat = prop[categorie]
                z = stats.norm.ppf((1 + self.config.niveau_confiance) / 2)

                # Formule de Wilson
                denominator = 1 + z**2/n
                p_adj = (p_hat + z**2/(2*n))/denominator
                ci_width = z*np.sqrt(p_hat*(1-p_hat)/n + z**2/(4*n**2))/denominator

                ic_proportions[categorie] = (max(0, p_adj - ci_width), min(1, p_adj + ci_width))

            resultats["distribution"] = {
                "frequences": freq.to_dict(),
                "proportions": prop.to_dict(),
                "ic_proportions": ic_proportions,
                "mode": data.mode()[0],
                "nombre_categories": len(freq),
                "entropie": stats.entropy(prop)  # Mesure de la diversité
            }

        return resultats

    def _formater_resultats(self, resultats: Dict, nom: str) -> str:
        """
        Formatage amélioré des résultats en tableaux.
        """
        tables = []

        # Statistiques descriptives numériques
        if "stats_descriptives" in resultats:
            df_desc = pd.DataFrame(resultats["stats_descriptives"], index=["Valeur"]).T

            # Ajout des intervalles de confiance
            ic_moyenne = resultats["intervalles_confiance"]["ic_moyenne"]
            ic_ecart_type = resultats["intervalles_confiance"]["ic_ecart_type"]

            df_desc.loc["IC_moyenne_inf"] = ic_moyenne[0]
            df_desc.loc["IC_moyenne_sup"] = ic_moyenne[1]
            df_desc.loc["IC_ecart_type_inf"] = ic_ecart_type[0]
            df_desc.loc["IC_ecart_type_sup"] = ic_ecart_type[1]

            tables.append(f"\nStatistiques descriptives pour {nom}:")
            tables.append(tabulate(df_desc.T, headers="keys", tablefmt="fancy_grid", floatfmt=".4f"))

            # Ajout des statistiques de forme avec IC
            if "forme" in resultats:
                forme_data = {
                    "Mesure": ["Skewness", "Kurtosis"],
                    "Valeur": [
                        resultats["forme"]["skewness"]["valeur"],
                        resultats["forme"]["kurtosis"]["valeur"]
                    ],
                    f"IC {self.config.niveau_confiance*100}% Inf": [
                        resultats["forme"]["skewness"]["ic"][0],
                        resultats["forme"]["kurtosis"]["ic"][0]
                    ],
                    f"IC {self.config.niveau_confiance*100}% Sup": [
                        resultats["forme"]["skewness"]["ic"][1],
                        resultats["forme"]["kurtosis"]["ic"][1]
                    ]
                }
                df_forme = pd.DataFrame(forme_data)
                tables.append("\nStatistiques de forme:")
                tables.append(tabulate(df_forme, headers="keys", tablefmt="fancy_grid", floatfmt=".4f"))

        # Tests de normalité
        if "tests_normalite" in resultats:
            test_data = []
            for test, details in resultats["tests_normalite"].items():
                test_data.append({
                    "Test": test.capitalize(),
                    "Statistique": details["statistique"],
                    "P-value": details["p_value"] if details["p_value"] is not None else "Voir valeurs critiques",
                    "Conclusion": "Normal" if (details["p_value"] is not None and details["p_value"] > 0.05) or (details["p_value"] is None and details["statistique"] < details["valeurs_critiques"][2]) else "Non Normal",
                    "Avantages": details["avantages"],
                    "Inconvénients": details["inconvénients"],
                    "Conditions d'utilisation": details["conditions"]
                })

            df_norm = pd.DataFrame(test_data)
            tables.append(f"\nTests de normalité pour {nom}:")
            tables.append(tabulate(df_norm, headers="keys", tablefmt="fancy_grid"))

            # Valeurs critiques Anderson-Darling
            if "anderson" in resultats["tests_normalite"]:
                tables.append(f"\nValeurs critiques Anderson pour {nom}:")
                ad_critical_values = resultats["tests_normalite"]["anderson"]["valeurs_critiques"]
                ad_critical_values_df = pd.DataFrame(ad_critical_values.reshape(1, -1), columns=["15%", "10%", "5%", "2.5%", "1%"])
                tables.append(tabulate(
                    ad_critical_values_df,
                    headers="keys",
                    tablefmt="fancy_grid"
                ))

        # Interprétation de la distribution
        if "interpretation_distribution" in resultats:
            tables.append("\n🔬 Interprétation de la distribution :")
            tables.append(tabulate([
                ["Asymétrie", resultats["interpretation_distribution"]["Asymétrie"]],
                ["Aplatissement", resultats["interpretation_distribution"]["Aplatissement"]]
            ], headers=["Aspect", "Description"], tablefmt="fancy_grid"))

        # Distribution catégorielle
        if "distribution" in resultats:
            cat_data = []
            for cat in resultats["distribution"]["frequences"].keys():
                cat_data.append({
                    "Catégorie": cat,
                    "Fréquence": resultats["distribution"]["frequences"][cat],
                    "Proportion": f"{resultats['distribution']['proportions'][cat]*100:.2f}%",
                    f"IC {self.config.niveau_confiance*100}% Inf": f"{resultats['distribution']['ic_proportions'][cat][0]*100:.2f}%",
                    f"IC {self.config.niveau_confiance*100}% Sup": f"{resultats['distribution']['ic_proportions'][cat][1]*100:.2f}%"
                })

            df_cat = pd.DataFrame(cat_data)
            tables.append(f"\nDistribution des catégories pour {nom}:")
            tables.append(tabulate(df_cat, headers="keys", tablefmt="fancy_grid"))

            # Mesures de diversité
            tables.append(f"\nMesures de diversité:")
            tables.append(f"Entropie de Shannon: {resultats['distribution']['entropie']:.4f}")

        return "\n".join(tables)

    def Analyser(
        self,
        data: pd.DataFrame,
        colonnes: Optional[List[str]] = None,
        afficher_plots: bool = True,
        **kwargs
    ):
        """
        Analyse statistique des variables avec visualisations multiples.
       
        Args:
            data (pd.DataFrame): DataFrame à analyser
            colonnes (List[str], optional): Liste des colonnes à analyser
            afficher_plots (bool): Afficher les visualisations
            **kwargs: Arguments supplémentaires pour personnaliser l'analyse:
                - kde (bool): Afficher la densité kernel
                - rug (bool): Afficher le rugged plot
                - style_boxplot (str): Style des boxplots ('box' ou 'violin')
                - theme (str): Thème Plotly
                - engine (str): Moteur de visualisation ('seaborn', 'plotly', 'both')
                - niveau_confiance (float): Niveau de confiance pour les IC

        Returns:
            - : Résultats de l'analyse
        
        
         Configuration des paramètres de visualisation.

        Attributes:
            theme_plotly (str): Thème Plotly pour les visualisations.
            theme_seaborn (str): Thème Seaborn pour les visualisations.
            hauteur (int): Hauteur des figures.
            largeur (int): Largeur des figures.
            taille_police (int): Taille de la police.
            palette (str): Palette de couleurs pour les visualisations.
            rotation_labels (int): Rotation des labels.
            afficher_kde (bool): Afficher la densité kernel.
            afficher_rug (bool): Afficher le rugged plot.
            nbins (int): Nombre de bins pour les histogrammes.
            style_boxplot (str): Style des boxplots ('box' ou 'violin').
            alpha (float): Transparence des plots.
            engine (str): Moteur de visualisation ('seaborn', 'plotly', ou 'both').
            niveau_confiance (float): Niveau de confiance pour les intervalles de confiance.
            palette_categorielle (str): Palette de couleurs pour les variables catégorielles.
            
        """
        # Mise à jour de la configuration avec les kwargs
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # Si aucune colonne n'est spécifiée, analyser toutes les colonnes
        if colonnes is None:
            colonnes = data.columns.tolist()

        resultats = {}

        for colonne in colonnes:
            if colonne not in data.columns:
                self.logger.warning(f"La colonne {colonne} n'existe pas dans le DataFrame")
                continue

            data = data[colonne]
            valid, message = verifier_donnees(data)
            if not valid:
                self.logger.warning(message)
                resultats[colonne] = {"message": message}
                continue

            resultats[colonne] = self._calculer_statistiques(data)

            print(self._formater_resultats(resultats[colonne], colonne))

            if afficher_plots:
                if np.issubdtype(data.dtype, np.number):
                    # Visualisations pour variables numériques
                    if self.config.engine in ['seaborn', 'both']:
                        figs_seaborn = creer_visualisation_seaborn_numerique(data, colonne, self.config)
                        for fig in figs_seaborn:
                            plt.show()

                    if self.config.engine in ['plotly', 'both']:
                        fig_plotly = creer_visualisation_plotly_numerique(data, colonne, self.config)
                        fig_plotly.show()
                else:
                    # Visualisations pour variables catégorielles
                    if self.config.engine in ['seaborn', 'both']:
                        fig_seaborn = creer_visualisation_seaborn_categorielle(data, colonne, self.config)
                        plt.show()

                    if self.config.engine in ['plotly', 'both']:
                        fig_plotly = creer_visualisation_plotly_categorielle(data, colonne, self.config)
                        fig_plotly.show()


