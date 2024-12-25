# tests/test_configuration.py
import unittest
from stat_analys.configuration import ConfigurationPlot

class TestConfigurationPlot(unittest.TestCase):
    def test_default_values(self):
        config = ConfigurationPlot()
        self.assertEqual(config.theme_plotly, "plotly_white")
        self.assertEqual(config.theme_seaborn, "whitegrid")
        self.assertEqual(config.hauteur, 600)
        self.assertEqual(config.largeur, 1000)
        self.assertEqual(config.taille_police, 12)
        self.assertEqual(config.palette, "viridis")
        self.assertEqual(config.rotation_labels, 45)
        self.assertEqual(config.afficher_kde, True)
        self.assertEqual(config.afficher_rug, True)
        self.assertEqual(config.nbins, 30)
        self.assertEqual(config.style_boxplot, "box")
        self.assertEqual(config.alpha, 1.0)
        self.assertEqual(config.engine, "seaborn")
        self.assertEqual(config.niveau_confiance, 0.95)
        self.assertEqual(config.palette_categorielle, "husl")

if __name__ == '__main__':
    unittest.main()
