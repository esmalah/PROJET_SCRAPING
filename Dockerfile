# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer les ports de l’API (8000) et de Streamlit (8501)
EXPOSE 8000 8501

# Définir le point d’entrée pour exécuter tout automatiquement
ENTRYPOINT ["bash", "entrypoint.sh"]
