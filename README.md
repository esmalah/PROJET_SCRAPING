# **Plateforme de Scraping et Analyse d'Articles BBC News**

## Introduction

Ce projet met en place une plateforme de scraping et d'analyse de texte pour les articles de BBC News. L'objectif est d'automatiser la collecte d'articles, d'en générer des résumés et d'extraire des mots-clés pour une meilleure compréhension du contenu médiatique.

## Objectifs

- Scraper automatiquement les articles de BBC News.
- Générer des résumés concis des articles.
- Extraire les mots-clés pertinents.
- Exposer une API REST pour récupérer les articles et analyses.
- Offrir une interface utilisateur interactive pour visualiser les résultats.

## Sources de Données

- **BBC News** : Extraction des articles via le web scraping.
- **Données Stockées** :
  - `data/bbc_articles.json` : Articles collectés et nettoyés.
  - `data/summaries.json` : Résumés des articles générés avec BART.
  - `data/keywords.json` : Mots-clés extraits avec KeyBERT.

## Technologies Utilisées

- **Python 3.10** : Langage principal du projet.
- **BeautifulSoup4** : Scraping des articles.
- **BART (facebook/bart-large-cnn)** : Génération automatique des résumés.
- **KeyBERT** : Extraction des mots-clés.
- **FastAPI** : API REST pour accéder aux données.
- **Streamlit** : Interface utilisateur pour la visualisation.
- **Docker** : Conteneurisation pour une exécution simplifiée.

## Installation et Exécution

### Cloner le projet
```bash
git clone https://github.com/esmalah/PROJET_SCRAPING.git
cd PROJET_SCRAPING
  ```

### Construire et exécuter le conteneur Docker
```bash
docker build -t bbc_scraper .
docker run -p 8000:8000 -p 8501:8501 -v $(pwd)/data:/app/data bbc_scraper
  ```
