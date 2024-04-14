import tkinter as tk
from final.application import Application, Onglet1Content, Onglet2Content
import unittest
from unittest.mock import Mock, MagicMock, patch
import webbrowser


def test_efface_filtre():
    app = Application()
    onglet1_content = Onglet1Content(app)
    onglet1_content.choice_var1.set("Sélectionné")
    onglet1_content.choice_var2.set("Sélectionné")
    onglet1_content.choice_var3.set("Sélectionné")
    onglet1_content.choice_var_marque.set("Sélectionné")
    onglet1_content.choice_var_modele.set("Sélectionné")
    onglet1_content.min_value_var.set(100)
    onglet1_content.max_value_var.set(200)
    onglet1_content.min_price_var.set(5000)
    onglet1_content.max_price_var.set(10000)

    onglet1_content.clear_filters()

    assert onglet1_content.choice_var1.get() == "Tous"
    assert onglet1_content.choice_var2.get() == "Tous"
    assert onglet1_content.choice_var3.get() == "Tous"
    assert onglet1_content.choice_var_marque.get() == "Tous"
    assert onglet1_content.choice_var_modele.get() == "Tous"
    assert onglet1_content.min_value_var.get() == 0.0
    assert onglet1_content.max_value_var.get() == 0.0
    assert onglet1_content.min_price_var.get() == 0.0
    assert onglet1_content.max_price_var.get() == 0.0
    app.destroy()


def test_filtre():
    app = Application()
    onglet1_content = Onglet1Content(app)

    onglet1_content.choice_var1.set("Sélectionné")
    onglet1_content.choice_var2.set("Sélectionné")
    onglet1_content.choice_var3.set("Sélectionné")
    onglet1_content.choice_var_marque.set("Sélectionné")
    onglet1_content.choice_var_modele.set("Sélectionné")
    onglet1_content.min_value_var.set(100)
    onglet1_content.max_value_var.set(200)
    onglet1_content.min_price_var.set(5000)
    onglet1_content.max_price_var.set(10000)
    onglet1_content.min_puissance_var.set(100)
    onglet1_content.max_puissance_var.set(200)
    onglet1_content.min_annee_var.set(2010)
    onglet1_content.max_annee_var.set(2020)
    assert onglet1_content.choice_var1.get() != "Tous"
    assert onglet1_content.choice_var2.get() != "Tous"
    assert onglet1_content.choice_var3.get() != "Tous"
    assert onglet1_content.choice_var_marque.get() != "Tous"
    assert onglet1_content.choice_var_modele.get() != "Tous"
    assert onglet1_content.min_value_var.get() != 0.0
    assert onglet1_content.max_value_var.get() != 0.0
    assert onglet1_content.min_price_var.get() != 0.0
    assert onglet1_content.max_price_var.get() != 0.0
    assert onglet1_content.min_annee_var.get() != 0.0
    assert onglet1_content.max_annee_var.get() != 0.0
    assert onglet1_content.min_puissance_var.get() != 0.0
    assert onglet1_content.max_puissance_var.get() != 0.0
    filter_button = onglet1_content.root.children["!button"]
    filter_button.invoke()
    app.destroy()


def test_changement_affichage():
    app = Application()
    onglet1_content = Onglet1Content(app)
    onglet1_content.min_value_var.set(100)
    onglet1_content.max_value_var.set(200)
    onglet1_content.min_price_var.set(5000)
    onglet1_content.max_price_var.set(10000)
    filter_button = onglet1_content.root.children["!button"]
    filter_button.invoke()
    affichage_resultat1 = onglet1_content.tree.get_children()
    onglet1_content.clear_filters()
    affichage_resultat2 = onglet1_content.tree.get_children()
    assert len(affichage_resultat1) < len(affichage_resultat2)
    app.destroy()


class TestOnglet2Content(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = Onglet2Content(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_update_graph_prix_note_moyenne(self):
        self.app.selected_graph_var.set("Prix et note Moyenne par Marque")
        self.app.update_graph(Mock())
        self.assertNotEqual(self.app.fig, None)

    def test_update_graph_matrice_correlation(self):
        self.app.selected_graph_var.set("Matrice de corrélation")
        self.app.update_graph(Mock())
        self.assertNotEqual(self.app.fig, None)


class OuvreLien(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.mock_tree = MagicMock()
        self.mock_df = MagicMock()
        self.instance = Onglet1Content(self.root)

    @patch("webbrowser.open")
    def test_on_treeview_select_with_http_link(self, webbrowser_open_mock):
        event = MagicMock()

        self.instance.tree.selection = MagicMock(return_value=["item_id"])

        self.instance.tree.item = MagicMock(
            return_value={
                "values": [
                    "https://www.autoscout24.fr/offres/volkswagen-lt-camping-car-diesel-blanc-fe35e0ae-4bac-4604-877c-c9524f182455"
                ]
            }
        )
        self.instance.on_treeview_select(event)

        webbrowser_open_mock = webbrowser.open
        webbrowser_open_mock.assert_called_once_with(
            "https://www.autoscout24.fr/offres/volkswagen-lt-camping-car-diesel-blanc-fe35e0ae-4bac-4604-877c-c9524f182455"
        )


class QuitApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.instance = Application()

    @patch("sys.exit")
    @patch("tkinter.Tk.destroy")
    def test_quit_application(self, destroy_mock, sys_exit_mock):
        self.instance.quit_application()
        destroy_mock.assert_called_once()
        sys_exit_mock.assert_called_once()
