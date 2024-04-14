"""Description.

Prépare la base de données pour l'entrainement des modèles de machine learning.
"""

import numpy as np
import ast
import re
import pandas as pd
from typing import Union


def _convertion_en_liste(fichier: str) -> list[list[Union[str, int]]]:
    """
    Convertit les données d'un fichier texte en liste de listes.

    """
    resultat = []
    with open(fichier, "r") as f:
        lignes = f.readlines()
        elements = [ast.literal_eval(ligne) for ligne in lignes]
        resultat.extend(elements)
    return resultat


def _extraire_chiffre(
    matrice: list[list[Union[str, int]]]
) -> list[list[Union[str, int]]]:
    """
    Extrait les chiffres des éléments de la matrice qui sont des chaînes de caractères.
    """
    prix: str
    matches: list
    ligne: int
    element: int
    for ligne in range(len(matrice)):
        for element in range(len(matrice[ligne])):
            if isinstance(matrice[ligne][element], str):
                prix = str(matrice[ligne][element])
                matches = re.findall(r"\u202f([^\s\']+)", prix)
                if matches and len(matches[0]) > 3:
                    matrice[ligne][element] = prix[:-1]
    return matrice


def _remplace_espace(
    resultat: list[list[Union[str, int]]]
) -> list[list[Union[str, int]]]:
    """
    Remplace les espaces inutiles dans la matrice résultante."""
    resultat = [
        [
            element.replace("\u202f", "")
            .replace(" km", "")
            .replace("€ ", "")
            .replace(" cm³", "")
            .replace(" kg", "")
            if isinstance(element, str)
            else element
            for element in sous_liste
        ]
        for sous_liste in resultat
    ]
    return resultat


def _transforme_liste_en_df(resultat: list[list[Union[str, int]]]) -> pd.DataFrame:
    """Transforme en dataframe et définit les noms de colonne."""
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
    df = pd.DataFrame(resultat, columns=noms_colonnes)
    return df


def _convertit_type_colone_en_numerique(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les types des colonnes numériques d'un DataFrame en types numériques."""
    df.replace("NA", np.nan, inplace=True)
    df["Annee"] = pd.to_datetime(df["Annee"], format="%m/%Y")
    df["Annee"] = df["Annee"].dt.year
    df[
        ["Prix", "Km", "Poids vide", "Cylindree", "Vitesse", "Siege", "Porte", "Annee"]
    ] = df[
        ["Prix", "Km", "Poids vide", "Cylindree", "Vitesse", "Siege", "Porte", "Annee"]
    ].apply(
        pd.to_numeric, errors="coerce"
    )

    return df


def _convertit_type_colonne_puissance(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme la colonne Puissance en float"""
    df["Puissance"] = df["Puissance"].str.extract(r"\((.*?)\)")
    df["Puissance"] = df["Puissance"].str.replace("CH", "")
    df["Puissance"] = pd.to_numeric(df["Puissance"])
    return df


def _creation_facteur_colonne_carburant(df: pd.DataFrame) -> pd.DataFrame:
    """Créée des catégories plus large pour la colonne Carburant"""
    df["Carburant"] = df["Carburant"].replace({"Super Plus E10 98": "Essence"})
    df["Carburant"] = df["Carburant"].replace({"Ethanol": "Essence"})
    df["Carburant"] = df["Carburant"].replace(
        {"Diesel (Filtre à particules)": "Diesel"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Essence (Filtre à particules)": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace({"Autres (Filtre à particules)": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace({"Autres": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace({"Super Plus 98": "Essence"})
    df["Carburant"] = df["Carburant"].replace({"Super 95": "Essence"})
    df["Carburant"] = df["Carburant"].replace({"Super E10 95": "Essence"})
    df["Carburant"] = df["Carburant"].replace(
        {"Super 95 (Filtre à particules)": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace({"Essence E10 91": "Essence"})
    df["Carburant"] = df["Carburant"].replace(
        {
            "Gaz de pétrole liquéfié / Super E10 95 / Super Plus E10 98 / Super 95 / Super Plus 98": "Essence"
        }
    )
    df["Carburant"] = df["Carburant"].replace({"GPL (Filtre à particules)": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace(
        {"Electrique (Filtre à particules)": "AUTRE"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Super E10 95 (Filtre à particules)": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace({"Gaz de pétrole liquéfié": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace({"Diesel écologique": "Diesel"})
    df["Carburant"] = df["Carburant"].replace(
        {"Diesel écologique (Filtre à particules)": "Diesel"}
    )
    df["Carburant"] = df["Carburant"].replace({"Essence 91": "Essence"})
    df["Carburant"] = df["Carburant"].replace(
        {
            "Gaz de pétrole liquéfié / Super E10 95 / Super Plus E10 98 / Super 95 / Super Plus 98 / Essence E10 91": "Essence"
        }
    )
    df["Carburant"] = df["Carburant"].replace({"Gaz naturel H": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace(
        {"Gaz de pétrole liquéfié / Essence E10 91 / Super 95": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Super Plus E10 98 (Filtre à particules)": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Gaz de pétrole liquéfié / Super E10 95": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Gaz de pétrole liquéfié / Super Plus E10 98": "Essence"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Vegetable oil / Diesel / Diesel écologique": "Diesel"}
    )
    df["Carburant"] = df["Carburant"].replace(
        {"Gaz naturel L (Filtre à particules)": "AUTRE"}
    )
    df["Carburant"] = df["Carburant"].replace({"GPL": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace({"GNL": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace({"Electrique": "AUTRE"})
    df["Carburant"] = df["Carburant"].replace(
        {
            "Ethanol / Super E10 95 / Essence 91 / Super Plus E10 98 / Super 95 / Super Plus 98 / Essence E10 91": "Essence"
        }
    )
    return df


def _remplacer_marques_rares(
    df: pd.DataFrame, colonne_marque: str, seuil=60, nouvelle_marque="AUTRE"
) -> pd.DataFrame:
    """Remplace la catégories des marques avec un nombre inférieur au seuil par la catgéorie autre"""
    comptage_marques = df[colonne_marque].value_counts()
    marques_rares = comptage_marques[comptage_marques < seuil].index.tolist()
    df[colonne_marque] = df[colonne_marque].replace(marques_rares, nouvelle_marque)
    return df


def _drop_colonne_ligne(df: pd.DataFrame) -> pd.DataFrame:
    """Enlève les colonne inutilisable et les valeurs aberrantes"""
    df.drop(columns=["Type moteur"], inplace=True)
    df.drop(columns=["Classe emission"], inplace=True)
    df.drop_duplicates(inplace=True)
    df.drop(df[df["Prix"] < 1000].index, inplace=True)
    df.drop(df[df["Prix"] > 100000].index, inplace=True)
    df.drop(df[df["Km"] < 10].index, inplace=True)
    df.drop(df[df["Km"] > 400000].index, inplace=True)
    df.drop(df[df["Vitesse"] > 10].index, inplace=True)
    df.drop(df[df["Cylindree"] < 400].index, inplace=True)
    df.drop(df[(df["Cylindree"] > 5000) & (df["Puissance"] < 200)].index, inplace=True)
    df.drop(df[(df["Porte"] > 5)].index, inplace=True)
    df.drop(df[(df["Porte"] < 2)].index, inplace=True)
    df.drop("Etat", axis=1, inplace=True)
    return df


def _drop_colonne_trop_na(df: pd.DataFrame, seuil=8000) -> pd.DataFrame:
    """Enlève les colonnes qui ont un nombre d'individus en NA supérieur au seuil."""
    df = df.dropna(axis=1, thresh=len(df) - seuil)
    return df


def _transforme_colonne_categorie(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    "Transforme le type de certaine colonne en catégorie, créé un nouveau data frame et créé des dummies pour les colonnes avec un nombre de catégorie pas trop important"
    df["Marque"] = df["Marque"].astype("category")
    df["Transmission"] = df["Transmission"].astype("category")
    df["Carrosserie"] = df["Carrosserie"].astype("category")
    df["Carburant"] = df["Carburant"].astype("category")
    data = df.copy()
    df = pd.get_dummies(df, columns=["Transmission"], drop_first=True)
    df = pd.get_dummies(df, columns=["Carrosserie"], drop_first=True)
    df = pd.get_dummies(df, columns=["Carburant"], drop_first=True)
    return df, data


def _traite_base_de_donnees(fichier: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    "Traite la base de donnée pour l'entrainement des modelèles de machine learning"
    resultat = _convertion_en_liste(fichier)
    resultat1 = _extraire_chiffre(resultat)
    resultat2 = _remplace_espace(resultat1)
    df = _transforme_liste_en_df(resultat2)
    df = _convertit_type_colone_en_numerique(df)
    df = _convertit_type_colonne_puissance(df)
    df = _creation_facteur_colonne_carburant(df)
    df = _remplacer_marques_rares(df, "Marque")
    df = _drop_colonne_ligne(df)
    df = _drop_colonne_trop_na(df)
    df, data = _transforme_colonne_categorie(df)
    return df, data
