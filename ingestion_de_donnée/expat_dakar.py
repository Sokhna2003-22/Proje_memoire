import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.expat-dakar.com/immobilier"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Statut HTTP :", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

annonces = soup.find_all("div", class_="listing-card")

print("Nombre d'annonces trouvées :", len(annonces))

data = []

for annonce in annonces:
    titre = annonce.find("h2")
    prix = annonce.find("span", class_="price")

    data.append({
        "titre": titre.text.strip() if titre else None,
        "prix": prix.text.strip() if prix else None
    })

df = pd.DataFrame(data)

# 🔍 AFFICHAGE DANS LE TERMINAL
print("\nAperçu des données :")
print(df.head())

print("\nInfos DataFrame :")
print(df.info())

# ✅ Sauvegarde SEULEMENT si le DataFrame n'est pas vide
if not df.empty:
    df.to_csv("Data/brutes/annonces_expat_dakar.csv", index=False)
    print("\n✅ Fichier CSV enregistré avec succès")
else:
    print("\n❌ Aucune donnée trouvée → fichier NON enregistré")
