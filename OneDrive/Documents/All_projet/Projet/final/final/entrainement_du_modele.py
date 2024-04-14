from final.traitement_base_de_donnees import _traite_base_de_donnees
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.impute import KNNImputer  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.preprocessing import StandardScaler, OneHotEncoder  # type: ignore
from sklearn.compose import ColumnTransformer  # type: ignore
from sklearn.ensemble import ExtraTreesRegressor  # type: ignore


def _initialise_variables_entrainement_modele(LIEN: str) -> tuple:
    df, data = _traite_base_de_donnees(LIEN)
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


def _initialise_parametres_modele(LIEN: str) -> tuple:
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
    ) = _initialise_variables_entrainement_modele(LIEN)
    Extra = Pipeline(
        [
            ("features", data_tr),
            ("imputation", KNNImputer(n_neighbors=12)),
            (
                "entrainement",
                ExtraTreesRegressor(
                    n_estimators=20,
                    max_depth=None,
                    min_samples_split=3,
                    min_samples_leaf=1,
                ),
            ),
        ]
    )
    return df, data, data_tr, X, y, X_tr, y_tr, X_te, y_te, Extra
