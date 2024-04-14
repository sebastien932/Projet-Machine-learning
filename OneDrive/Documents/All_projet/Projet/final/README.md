# Projet de Machine Learning : Trouver la bonne voiture d'occasion

## Introduction

Bienvenue dans notre projet de machine learning. L'objectif principal est d'aider les utilisateurs à trouver la meilleure annonce de voiture d'occasion en fonction de leurs critères tout en réalisant une bonne affaire financière.
Pour ce faire, le projet se décline en plusieurs axes, le scrapping des données sur le site [AutoScout24](https://www.autoscout24.fr), le traitement de la base de données, l'entrainement d'un modèle de Machine Learning, la notation de l'annonce et enfin l'application permettant aux utilisateurs d'obtenir les annonces des voitures ayant obtenues les meilleures notes en fonction de leurs critères.
Si vous voulez passez **directement à l'application** de la librairie veuillez cliquez **[ici](#application)**

## Description du projet

### Webscraping avec `Selenium`

Pour constituer notre base de données, nous avons utilisé Selenium pour extraire les liens des annonces de voitures  sur le site AutoScout24 pour des raisons de facilités d'accès au site. Cette approche nous a permis d'obtenir un ensemble de données exhaustif pour notre modèle de prédiction.
Néanmoins, il est important de noter qu'il serait intéressant d'ajouter d'autres sites afin d'améliorer notre base de données et donc notre modèle de prédiction

Le processus de webscraping pour collecter les données des annonces de voitures s'est décomposé en quatre étapes distinctes, chacune jouant un rôle clé dans l'obtention d'un ensemble de données complet et informatif.

#### 1. Nombre de Marques

La première étape consistait à récupérer le nombre total d'offres de voitures par marques disponible sur le site [AutoScout24](https://www.autoscout24.fr). Les offres affichés étant limités à 400, il fallait trouver des filtres permettant de récupérer le plus d'annonces possibile. C'est pouquoi nous avons choisis de filtrer sur les marques puis les modèles, afin d'optimiser le temps d'exécution du code.

#### 2. Nombre de Modèles

Une fois le nombre d'annonce par marque obtenu, il a fallu le faire pour les modèles, cette fois-ci, si le nombre d'offre de la marque était inférieur à 400, alors le programme n'avait pas besoin de filtrer sur les modèles.
Ensuite, nous avons identifié le nombre de modèles associés à chaque marque.

#### 3. Extraction des Liens des Pages

La troisième partie du processus était dédiée à l'extraction des liens menant aux pages individuelles des annonces. Connaissant le nombre d'offre par marques et par modele, cela a permis au programme de ne pas à filtrer toutes les marques et tous les modèles, faisant gagner ainsi un gain de temps considérable.

#### 4. Extraction des Descriptifs des Liens

Enfin, nous avons extrait les descriptifs détaillés de chaque annonce en suivant les liens collectés. Cette étape a permis d'obtenir des informations spécifiques sur chaque voiture, telles que le prix, le kilométrage, l'année de fabrication, etc.

L'ensemble de ces étapes a abouti à la constitution d'une base de données robuste, prête à être utilisée dans notre modèle de prédiction des prix de voitures d'occasion.
Néanmoins, il est important de préciser que ce porcessus reste très fastidieux et prend un temps d'écution très long.

### Nettoyage des Données

Après avoir collecté les données, nous avons effectué un nettoyage approfondi en éliminant les valeurs aberrantes et en traitant les valeurs manquantes. La comparaison des performances des modèles avec et sans les données manquantes a été réalisée pour évaluer l'impact sur la qualité des prédictions.

Nous avons également regroupé certains modalités et caractéristiques afin d'éviter des disparités trop importantes dans notre ensemble de données.

Nous avons également choisis de garder uniquement les annonces avec un prix compris entre 1000€ et 100 000€, les annonces avec un prix inférieur à 1000€ était souvent bien noté à tort (notamment dû au fait que certaines voitures pouvait être vendue "pour pièce") et les voitures avec un prix supérieur à 100 000€ avait une différence entre prix et prédit et le prix de l'annonce très important (surement dû au fait du manque d'annonces avec un prix au dessus de 100 000€).

### Modèle de Machine Learning - ExtraTreesRegressor

Afin d'obtenir le prix prédit de chaque annonce, nous avons décidé de faire du machine learning.
La première a été d'utiliser la fonction `OneHotEncoder` afin de créer différentes colonnes pour nos variables  catégorielles en variables binaire et la fonction `StandardScaler` afin de mettre nos colonnes numériques à l'échelle. Dans une seconde étape nous avons diviser notre base de données en deux afin d'obtenir un échantillon d'entraînement et un échantillon de test.
Puis dans une troisème étape, nous avons entraîné plusieurs modèles, notammemnt un `ExtraTreesRegressor`, `GradientBoostingRegressor`, un `RandomForestRegressor` et un `MLPRegressor`, sur lequels nous avons utilisés différents intervalles de valeurs afin d'optimiser les hyper paramètres.
Ayant une base données contenant plusieurs valeurs manquantes, nous avons fait le choix de garder les lignes contenant ces valeurs manquantes et nous avons utilisé la fonction `KNNImputer`, en optimisant également différentes valeurs pour obtenir le meilleur modèle possible.
Enfin, pour assurer la qualité de notre modèle nous avons utilisé la fonction `GridsearchCV` pour effectuer une cross validation en laissant le nombre de plis par défault, c'est à dire à 5.
Voici ci-dessous le code utilis afin d'optimiser les paramètres de l'`ExtraTreesRegressor` :

```python
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


def extra(LIEN1: str, LIEN2: str) -> tuple:
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
    return df_extra,cv_extra
```

Les autres modèles reprennent la logique du code ci-dessus.

Après avoir entraîné plusieurs modèles sur les données d'entraînement, le modèle qui a présenté les meilleures performances dans la prédiction des prix des voitures d'occasion est le `ExtraTreesRegressor` de la librairie.
Nous avons utiliser se modèle pour la prédiction des prix de notre base de données en fixant les paramètre suivants :

- `imputation__n_neighbors` = 12
- `n_estimators` =  20
- `max_depth` = None
- `min_samples_split` = 3
- `min_samples_leaf` = 1

### Méthode de Notation

Pour évaluer la qualité d'une annonce il a fallu prendre une méthode de notation qui est la suivant :

$$
\begin{aligned}
    &\text{Note} = \left(\frac{\phantom{Vr}Ve - Vr}{Ve}\right) \times 10 \\
    &\text{avec}  \quad -\infty < \text{Note} < 10 \\
    &Ve = \text{Valeur estimé (valeur prédite)} \\
    &Vr = \text{Valeur réelle (prix determiné par le vendeur)}
\end{aligned}
$$

#### Interprétation des Résultats

Notre objectif avec cette approche de notation est de fournir aux utilisateurs une évaluation immédiate de la justesse des prix des annonces. En mettant en évidence les divergences entre les valeurs prédites et les estimations du vendeur, nous offrons aux acheteurs une assistance précieuse pour prendre des décisions éclairées lors de l'achat de leur voiture d'occasion.

- Une note proche de **10** : La valeur prédite par notre modèle est largement supérieur à celle estimée par le vendeur, suggérant une très bonne affaire.

- Une note négative : La valeur prédite est inférieure à l'estimation du vendeur, indiquant potentiellement une surévaluation de la voiture.

- Une note proche de **0** : Indique que la valeure prédite et la valeur estimée par le vendeur sont proche.

### Application Interactive

Nous avons développé une application interactive, décliné en trois onglets. Le premier onglet permet aux utilisateurs d'entrer les filtres souhaités pour leurs voitures et renvoie un tableau contenant les carctéristques des voitures triées de la meilleure note à la moins bonne. Les liens des annonces sont cliquables et renvoie directement à la page web de l'annonce.
Le deuxième contient différents graphqiues présentant permettant d'avoir une vue d'ensemble de la base de données et des notes du voitures obtenues et enfin le troisème contient un tableau de statistiques descriptives et un tableau avec les réusltats de test et d'apprentissage du modèle de machine learning (`ExtraTreesRegressor` si vous n'avez pas changé de modèle et le modèle le plus performant si vous souhaitez ré-entrainé les données).

## Utilisation de la librairie {#application}

### enregistre_dataframe

La première commande utilisable de la librairie `final` du script `__main__.py` est la commande `enregistre_dataframe`, qui a partir d'un fichier .txt contenant les liens des annonces va générer un data frame et l'enregistrera également au format .txt.
Pour utiliser cette commande il suffit de taper la ligne de code suivante via votre environnement virtuelle :

```sh
python -m final enregistre_dataframe LIENS_EXEMPLE.txt
```

Vous pouvez également utiliser la commande suivante :

```sh
python -m final enregistre_dataframe LIENS_EXEMPLE.txt t
```

Avec `t` un `int` représentant le nombre de seconde que vous voulez laisser au programme avant de le forcer à passer au lien suivant si il n'a pas réussi à charger l'URL du lien. Par défault t vaut 1 seconde, veillez à **ne pas trop l'augmenter** sinon le temps d'exécution du code pourra être largement plus long.

avec `LIENS_EXEMPLE.txt`, le nom du fichier contenant les liens des annonces.
Cette commande enregistrera alors un nouveau fichier `BASE_DE_DONNEES.txt` contenant les différentes caractéristques des liens.

### entrainement_modele

La seconde commande également utilisable via le script `__main__.py` est la fonction `entrainement_modele`, qui a partir du data frame enregistré au format .txt, va traiter la base de données puis va entraîner un `ExtraTreesRegressor` de la librairie `sklearn`.
Pour utiliser cette commande il suffit de taper la ligne de code suivante via votre environnement virtuelle :

```sh
python -m final entrainement_modele BASE.txt
```

avec `BASE.txt`, le nom du fichier contenant le data frame.
Cette commande enregistrera alors un nouveau fichier `donnees.json` contenant la base de données traitée et entraînée.

Si vous souhaitez ré-entrainer tous modèles sur la même base de données pour vérifier les résultats ou tout simplement pour entraîner un nouveau modèle sur des nouvelles données vous pouvez utiser la commande suivante :

```sh
python -m final entrainement_modele BASE.txt
```

**Attention**, le temps d'éxcution sera conséquent et dépendra énormément de la performance de votre pc.

### lancement_application

Enfin la dernière commande utilisable via le script `__main__.py` est la fonction `lancement_application`, qui a partir du data frame enregistré au format .json va lancer l'application décrite ci-dessus. Pour lancer lancer l'application il suffit de taper la ligne de code suivante :

```sh
python -m final lancement_application
```
