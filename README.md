# Prédiction des prix immobiliers à Dakar

## Contexte
Le marché immobilier à Dakar connaît une forte variation des prix selon les quartiers,
les caractéristiques des biens et leur localisation.
Il est souvent difficile d’estimer le juste prix d’un bien immobilier.

## Problématique
Comment estimer automatiquement le prix d’un bien immobilier à Dakar
à partir de ses caractéristiques et de sa localisation ?

## Objectif du projet
Développer un modèle de Machine Learning capable de prédire le prix
d’un bien immobilier à Dakar à partir de données réelles collectées en ligne.

## Organisation du projet

- ingestion_donnees : collecte des données par scraping
- traitement_donnees : nettoyage, transformation et enrichissement des données
- stockage : stockage des données dans une base PostgreSQL
- ml : entraînement et prédiction avec des modèles de Machine Learning
- data : fichiers de données (brutes, nettoyées, préparées)
- docker : configuration Docker du projet

## Pipeline de traitement
1. Ingestion des données
2. Nettoyage et traitement
3. Stockage
4. Modélisation Machine Learning
5. Analyse et interprétation des résultats

## Technologies utilisées
- Python
- Docker et Docker Compose
- PostgreSQL
- VS Code
