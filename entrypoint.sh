#!/bin/bash

# Exécuter le scraping pour récupérer les articles
echo "Lancement du scraper..."
python scripts/scraper.py

# Exécuter l'extraction des résumés
echo "Lancement de l'extraction des résumés..."
python scripts/summarizer_bart.py

# Exécuter l'extraction des mots-clés
echo "Lancement de l'extraction des mots-clés..."
python scripts/keyword_extractor.py

# Lancer l'API FastAPI en arrière-plan
echo "Démarrage de l'API FastAPI..."
uvicorn scripts.api:app --host 0.0.0.0 --port 8000 --reload &

# Lancer Streamlit
echo "Démarrage de l'interface Streamlit..."
streamlit run scripts/app.py --server.port=8501 --server.address=0.0.0.0
