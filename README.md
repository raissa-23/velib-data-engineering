# Vélib Data Engineering - Influence de la météo sur le parc de Vélib à Paris

## Objectif
Collecter et analyser les données du Vélib et de la météo à Paris pour comprendre comment la météo influence l'utilisation des vélos.

## Architecture
- **Bronze** : Données brutes des APIs (Open Data Paris + Open Meteo)
- **Silver** : Données nettoyées et transformées
- **Gold** : Données agrégées pour l'analyse

## Stack Technique
- Python 3.10
- PostgreSQL
- Docker & Docker Compose
- Pandas, Requests

## Installation
```bash
docker-compose up

## Structure du Projet
.
├── src/                    # Code Python
├── data/                   # Données (raw, processed)
├── docker/                 # Fichiers Docker
├── requirements.txt        # Dépendances Python
└── README.md
