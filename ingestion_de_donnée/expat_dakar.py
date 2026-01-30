from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

data = []
page = 1

while True:
    url = f"https://www.expat-dakar.com/immobilier?page={page}"
    print(f"Scraping page {page} → {url}")

    driver.get(url)
    time.sleep(20)  # Cloudflare + chargement

    listings = driver.find_elements(By.CLASS_NAME, "listing-card")

    #Stop si plus d'annonces
    if len(listings) == 0:
        print("Plus aucune annonce trouvée, arrêt.")
        break

    for listing in listings:
        try:
            title = listing.find_element(
                By.CLASS_NAME, "listing-card__header__title"
            ).text
        except:
            title = None

        try:
            bedrooms = listing.find_element(
                By.CSS_SELECTOR, "span[class*='no-of-bedrooms']"
            ).text
        except:
            bedrooms = None

        try:
            surface = listing.find_element(
                By.CSS_SELECTOR, "span[class*='square-metres']"
            ).text
        except:
            surface = None

        try:
            location = listing.find_element(
                By.CLASS_NAME, "listing-card__header__location"
            ).text
        except:
            location = None

        try:
            price = listing.find_element(
                By.CLASS_NAME, "listing-card__price__value"
            ).text
        except:
            price = None

        data.append({
            "Titre": title,
            "Chambres": bedrooms,
            "Surface": surface,
            "Localisation": location,
            "Prix": price
        })

    page += 1

driver.quit()

df = pd.DataFrame(data)
df.to_csv("expat_dakar_immobilier_complet.csv", index=False, encoding="utf-8")

print(f"Scraping terminé : {len(df)} annonces récupérées")
