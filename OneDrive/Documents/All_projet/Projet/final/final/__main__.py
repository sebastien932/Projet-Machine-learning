from .parcours_url import _fichier_texte_en_liste, _parcours_liens
from .entrainement_du_modele import _initialise_parametres_modele
from .nouveau_modele import _extra, _boosting, _random_forest, _res_neuro
from .application import Application
import sys
from typing import Union
import pandas as pd


def enregistre_dataframe(chemin_fichier: str, t=1):
    """
    Enregistre les données récupérées à partir des liens dans un fichier texte.
    """
    LIENS = _fichier_texte_en_liste(chemin_fichier)
    data: list
    data = []
    data = _parcours_liens(LIENS, t, data)
    nom_fichier = "BASE_DE_DONNEES.txt"
    with open(nom_fichier, "w") as fichier:
        for element in data:
            fichier.write(str(element) + "\n")


def entrainement_modele(chemin_fichier: str):
    _, data, _, X, _, X_tr, y_tr, X_te, y_te, Extra = _initialise_parametres_modele(
        chemin_fichier
    )
    Extra.fit(X_tr, y_tr)
    n_estimators = Extra.named_steps["entrainement"].n_estimators
    max_depth = Extra.named_steps["entrainement"].max_depth
    min_samples_split = Extra.named_steps["entrainement"].min_samples_split
    min_samples_leaf = Extra.named_steps["entrainement"].min_samples_leaf
    score_tr = round(Extra.score(X_tr, y_tr), 2)
    score_te = round(Extra.score(X_te, y_te), 2)
    data_extra = pd.DataFrame(
        {
            "": "ExtraTreesRegressor",
            "n_estimators": [n_estimators],
            "max_depth": [max_depth],
            "min_samples_split": [min_samples_split],
            "min_samples_leaf": [min_samples_leaf],
            "score_train": [score_tr],
            "score_test": [score_te],
        }
    )
    data["Prix_pred"] = Extra.predict(X)
    data["Note"] = (data["Prix_pred"] - data["Prix"]) / data["Prix_pred"] * 10
    data.to_json("donnees.json", orient="records", lines=True)
    data_extra.to_json("modele.json", orient="records", lines=True)


def entrainement_nouveau_modele(LIEN1: str, LIEN2: str):
    df_extra, cv_extra, data, X = _extra(LIEN1, LIEN2)
    df_rfr, cv_rfr = _random_forest(LIEN1, LIEN2)
    df_mlp, cv_mlp = _res_neuro(LIEN1, LIEN2)
    df_gbr, cv_gbr = _boosting(LIEN1, LIEN2)
    score_tr_extra = df_extra.loc[
        df_extra["Paramètre"] == "score_test", "Valeur"
    ].values[0]
    score_tr_rfr = df_rfr.loc[df_extra["Paramètre"] == "score_test", "Valeur"].values[0]
    score_tr_mlp = df_mlp.loc[df_extra["Paramètre"] == "score_test", "Valeur"].values[0]
    score_tr_gbr = df_gbr.loc[df_extra["Paramètre"] == "score_test", "Valeur"].values[0]

    if (
        score_tr_extra >= score_tr_rfr
        and score_tr_extra >= score_tr_mlp
        and score_tr_extra >= score_tr_gbr
    ):
        data["Prix_pred"] = cv_extra.predict(X)
        nouvelle_ligne = {"Paramètre": "Modele", "Valeur": "ExtraTreesRegressor"}
        df_extra = pd.concat(
            [pd.DataFrame([nouvelle_ligne]), df_extra], ignore_index=True
        )
        df_extra.to_json("modele.json", orient="records")
    elif score_tr_rfr >= score_tr_mlp and score_tr_rfr >= score_tr_gbr:
        data["Prix_pred"] = cv_rfr.predict(X)
        nouvelle_ligne = {"Paramètre": "Modele", "Valeur": "RandomForestRegressor"}
        df_rfr = pd.DataFrame(
            [nouvelle_ligne] + df_rfr.values.tolist(), columns=df_rfr.columns
        )
        df_rfr.reset_index(drop=True, inplace=True)
        df_rfr.to_json("modele.json", orient="records")
    elif score_tr_mlp >= score_tr_gbr:
        data["Prix_pred"] = cv_mlp.predict(X)
        nouvelle_ligne = {"Paramètre": "Modele", "Valeur": "MLPRegressor"}
        df_mlp = pd.DataFrame(
            [nouvelle_ligne] + df_mlp.values.tolist(), columns=df_mlp.columns
        )
        df_mlp.reset_index(drop=True, inplace=True)
        df_mlp.to_json("modele.json", orient="records")
    else:
        data["Prix_pred"] = cv_gbr.predict(X)
        nouvelle_ligne = {"Paramètre": "Modele", "Valeur": "GradientBoostingRegressor"}
        df_gbr = pd.DataFrame(
            [nouvelle_ligne] + df_gbr.values.tolist(), columns=df_gbr.columns
        )
        df_gbr.reset_index(drop=True, inplace=True)
        df_gbr.to_json("modele.json", orient="records")

    data["Note"] = (data["Prix_pred"] - data["Prix"]) / data["Prix_pred"] * 10
    data.to_json("donnees.json", orient="records", lines=True)


def lancement_application():
    """
    Lance l'application tkinter.
    """
    app = Application()
    app.state("zoomed")
    app.mainloop()


if __name__ == "__main__":
    fonction_a_executer = sys.argv[1]
    if fonction_a_executer == "enregistre_dataframe":
        chemin_fichier = sys.argv[2]
        t: Union[int, None]
        try:
            t = int(sys.argv[3])
        except IndexError:
            t = None
        if not isinstance(t, int):
            enregistre_dataframe(chemin_fichier)
        else:
            enregistre_dataframe(chemin_fichier, t=sys.argv[3])
    elif fonction_a_executer == "entrainement_modele":
        chemin_fichier = sys.argv[2]
        entrainement_modele(chemin_fichier)
    elif fonction_a_executer == "entrainement_nouveau_modele":
        chemin_fichier1 = sys.argv[2]
        chemin_fichier2 = sys.argv[3]
        entrainement_nouveau_modele(chemin_fichier1, chemin_fichier2)
    elif fonction_a_executer == "lancement_application":
        lancement_application()
    else:
        print(f"La fonction '{fonction_a_executer}' n'est pas reconnue.")
        sys.exit(1)
