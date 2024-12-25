# stat_analys/configuration.py
from dataclasses import dataclass

@dataclass
class ConfigurationPlot:
    """
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
    theme_plotly: str = "plotly_white"
    theme_seaborn: str = "whitegrid"
    hauteur: int = 600
    largeur: int = 1000
    taille_police: int = 12
    palette: str = "viridis"
    rotation_labels: int = 45
    afficher_kde: bool = True
    afficher_rug: bool = True
    nbins: int = 30
    style_boxplot: str = "box"  # 'box' ou 'violin'
    alpha: float = 1.0
    engine: str = "seaborn"  # 'seaborn', 'plotly', ou 'both'
    niveau_confiance: float = 0.95
    palette_categorielle: str = "husl"  # Pour les variables catégorielles
