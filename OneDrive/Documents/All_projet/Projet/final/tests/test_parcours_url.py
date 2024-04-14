from final.parcours_url import (
    _fichier_texte_en_liste,
    _driver_option,
    _recupere_prix,
    _recupere_kilometrage,
    _recupere_annee,
    _recupere_puissance,
    _recupere_transmission,
    _recupere_cylindree,
    _recupere_vitesse,
    _recupere_poids_vide,
    _recupere_carrosserie,
    _recupere_etat,
    _recupere_type_moteur,
    _recupere_siege,
    _recupere_porte,
    _recupere_carburant,
    _recupere_classe_emission,
    _recupere_confort,
    _recupere_divertissement,
    _recupere_securite,
    _recupere_autre,
    _recupere_marque,
    _recupere_modele,
    _attente_lien,
    _ajoute_ligne,
    _parcours_liens,
)
import pytest


def test_fichier_texte_en_liste():
    entree = "LIENS_ANNONCES_VOITURES_V2.txt"
    attendu = [
        "https://www.autoscout24.fr/offres/porsche-cayenne-coupe-4-0-v8-680-ch-tiptronic-bva-turbo-s-e-hybrid-autres-gris-72c2fc62-de51-4817-ae89-176ec075066d",
        "https://www.autoscout24.fr/offres/bmw-420-420ia-184ch-m-sport-essence-e9e9ac9a-03db-4f5a-9fcc-604c950bd3c7",
    ]
    assert _fichier_texte_en_liste(entree)[0:2] == attendu


@pytest.mark.selenium
def test_driver_option():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    assert (
        "Porsche Cayenne SUV/4x4/Pick-Up en Gris occasion à LYON pour € 184\u202f900,-"
        == driver.title
    )
    driver.quit()


def test_recupere_prix_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_prix(driver, t)
    assert prix == "€ 184\u202f900"
    driver.quit()


def test_recupere_prix_avec_element_non_valide():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_prix(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_kilometrage_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_kilometrage(driver, t)
    assert prix == "17\u202f500 km"
    driver.quit()


def test_recupere_kilometrage_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_kilometrage(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_annee_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_annee(driver, t)
    assert prix == "09/2022"
    driver.quit()


def test_recupere_annee_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_annee(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_puissance_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_puissance(driver, t)
    assert prix == "500 kW (680 CH)"
    driver.quit()


def test_recupere_puissance_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_puissance(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_transmission_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_transmission(driver, t)
    assert prix == "Boîte automatique"
    driver.quit()


def test_recupere_transmission_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_transmission(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_cylindree_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_cylindree(driver, t)
    assert prix == "3\u202f996 cm³"
    driver.quit()


def test_recupere_cylindree_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_cylindree(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_vitesse_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_vitesse(driver, t)
    assert prix == "8"
    driver.quit()


def test_recupere_vitesse_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_vitesse(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_poids_vide_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_poids_vide(driver, t)
    assert prix == "2\u202f535 kg"
    driver.quit()


def test_recupere_poids_vide_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_poids_vide(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_carosserie_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_carrosserie(driver, t)
    assert prix == "SUV/4x4/Pick-Up"
    driver.quit()


def test_recupere_carosserie_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_carrosserie(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_etat_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_etat(driver, t)
    assert prix == "Occasion"
    driver.quit()


def test_recupere_etat_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_etat(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_type_moteur_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[5]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_type_moteur(driver, t)
    assert prix == "4x4"
    driver.quit()


def test_recupere_type_moteur_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_type_moteur(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_siege_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_siege(driver, t)
    assert prix == "5"
    driver.quit()


def test_recupere_siege_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_siege(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_porte_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_porte(driver, t)
    assert prix == "5"
    driver.quit()


def test_recupere_porte_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_porte(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_carburant_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_carburant(driver, t)
    assert prix == "Super Plus E10 98"
    driver.quit()


def test_recupere_carburant_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_carburant(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_classe_emission_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_classe_emission(driver, t)
    assert prix == "Super Plus E10 98"
    driver.quit()


def test_recupere_classe_emission_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_classe_emission(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_confort_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    prix = _recupere_confort(driver)
    assert prix == 15
    driver.quit()


def test_recupere_confort_avec_element_non_valide():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    prix = _recupere_confort(driver)
    assert prix == "NA"
    driver.quit()


def test_recupere_divertissement_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    prix = _recupere_divertissement(driver)
    assert prix == 1
    driver.quit()


def test_recupere_divertissement_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    prix = _recupere_divertissement(driver)
    assert prix == "NA"
    driver.quit()


def test_recupere_securite_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    prix = _recupere_securite(driver)
    assert prix == 9
    driver.quit()


def test_recupere_securite_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    prix = _recupere_securite(driver)
    assert prix == "NA"
    driver.quit()


def test_recupere_autre_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    prix = _recupere_autre(driver)
    assert prix == 3
    driver.quit()


def test_recupere_autre_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    prix = _recupere_autre(driver)
    assert prix == "NA"
    driver.quit()


def test_recupere_marque_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_marque(driver, t)
    assert prix == "Porsche"
    driver.quit()


def test_recupere_marque_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_marque(driver, t)
    assert prix == "NA"
    driver.quit()


def test_recupere_modele_avec_element_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    prix = _recupere_modele(driver, t)
    assert prix == "Cayenne"
    driver.quit()


def test_recupere_modele_avec_element_non_valdie():
    driver = _driver_option()
    driver.get("https://www.autoscout24.fr/")
    t = 0
    prix = _recupere_modele(driver, t)
    assert prix == "NA"
    driver.quit()


def test_attente_lien_valide():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    URL_COURANT = entree
    URL_DESTINATION = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[1]
    _attente_lien(driver, URL_COURANT, URL_DESTINATION, temps_max_execution=2)


def test_ajoute_ligne():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    data = []
    _ajoute_ligne(entree, driver, t, data)
    assert data == [
        [
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
    ]


def test_parcours_liens():
    entree = _fichier_texte_en_liste("LIENS_ANNONCES_VOITURES_V2.txt")[0]
    driver = _driver_option()
    driver.get(entree)
    t = 10
    data = []
    data = _parcours_liens([entree], t, data)
    assert data == [
        [
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
    ]
