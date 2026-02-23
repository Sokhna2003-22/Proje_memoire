from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# ==============================
# CONFIGURATION
# ==============================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)

data = []
page = 1

# ==============================
# SCRAPING AUTOMATIQUE
# ==============================

while True:

    print(f"\n Scraping page {page}")
    driver.get(f"https://www.expat-dakar.com/immobilier?page={page}")
    time.sleep(20)

    annonces = driver.find_elements(By.XPATH, "//a[contains(@href, '/annonce/')]")

    if not annonces:
        print(" Plus d'annonces. Fin du scraping.")
        break

    annonce_links = []

    for a in annonces:
        link = a.get_attribute("href")
        if link and link not in annonce_links:
            annonce_links.append(link)

    print(f"➡ {len(annonce_links)} annonces trouvées")

    # ==============================
    # SCRAPER CHAQUE ANNONCE
    # ==============================

    for link in annonce_links:

        driver.get(link)

        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        except:
            continue

        # ----- Titre -----
        try:
            titre = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            titre = ""

        # ----- Prix -----
        try:
            prix = driver.find_element(By.XPATH, "//*[contains(text(),'Cfa')]").text.strip()
        except:
            prix = ""

        # ----- Localisation -----
        try:
            localisation = driver.find_element(By.XPATH, "//span[contains(text(),'Dakar')]").text.strip()
        except:
            localisation = ""

        # ----- Description -----
        try:
            description = driver.find_element(
                By.XPATH,
                "//div[contains(@class,'description')]"
            ).text.strip()
        except:
            description = ""

        # ----- Détails -----
        chambres = ""
        salle_bain = ""
        surface = ""

        try:
            details = driver.find_elements(By.XPATH, "//li")

            for d in details:
                text = d.text.lower()

                if "chambre" in text:
                    chambres = d.text

                elif "salle" in text and "bain" in text:
                    salle_bain = d.text

                elif "m²" in text or "m2" in text:
                    surface = d.text

        except:
            pass

        data.append({
            "Titre": titre,
            "Prix": prix,
            "Localisation": localisation,
            "Chambres": chambres,
            "Salle de bain": salle_bain,
            "Surface (m²)": surface,
            "Description": description
        })

        print("✔", titre)
        time.sleep(1.5)

    page += 1

# ==============================
# EXPORT CSV
# ==============================

driver.quit()

df = pd.DataFrame(data)
df.to_csv("expat_dakar_immobilier_total.csv", index=False, encoding="utf-8-sig")

print(f"\n Scraping terminé : {len(df)} annonces récupérées.")