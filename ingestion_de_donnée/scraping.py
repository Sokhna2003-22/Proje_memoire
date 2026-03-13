import pandas as pd
import time
import random
import re
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================
# CONFIGURATION ET REPRISE
# ==============================

CSV_FILE = "dataset_immobilier_expat.csv"
MAX_PAGES = 400
BASE_URL = "https://www.expat-dakar.com/immobilier"

# Déterminer la page de départ
def get_start_page():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # On estime la page en fonction du nombre d'annonces (env. 20 par page)
        # Mais pour être précis, on va te laisser la modifier manuellement si besoin
        # Ici, tu t'es arrêté à 154, donc on met 154 par défaut si le fichier existe
        return 154 
    return 1

START_PAGE = get_start_page()

def create_driver():
    print(" Initialisation du navigateur...")
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Boucle de tentative de création (si internet coupe)
    while True:
        try:
            driver = uc.Chrome(options=options, version_main=141)
            return driver
        except Exception as e:
            print(f" Erreur de connexion/driver : {e}. Nouvel essai dans 30s...")
            time.sleep(30)

def extract_number(text):
    if not text: return None
    nums = re.findall(r'\d+', text.replace("\u202f", "").replace(" ", ""))
    return int("".join(nums)) if nums else None

# ==============================
# LANCEMENT DU SCRAPING
# ==============================

driver = create_driver()
wait = WebDriverWait(driver, 30)
data = []

# Charger les données existantes pour ne pas les perdre
if os.path.exists(CSV_FILE):
    data = pd.read_csv(CSV_FILE).to_dict('records')

try:
    for page in range(START_PAGE, MAX_PAGES + 1):
        
        # Redémarrage cyclique
        if page > START_PAGE and page % 10 == 0:
            print("\n Nettoyage mémoire...")
            if driver: driver.quit()
            time.sleep(10)
            driver = create_driver()
            wait = WebDriverWait(driver, 30)

        print(f"\n---  Page {page}/{MAX_PAGES} (Total collecté: {len(data)}) ---")
        
        try:
            driver.get(f"{BASE_URL}?page={page}")
            time.sleep(random.uniform(15, 20)) 

            elements = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(@href, '/annonce/')]")
            ))
            links = list(set([el.get_attribute("href") for el in elements if el.get_attribute("href")]))

            for index, link in enumerate(links):
                try:
                    driver.get(link)
                    time.sleep(random.uniform(6, 10))

                    titre = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
                    
                    try:
                        p_text = driver.find_element(By.XPATH, "//span[contains(@class, 'price')]").text
                        prix = extract_number(p_text)
                    except: prix = None

                    try:
                        loc = driver.find_element(By.XPATH, "//*[contains(@class, 'address')]").text
                    except: loc = "Dakar"

                    try:
                        desc = driver.find_element(By.XPATH, "//div[contains(@class, 'listing-item__description')]").text
                    except: desc = "Pas de description"

                    full_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                    chambres = re.search(r'(\d+)\s*chambre', full_text)
                    douches = re.search(r'(\d+)\s*salle', full_text)
                    surface = re.search(r'(\d+)\s*m²', full_text)

                    data.append({
                        "Titre": titre,
                        "Prix_CFA": prix,
                        "Localisation": loc.strip().replace("\n", " "),
                        "Nb_Chambres": int(chambres.group(1)) if chambres else None,
                        "Nb_Salles_Bain": int(douches.group(1)) if douches else None,
                        "Surface_m2": int(surface.group(1)) if surface else None,
                        "Description": desc.strip()
                    })
                    print(f"   [{index + 1}/{len(links)}] ✔ {titre[:20]}", end="\r")

                except Exception:
                    continue
            
            # Sauvegarde à chaque page
            pd.DataFrame(data).drop_duplicates().to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

        except Exception as e:
            print(f"\n Erreur page {page}: {e}")
            if "session" in str(e).lower() or "dns" in str(e).lower():
                if driver: 
                    try: driver.quit()
                    except: pass
                driver = create_driver()
                wait = WebDriverWait(driver, 30)
            continue

finally:
    if driver:
        try: driver.quit()
        except: pass
    print(f"\n✨ Session terminée. Data sauvée dans {CSV_FILE}")