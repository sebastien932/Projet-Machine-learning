from final.traitement_base_de_donnees import _traite_base_de_donnees
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.ensemble import (  # type: ignore
    ExtraTreesRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor,
)  # type: ignore
from sklearn.neural_network import MLPRegressor  # type: ignore
from sklearn.impute import KNNImputer  # type: ignore
from sklearn.model_selection import GridSearchCV, train_test_split  # type: ignore
from sklearn.preprocessing import StandardScaler, OneHotEncoder  # type: ignore
from sklearn.compose import ColumnTransformer  # type: ignore
import pandas as pd  # type: ignore


def transforme_json(LIEN):
    df, data = _traite_base_de_donnees(LIEN)
    df = pd.DataFrame(df)
    data.to_json("data.json", orient="records", lines=True)
    df.to_json("df.json", orient="records", lines=True)


def _initialise_variables_nouveau_modele(LIEN1: str, LIEN2: str) -> tuple:
    df = pd.read_json(LIEN1, orient="records", lines=True)
    data = pd.read_json(LIEN2, orient="records", lines=True)
    X = df[
        [
            "Km",
            "Annee",
            "Siege",
            "Porte",
            "Confort",
            "Marque",
            "Modele",
            "Transmission_Boîte manuelle",
            "Transmission_Semi-automatique",
            "Carrosserie_Berline",
            "Carrosserie_Break",
            "Carrosserie_Cabriolet",
            "Carrosserie_Citadine",
            "Carrosserie_Coupé",
            "Carrosserie_Monospace",
            "Carrosserie_SUV/4x4/Pick-Up",
            "Carrosserie_Utilitaire",
            "Carburant_Diesel",
            "Carburant_Essence",
        ]
    ]
    y = df["Prix"].values
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3)

    cat_fit = [
        "Marque",
        "Modele",
        "Transmission_Boîte manuelle",
        "Transmission_Semi-automatique",
        "Carrosserie_Berline",
        "Carrosserie_Break",
        "Carrosserie_Cabriolet",
        "Carrosserie_Citadine",
        "Carrosserie_Coupé",
        "Carrosserie_Monospace",
        "Carrosserie_SUV/4x4/Pick-Up",
        "Carrosserie_Utilitaire",
        "Carburant_Diesel",
        "Carburant_Essence",
    ]
    temp = ColumnTransformer([("cat", OneHotEncoder(), cat_fit)]).fit(X)
    cats = temp.named_transformers_["cat"].categories_
    cat_tr = OneHotEncoder(categories=cats, sparse_output=False)

    num_fit = ["Km", "Annee", "Siege", "Porte", "Confort"]
    num_tr = StandardScaler()

    data_tr = ColumnTransformer([("num", num_tr, num_fit), ("cat", cat_tr, cat_fit)])
    return df, data, data_tr, X, y, X_tr, y_tr, X_te, y_te


def _extra(LIEN1: str, LIEN2: str) -> tuple:
    (
        df,
        data,
        data_tr,
        X,
        y,
        X_tr,
        y_tr,
        X_te,
        y_te,
    ) = _initialise_variables_nouveau_modele(LIEN1, LIEN2)
    Extra = Pipeline(
        [
            ("features", data_tr),
            ("imputation", KNNImputer(n_neighbors=12)),
            ("entrainement", ExtraTreesRegressor()),
        ]
    )
    cv_extra = GridSearchCV(
        estimator=Extra,
        param_grid={
            "imputation__n_neighbors": range(4, 16, 4),
            "entrainement__n_estimators": range(10, 51, 10),
            "entrainement__max_depth": [None, 10, 20, 30],
            "entrainement__min_samples_split": range(1, 6, 1),
            "entrainement__min_samples_leaf": range(1, 10, 2),
        },
        n_jobs=-1,
    )
    cv_extra.fit(X_tr, y_tr)
    indice_meilleur = cv_extra.cv_results_["rank_test_score"].argmin()
    meilleurs_parametres = cv_extra.cv_results_["params"][indice_meilleur]
    meilleurs_parametres["score_entrainement"] = round(cv_extra.score(X_tr, y_tr), 2)
    meilleurs_parametres["score_test"] = round(cv_extra.score(X_te, y_te), 2)
    df_extra = pd.DataFrame(
        list(meilleurs_parametres.items()), columns=["Paramètre", "Valeur"]
    )
    return df_extra, cv_extra, data, X


def _random_forest(LIEN1: str, LIEN2: str) -> tuple:
    (
        df,
        data,
        data_tr,
        X,
        y,
        X_tr,
        y_tr,
        X_te,
        y_te,
    ) = _initialise_variables_nouveau_modele(LIEN1, LIEN2)
    rfr = Pipeline(
        [
            ("features", data_tr),
            ("imputation", KNNImputer()),
            ("entrainement", RandomForestRegressor()),
        ]
    )
    cv_rfr = GridSearchCV(
        estimator=rfr,
        param_grid={
            "imputation__n_neighbors": range(4, 16, 4),
            "entrainement__n_estimators": range(10, 100, 10),
            "entrainement__max_depth": range(1, 10, 1),
        },
    )
    cv_rfr.fit(X_tr, y_tr)
    indice_meilleur = cv_rfr.cv_results_["rank_test_score"].argmin()
    meilleurs_parametres = cv_rfr.cv_results_["params"][indice_meilleur]
    meilleurs_parametres["score_entrainement"] = round(cv_rfr.score(X_tr, y_tr), 2)
    meilleurs_parametres["score_test"] = round(cv_rfr.score(X_te, y_te), 2)
    df_rfr = pd.DataFrame(
        list(meilleurs_parametres.items()), columns=["Paramètre", "Valeur"]
    )
    return df_rfr, cv_rfr


def _res_neuro(LIEN1: str, LIEN2: str) -> tuple:
    (
        df,
        data,
        data_tr,
        X,
        y,
        X_tr,
        y_tr,
        X_te,
        y_te,
    ) = _initialise_variables_nouveau_modele(LIEN1, LIEN2)

    mlp = Pipeline(
        [
            ("features", data_tr),
            ("imputation", KNNImputer()),
            ("entrainement", MLPRegressor()),
        ]
    )
    cv_mlp = GridSearchCV(
        estimator=mlp,
        param_grid={
            "imputation__n_neighbors": range(4, 16, 4),
            "entrainement__hidden_layer_sizes": [(50,), (100,), (50, 50), (75, 75)],
            "entrainement__max_iter": [500, 750, 1000],
            "entrainement__solver": ["adam"],
        },
    )
    cv_mlp.fit(X_tr, y_tr)
    indice_meilleur = cv_mlp.cv_results_["rank_test_score"].argmin()
    meilleurs_parametres = cv_mlp.cv_results_["params"][indice_meilleur]
    meilleurs_parametres["score_entrainement"] = round(cv_mlp.score(X_tr, y_tr), 2)
    meilleurs_parametres["score_test"] = round(cv_mlp.score(X_te, y_te), 2)
    df_mlp = pd.DataFrame(
        list(meilleurs_parametres.items()), columns=["Paramètre", "Valeur"]
    )
    return df_mlp, cv_mlp


def _boosting(LIEN1: str, LIEN2: str) -> tuple:
    (
        df,
        data,
        data_tr,
        X,
        y,
        X_tr,
        y_tr,
        X_te,
        y_te,
    ) = _initialise_variables_nouveau_modele(LIEN1, LIEN2)

    gbr = Pipeline(
        [
            ("features", data_tr),
            ("imputation", KNNImputer()),
            ("entrainement", GradientBoostingRegressor()),
        ]
    )
    cv_gbr = GridSearchCV(
        estimator=gbr,
        param_grid={
            "imputation__n_neighbors": range(4, 16, 4),
            "entrainement__learning_rate": (0.005, 0.01, 0.1, 0.5, 1),
            "entrainement__n_estimators": (25, 50, 100, 200),
        },
    )
    cv_gbr.fit(X_tr, y_tr)
    indice_meilleur = cv_gbr.cv_results_["rank_test_score"].argmin()
    meilleurs_parametres = cv_gbr.cv_results_["params"][indice_meilleur]
    meilleurs_parametres["score_entrainement"] = round(cv_gbr.score(X_tr, y_tr), 2)
    meilleurs_parametres["score_test"] = round(cv_gbr.score(X_te, y_te), 2)
    df_gbr = pd.DataFrame(
        list(meilleurs_parametres.items()), columns=["Paramètre", "Valeur"]
    )
    return df_gbr, cv_gbr
