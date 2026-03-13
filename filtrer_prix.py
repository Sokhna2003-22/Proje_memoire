import pandas as pd

# Chemin du fichier CSV
file_path = "/home/sokhna-mbathie-niang/Documents/ODC/Projet_Memoire/Data/propres/annonces_dakar_propres.csv"

# Charger le dataset
data = pd.read_csv(file_path)

# Vérifier si la colonne 'prix' existe
if 'Prix' in data.columns:
    # Filtrer les prix inférieurs à 100000
    filtered_data = data[data['Prix'] < 100000]
    print(filtered_data)
else:
    print("La colonne 'Prix' n'existe pas dans le dataset.")