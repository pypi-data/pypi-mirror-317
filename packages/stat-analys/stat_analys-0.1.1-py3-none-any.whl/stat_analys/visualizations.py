# stat_analys/visualizations.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from typing import Tuple
from .configuration import ConfigurationPlot

def creer_visualisation_seaborn_numerique(
    data: pd.Series,
    nom: str,
    config: ConfigurationPlot
) -> Tuple[plt.Figure, plt.Figure]:
    """
    Création des visualisations Seaborn pour variables numériques.
    """
    # Figure 1: Distribution et KDE
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Distribution avec KDE
    sns.histplot(
        data=data,
        kde=config.afficher_kde,
        ax=ax1,
        stat="density",
        alpha=config.alpha
    )
    if config.afficher_rug:
        sns.rugplot(data=data, ax=ax1, color="red", alpha=0.3)
    ax1.set_title(f"Distribution de {nom}")

    # Q-Q plot
    stats.probplot(data.dropna(), dist="norm", plot=ax2)
    ax2.set_title("Q-Q Plot")

    # Figure 2: Boxplot et Violin plot
    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 5))

    # Boxplot
    sns.boxplot(y=data, ax=ax3)
    ax3.set_title("Boîte à moustaches")

    # Violin plot
    sns.violinplot(y=data, ax=ax4)
    ax4.set_title("Violin Plot")

    return fig1, fig2

def creer_visualisation_seaborn_categorielle(
    data: pd.Series,
    nom: str,
    config: ConfigurationPlot
) -> plt.Figure:
    """
    Création des visualisations Seaborn pour variables catégorielles.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), dpi=200)

    # Countplot avec palette de couleurs personnalisée
    sns.countplot(
        y=data,
        ax=ax1,
        palette=config.palette_categorielle,
        order=data.value_counts().index,
        legend=True
    )
    ax1.set_title(f"Distribution des catégories de {nom}")
    ax1.tick_params(axis='x', rotation=config.rotation_labels)

    # Pie chart
    plt.sca(ax2)
    data.value_counts().plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=sns.color_palette(config.palette_categorielle),
    )
    ax2.set_title("Répartition en pourcentage")

    return fig

def creer_visualisation_plotly_numerique(data: pd.Series, nom: str, config: ConfigurationPlot):
    """
    Création des visualisations Plotly pour variables numériques.
    """
    # Création du subplot Plotly avec plus de détails statistiques
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Distribution et KDE",
            "Boîte à moustaches avec points",
            "Violin Plot avec statistiques",
            "Q-Q Plot avec IC"
        )
    )

    # Distribution avec KDE
    if config.afficher_kde:
        kde = stats.gaussian_kde(data.dropna())
        x_range = np.linspace(data.min(), data.max(), 200)  # Plus de points pour une courbe plus lisse
        kde_values = kde(x_range)

    hist = go.Histogram(
        x=data,
        name="Distribution",
        nbinsx=config.nbins,
        opacity=config.alpha,
        histnorm='probability density'
    )
    fig.add_trace(hist, row=1, col=1)

    if config.afficher_kde:
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=kde_values,
                name="KDE",
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )

    # Boîte à moustaches avancée
    fig.add_trace(
        go.Box(
            y=data,
            name=nom,
            boxpoints='outliers',
            notched=True,  # Ajoute une encoche pour l'IC de la médiane
            boxmean=True   # Montre la moyenne
        ),
        row=1, col=2
    )

    # Violin plot avec statistiques
    fig.add_trace(
        go.Violin(
            y=data,
            name=nom,
            box_visible=True,
            meanline_visible=True,
            points='outliers'
        ),
        row=2, col=1
    )

    # Q-Q plot avec intervalles de confiance
    qq = stats.probplot(data.dropna())
    theoretical_quantiles = qq[0][0]
    sample_quantiles = qq[0][1]

    # Calcul des intervalles de confiance pour le Q-Q plot
    n = len(sample_quantiles)
    confidence = 0.95
    z = stats.norm.ppf((1 + confidence) / 2)
    se = stats.norm.std() * np.sqrt(1 + 1/n)
    ci = z * se

    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=sample_quantiles,
            mode='markers',
            name='Q-Q Plot',
            marker=dict(color='blue')
        ),
        row=2, col=2
    )

    # Ligne de référence Q-Q
    line_x = np.linspace(
        min(theoretical_quantiles),
        max(theoretical_quantiles),
        100
    )
    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_x,
            mode='lines',
            name='Référence',
            line=dict(color='red', dash='dash')
        ),
        row=2, col=2
    )

    # Intervalles de confiance Q-Q
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=theoretical_quantiles + ci,
            mode='lines',
            name='IC 95%',
            line=dict(color='gray', dash='dot'),
            showlegend=False
        ),
        row=2, col=2
    )

    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=theoretical_quantiles - ci,
            mode='lines',
            name='IC 95%',
            line=dict(color='gray', dash='dot'),
            showlegend=False
        ),
        row=2, col=2
    )

    # Mise à jour du layout
    fig.update_layout(
        height=config.hauteur,
        width=config.largeur,
        title_text=f"Analyse détaillée de {nom}",
        template=config.theme_plotly,
        showlegend=True
    )

    return fig

def creer_visualisation_plotly_categorielle(data: pd.Series, nom: str, config: ConfigurationPlot):
    """
    Création des visualisations Plotly pour variables catégorielles.
    """
    # Calcul des proportions et IC
    counts = data.value_counts()
    proportions = data.value_counts(normalize=True)
    n = len(data)

    # Calcul des IC pour les proportions (méthode Wilson)
    ic_inf = []
    ic_sup = []
    for p in proportions:
        z = stats.norm.ppf((1 + config.niveau_confiance) / 2)
        denominator = 1 + z**2/n
        p_adj = (p + z**2/(2*n))/denominator
        ci_width = z*np.sqrt(p*(1-p)/n + z**2/(4*n**2))/denominator
        ic_inf.append(max(0, p_adj - ci_width))
        ic_sup.append(min(1, p_adj + ci_width))

    # Création des subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            "Distribution des catégories avec IC",
            "Diagramme circulaire avec proportions"
        ),
        specs=[[{"type": "bar"}, {"type": "pie"}]]
    )

    # Barplot avec IC
    fig.add_trace(
        go.Bar(
            x=counts.index,
            y=proportions,
            name="Proportion",
            text=[f"{v:.1%}" for v in proportions],
            textposition='auto',
            error_y=dict(
                type='data',
                symmetric=False,
                array=[sup - p for p, sup in zip(proportions, ic_sup)],
                arrayminus=[p - inf for p, inf in zip(proportions, ic_inf)],
                visible=True
            )
        ),
        row=1, col=1
    )

    # Pie chart amélioré
    fig.add_trace(
        go.Pie(
            labels=counts.index,
            values=counts,
            hole=0.3,
            textinfo='percent+label',
            hoverinfo='label+percent+value',
            textposition='inside',
            insidetextorientation='radial'
        ),
        row=1, col=2
    )

    # Mise à jour du layout
    fig.update_layout(
        height=config.hauteur,
        width=config.largeur,
        title_text=f"Analyse des catégories de {nom}",
        template=config.theme_plotly,
        showlegend=True,
        # Mise à jour des annotations pour plus de clarté
        annotations=[
            dict(
                x=0.25,
                y=1.1,
                text=f"Distribution avec IC {config.niveau_confiance*100:.0f}%",
                showarrow=False,
                xref="paper",
                yref="paper"
            ),
            dict(
                x=0.75,
                y=1.1,
                text="Répartition proportionnelle",
                showarrow=False,
                xref="paper",
                yref="paper"
            )
        ]
    )

    return fig
