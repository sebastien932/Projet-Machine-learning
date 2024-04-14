from final.traitement_base_de_donnees import (
    _convertion_en_liste,
    _extraire_chiffre,
    _remplace_espace,
    _transforme_liste_en_df,
    _convertit_type_colone_en_numerique,
    _convertit_type_colonne_puissance,
    _creation_facteur_colonne_carburant,
    _remplacer_marques_rares,
    _drop_colonne_ligne,
    _drop_colonne_trop_na,
    _transforme_colonne_categorie,
    _traite_base_de_donnees,
)
import numpy as np
import pandas as pd


def test_convertion_en_liste():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)[0]
    assert resultat == [
        "https://www.autoscout24.fr/offres/porsche-cayenne-coupe-4-0-v8-680-ch-tiptronic-bva-turbo-s-e-hybrid-autres-gris-72c2fc62-de51-4817-ae89-176ec075066d",
        "€ 184\u202f900",
        "17\u202f500 km",
        "09/2022",
        "500 kW (680 CH)",
        "Boîte automatique",
        "3\u202f996 cm³",
        "8",
        "2\u202f535 kg",
        "SUV/4x4/Pick-Up",
        "Occasion",
        "NA",
        "5",
        "5",
        "Super Plus E10 98",
        "Super Plus E10 98",
        15,
        1,
        9,
        3,
        "Porsche",
        "Cayenne",
    ]


def test_extraire_chiffre():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    assert resultat[0] == [
        "https://www.autoscout24.fr/offres/porsche-cayenne-coupe-4-0-v8-680-ch-tiptronic-bva-turbo-s-e-hybrid-autres-gris-72c2fc62-de51-4817-ae89-176ec075066d",
        "€ 184\u202f900",
        "17\u202f500 km",
        "09/2022",
        "500 kW (680 CH)",
        "Boîte automatique",
        "3\u202f996 cm³",
        "8",
        "2\u202f535 kg",
        "SUV/4x4/Pick-Up",
        "Occasion",
        "NA",
        "5",
        "5",
        "Super Plus E10 98",
        "Super Plus E10 98",
        15,
        1,
        9,
        3,
        "Porsche",
        "Cayenne",
    ]


def test_remplace_espace():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    assert resultat[0] == [
        "https://www.autoscout24.fr/offres/porsche-cayenne-coupe-4-0-v8-680-ch-tiptronic-bva-turbo-s-e-hybrid-autres-gris-72c2fc62-de51-4817-ae89-176ec075066d",
        "184900",
        "17500",
        "09/2022",
        "500 kW (680 CH)",
        "Boîte automatique",
        "3996",
        "8",
        "2535",
        "SUV/4x4/Pick-Up",
        "Occasion",
        "NA",
        "5",
        "5",
        "Super Plus E10 98",
        "Super Plus E10 98",
        15,
        1,
        9,
        3,
        "Porsche",
        "Cayenne",
    ]


def test_transforme_liste_en_df():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    noms_colonnes = [
        "Lien",
        "Prix",
        "Km",
        "Annee",
        "Puissance",
        "Transmission",
        "Cylindree",
        "Vitesse",
        "Poids vide",
        "Carrosserie",
        "Etat",
        "Type moteur",
        "Siege",
        "Porte",
        "Carburant",
        "Classe emission",
        "Confort",
        "Divertissement",
        "Securite",
        "Autre",
        "Marque",
        "Modele",
    ]

    assert isinstance(df_resultat, pd.DataFrame)
    assert set(df_resultat.columns) == set(noms_colonnes)
    assert len(df_resultat) == len(resultat)


def test_convertit_type_colonne_en_numerique():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    assert pd.api.types.is_numeric_dtype(df_resultat["Prix"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Km"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Poids vide"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Cylindree"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Vitesse"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Siege"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Porte"])
    assert pd.api.types.is_numeric_dtype(df_resultat["Annee"])


def test_convertit_type_colonne_puissance():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    assert df_resultat["Puissance"][0] == 680


def test_convertit_type_colonne_carburant():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    df_resultat = _creation_facteur_colonne_carburant(df_resultat)
    categories_attendues = [np.nan, "AUTRE", "Essence", "Diesel"]
    assert set(df_resultat["Carburant"].unique()) == set(categories_attendues)


def test_remplacer_marques_rares():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    df_resultat = _creation_facteur_colonne_carburant(df_resultat)
    df_resultat = _remplacer_marques_rares(df_resultat, "Marque")
    elements = df_resultat["Marque"].value_counts()
    for element in elements:
        assert element > 60


def test_drop_colonne_ligne():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    df_resultat = _creation_facteur_colonne_carburant(df_resultat)
    df_resultat = _remplacer_marques_rares(df_resultat, "Marque")
    df_resultat = _drop_colonne_ligne(df_resultat)

    assert "Type moteur" not in df_resultat.columns
    assert "Classe emission" not in df_resultat.columns
    assert all(df_resultat["Prix"] >= 1000)
    assert all(df_resultat["Prix"] <= 100000)
    assert all((df_resultat["Km"] <= 400000) | (df_resultat["Km"].isna()))
    assert all((df_resultat["Km"] >= 10) | (df_resultat["Km"].isna()))
    assert all((df_resultat["Vitesse"] <= 10) | (df_resultat["Vitesse"].isna()))
    assert all((df_resultat["Cylindree"] >= 400) | (df_resultat["Cylindree"].isna()))
    assert all((df_resultat["Porte"] <= 5) | (df_resultat["Porte"].isna()))
    assert all((df_resultat["Porte"] >= 2) | (df_resultat["Porte"].isna()))
    assert "Etat" not in df_resultat.columns


def test_drop_colonne_trop_na():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    df_resultat = _creation_facteur_colonne_carburant(df_resultat)
    df_resultat = _remplacer_marques_rares(df_resultat, "Marque")
    df_resultat = _drop_colonne_ligne(df_resultat)
    df_resultat = _drop_colonne_trop_na(df_resultat)
    elements = df_resultat.isna().sum()
    for element in elements:
        assert element < 8000


def test_transforme_colonne_categorie():
    fichier = "BASE.txt"
    resultat = _convertion_en_liste(fichier)
    resultat = _extraire_chiffre(resultat)
    resultat = _remplace_espace(resultat)
    df_resultat = _transforme_liste_en_df(resultat)
    df_resultat = _convertit_type_colone_en_numerique(df_resultat)
    df_resultat = _convertit_type_colonne_puissance(df_resultat)
    df_resultat = _creation_facteur_colonne_carburant(df_resultat)
    df_resultat = _remplacer_marques_rares(df_resultat, "Marque")
    df_resultat = _drop_colonne_ligne(df_resultat)
    df_resultat = _drop_colonne_trop_na(df_resultat)
    df_resultat, data_resultat = _transforme_colonne_categorie(df_resultat)
    assert pd.api.types.is_categorical_dtype(data_resultat["Marque"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Transmission"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Carburant"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Carrosserie"])
    assert "Transmission" not in df_resultat.columns
    assert "Carrosserie" not in df_resultat.columns
    assert "Carburant" not in df_resultat.columns


def test_traite_base_de_donnees():
    fichier = "BASE.txt"
    df_resultat, data_resultat = _traite_base_de_donnees(fichier)
    assert pd.api.types.is_categorical_dtype(data_resultat["Marque"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Transmission"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Carburant"])
    assert pd.api.types.is_categorical_dtype(data_resultat["Carrosserie"])
    assert "Transmission" not in df_resultat.columns
    assert "Carrosserie" not in df_resultat.columns
    assert "Carburant" not in df_resultat.columns
