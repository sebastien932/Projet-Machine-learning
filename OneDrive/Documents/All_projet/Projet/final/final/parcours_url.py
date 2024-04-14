""" Parcours les liens pour récupérer les 

        informations sur les voitures """

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
import logging


def _fichier_texte_en_liste(chemin_fichier: str) -> list:
    """Transforme chemin_fichier en liste"""
    with open(chemin_fichier, "r", encoding="utf-8") as fichier:
        LIENS_ANNONCES_VOITURES_V2 = fichier.readlines()
    for i in range(0, len(LIENS_ANNONCES_VOITURES_V2)):
        LIENS_ANNONCES_VOITURES_V2[i] = LIENS_ANNONCES_VOITURES_V2[i].replace("\n", "")
    return LIENS_ANNONCES_VOITURES_V2


def _driver_option():
    chrome_options = Options()
    LOGGER = logging.getLogger("selenium")
    LOGGER.setLevel(logging.WARNING)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--accept-cookies")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-logging")
    LOGGER = logging.getLogger("selenium")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def _recupere_prix(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le prix d'une voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    prix = None
    try:
        price_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "PriceInfo_price__XU0aF"))
        )
    except TimeoutException:
        prix = "NA"
    if prix != "NA":
        price = price_element.text
        prix = price.replace(",", "").replace("-", "")
    return prix


def _recupere_kilometrage(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le kilométrage d'une voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    kilometrage = None
    try:
        kilometrage_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Kilométrage"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        kilometrage = "NA"
    if kilometrage != "NA":
        kilometrage = kilometrage_element.text.strip()
    return kilometrage


def _recupere_annee(driver: ChromeWebDriver, t: int) -> str:
    """Récupère l'année de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    annee = None
    try:
        annee_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Année"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        annee = "NA"
    if annee != "NA":
        annee = annee_element.text.strip()
    return annee


def _recupere_puissance(driver: ChromeWebDriver, t: int) -> str:
    """Récupère l'année de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    puissance = None
    try:
        puissance_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Puissance kW (CH)"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        puissance = "NA"
    if puissance != "NA":
        puissance = puissance_element.text.strip()
    return puissance


def _recupere_transmission(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le type de transmission de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    transmission = None
    try:
        transmission_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Transmission"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        transmission = "NA"
    if transmission != "NA":
        transmission = transmission_element.text.strip()
    return transmission


def _recupere_cylindree(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le cylindré de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    cylindree = None
    try:
        cylindree_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Cylindrée"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        cylindree = "NA"
    if cylindree != "NA":
        cylindree = cylindree_element.text.strip()
    return cylindree


def _recupere_vitesse(driver: ChromeWebDriver, t: int) -> str:
    """Récupère la vitesse de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    vitesse = None
    try:
        vitesses_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Vitesses"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        vitesse = "NA"
    if vitesse != "NA":
        vitesse = vitesses_element.text.strip()
    return vitesse


def _recupere_poids_vide(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le pids à vide de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    poids_vide = None
    try:
        poids_vide_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Poids à vide"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        poids_vide = "NA"
    if poids_vide != "NA":
        poids_vide = poids_vide_element.text.strip()
    return poids_vide


def _recupere_carrosserie(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le type de carrosserie de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    carrosserie = None
    try:
        carrosserie_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Carrosserie"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        carrosserie = "NA"
    if carrosserie != "NA":
        carrosserie = carrosserie_element.text.strip()
    return carrosserie


def _recupere_etat(driver: ChromeWebDriver, t: int) -> str:
    """Récupère l' etat  de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    etat = None
    try:
        etat_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="État"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        etat = "NA"
    if etat != "NA":
        etat = etat_element.text.strip()
    return etat


def _recupere_type_moteur(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le type de moteur de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    type_moteur = None
    try:
        type_moteur_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Type de moteur"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        type_moteur = "NA"
    if type_moteur != "NA":
        type_moteur = type_moteur_element.text.strip()
    return type_moteur


def _recupere_siege(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le nombre de siège de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    siege = None
    try:
        sieges_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Sièges"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        siege = "NA"
    if siege != "NA":
        siege = sieges_element.text.strip()
    return siege


def _recupere_porte(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le nombre de porte de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    portes = None
    try:
        portes_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Portes"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        portes = "NA"
    if portes != "NA":
        portes = portes_element.text.strip()
    return portes


def _recupere_carburant(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le type de carburant de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    carburant = None
    try:
        carburant_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Carburant"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        carburant = "NA"
    if carburant != "NA":
        carburant = carburant_element.text.strip()
    return carburant


def _recupere_classe_emission(driver: ChromeWebDriver, t: int) -> str:
    """Récupère la classe d'emission de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    classe_emission = None
    try:
        classe_emission_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//dt[text()="Carburant"]/following-sibling::dd')
            )
        )
    except TimeoutException:
        classe_emission = "NA"
    if classe_emission != "NA":
        classe_emission = classe_emission_element.text.strip()
    return classe_emission


def _recupere_confort(driver: WebDriver) -> Union[int, str]:
    """Récupère le nombre d'instrument de confort de la voiture à l'aide de selenium"""
    nombre_elements_confort: WebElement
    confort_li_elements: list[WebElement]
    confort: Union[str, int, None]
    confort = None
    try:
        nombre_elements_confort = driver.find_element(
            By.XPATH, '//dd[@class="DataGrid_defaultDdStyle__3IYpG"]'
        )
    except NoSuchElementException:
        confort = "NA"
    if confort is None:
        confort_li_elements = nombre_elements_confort.find_elements(By.TAG_NAME, "li")
        confort = len(confort_li_elements)
    return confort


def _recupere_divertissement(driver: WebDriver) -> Union[int, str]:
    """Récupère le nombre d'instrument de divertissement de la voiture à l'aide de selenium"""
    divertissement_elements: WebElement
    divertissement_li_elements: list[WebElement]
    nb_divertissement: Union[str, int, None]
    nb_divertissement = None
    try:
        divertissement_elements = driver.find_element(
            By.XPATH, '//dt[text()="Divertissement / Médias"]/following-sibling::dd/ul'
        )
    except NoSuchElementException:
        nb_divertissement = "NA"
    if nb_divertissement is None:
        divertissement_li_elements = divertissement_elements.find_elements(
            By.TAG_NAME, "li"
        )
        nb_divertissement = len(divertissement_li_elements)
    return nb_divertissement


def _recupere_securite(driver: WebDriver) -> Union[int, str]:
    """Récupère le nombre d'instrument de sécurité de la voiture à l'aide de selenium"""
    sécurité_elements: WebElement
    sécurité_li_elements: list[WebElement]
    nb_sécurité: Union[str, int, None]
    nb_sécurité = None
    try:
        sécurité_elements = driver.find_element(
            By.XPATH, '//dt[text()="Sécurité"]/following-sibling::dd/ul'
        )
    except NoSuchElementException:
        nb_sécurité = "NA"
    if nb_sécurité is None:
        sécurité_li_elements = sécurité_elements.find_elements(By.TAG_NAME, "li")
        nb_sécurité = len(sécurité_li_elements)
    return nb_sécurité


def _recupere_autre(driver: WebDriver) -> Union[int, str]:
    """Récupère le nombre d'instrument autre de la voiture à l'aide de selenium"""
    Autre_elements: WebElement
    Autre_li_elements: list[WebElement]
    nb_autre: Union[str, int, None]
    nb_autre = None
    try:
        Autre_elements = driver.find_element(
            By.XPATH, '//dt[text()="Autres"]/following-sibling::dd/ul'
        )
    except NoSuchElementException:
        nb_autre = "NA"
    if nb_autre is None:
        Autre_li_elements = Autre_elements.find_elements(By.TAG_NAME, "li")
        nb_autre = len(Autre_li_elements)
    return nb_autre


def _recupere_marque(driver: ChromeWebDriver, t: int) -> str:
    """Récupère la marque de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    marque = None
    try:
        Marque_element = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l")
            )
        )
    except TimeoutException:
        marque = "NA"
    if marque != "NA":
        marque = Marque_element.text.strip()
    return marque


def _recupere_modele(driver: ChromeWebDriver, t: int) -> str:
    """Récupère le modèle de la voiture à l'aide de selenium"""
    wait = WebDriverWait(driver, t)
    modele = None
    try:
        Modèle_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "StageTitle_model__EbfjC"))
        )
    except TimeoutException:
        modele = "NA"
    if modele != "NA":
        modele = Modèle_element.text.strip()
    return modele


def _attente_lien(
    driver: WebDriver, URL_COURANT: str, URL_DESTINATION: str, temps_max_execution=20
):
    temps_debut = time.time()
    if URL_COURANT != URL_DESTINATION:
        while (
            URL_COURANT != URL_DESTINATION
            and (time.time() - temps_debut) < temps_max_execution
        ):
            time.sleep(1)
            URL_COURANT = driver.current_url


def _ajoute_ligne(
    LIEN: str, driver: ChromeWebDriver, t: int, data: list
) -> list[list[Union[str, int]]]:
    """
    Ajoute une nouvelle ligne de données à la liste existante."""
    data.append(
        [
            LIEN,
            _recupere_prix(driver, t),
            _recupere_kilometrage(driver, t),
            _recupere_annee(driver, t),
            _recupere_puissance(driver, t),
            _recupere_transmission(driver, t),
            _recupere_cylindree(driver, t),
            _recupere_vitesse(driver, t),
            _recupere_poids_vide(driver, t),
            _recupere_carrosserie(driver, t),
            _recupere_etat(driver, t),
            _recupere_type_moteur(driver, t),
            _recupere_siege(driver, t),
            _recupere_porte(driver, t),
            _recupere_carburant(driver, t),
            _recupere_classe_emission(driver, t),
            _recupere_confort(driver),
            _recupere_divertissement(driver),
            _recupere_securite(driver),
            _recupere_autre(driver),
            _recupere_marque(driver, t),
            _recupere_modele(driver, t),
        ]
    )
    return data


def _parcours_liens(
    LIENS: list[str], t: int, data: list
) -> list[list[Union[str, int]]]:
    """
    Parcourt une liste de liens, récupère les données et les stocke dans une liste.
    """
    driver = _driver_option()
    temps_tout_debut = time.time()
    for LIEN in LIENS:
        temps_debut = time.time()
        driver.get(LIEN)
        URL_DESTINATION = LIEN
        URL_COURANT = driver.current_url
        _attente_lien(driver, URL_COURANT, URL_DESTINATION)
        if URL_COURANT == URL_DESTINATION:
            if _recupere_prix(driver, t) != "NA":
                data = _ajoute_ligne(LIEN, driver, t, data)

                temps_ecoule = time.time() - temps_debut
                if temps_ecoule > 4:
                    driver.quit()
                    driver = _driver_option()
                    driver.get(LIEN)
                temps_total = round(time.time() - temps_tout_debut, 2)
                print(
                    f"{LIENS.index(LIEN) +1} sur {len(LIENS)} en {temps_total} secondes et temps du lien : {round(temps_ecoule,2)} secondes"
                )
    driver.quit()
    return data
