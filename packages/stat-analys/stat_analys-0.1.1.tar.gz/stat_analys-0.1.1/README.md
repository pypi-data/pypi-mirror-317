# Stat Analys

`stat_analys` est un package Python pour l'analyse statistique univariee. Il permet de realiser des analyses statistiques detaillees et de generer des visualisations pour les variables numeriques et categorielles.

## Installation

Installez le package en utilisant la commande suivante :

```bash
pip install stat_analys
```

## Utilisation

Voici un exemple d'utilisation du package :

```python
import pandas as pd
from stat_analys.univariate_stat import AdvancedUnivariateStat
from stat_analys.configuration import ConfigurationPlot

# Creation d'un DataFrame exemple
data = {
    'numerique': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'categorielle': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
}
df = pd.DataFrame(data)

# Configuration des paramètres de visualisation
config = ConfigurationPlot(theme_plotly="plotly_dark", theme_seaborn="darkgrid")

# Creation de l'objet d'analyse
stat = AdvancedUnivariateStat(config)

# Analyse statistique avancee
resultats = stat.Analyser(df, colonnes=['numerique', 'categorielle'], afficher_plots=True)
```

## Fonctionnalites

- **Analyse statistique descriptive** : Moyennes, medianes, ecart-types, etc.
- **Tests de normalite** : Verifiez si vos donnees suivent une distribution normale.
- **Calcul des intervalles de confiance** : Obtenez des estimations robustes de vos donnees.
- **Visualisations** : Graphiques interactifs avec Plotly et esthetiques avec Seaborn.

## Contribution

Les contributions sont les bienvenues !

1. Ouvrez une issue pour discuter de vos idees d'amelioration ou signaler des bugs.
2. Faites un fork du depot.
3. Apportez vos modifications et soumettez une pull request.

Nous serons ravis de collaborer avec vous !
# stat_analys
