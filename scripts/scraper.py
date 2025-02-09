import os
import requests
import json
import re
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# Initialisation des stopwords en anglais
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

# Définition des chemins pour stocker les articles
DATA_DIR = "./data"
DATA_FILE = os.path.join(DATA_DIR, "bbc_articles.json")

# Vérifier si le dossier "data" existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# En-têtes pour éviter les blocages
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

# Scraper les articles récents depuis BBC News
def get_latest_articles():
    url = "https://www.bbc.com/news"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_links = soup.find_all('a', href=True)

        articles_links = [
            "https://www.bbc.com" + link.get('href')
            for link in all_links if "/news/" in link.get('href') and not link.get('href').startswith("https")
        ]

        return list(set(articles_links))  # Éviter les doublons
    else:
        return []

# Extraire et nettoyer le texte des articles
def get_article_content(article_url):
    response = requests.get(article_url, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        article_body = soup.find('article')
        paragraphs = article_body.find_all('p') if article_body else soup.find_all('p')

        clean_text = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        return clean_text if clean_text else "Aucun texte pertinent trouvé."
    
    return "Impossible de récupérer l'article."

# Fonction de nettoyage du texte
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)  
    text = text.translate(str.maketrans("", "", string.punctuation))  
    text = " ".join([word for word in text.split() if word not in STOPWORDS])  
    return text

# Sauvegarde des articles en JSON
def save_articles(articles_dict):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(articles_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")

# Charger les articles depuis le fichier JSON
def load_articles():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

# Exécuter le scraping et enregistrer les articles
if __name__ == "__main__":
    articles_links = get_latest_articles()

    articles_dict = {}
    
    for i, url in enumerate(articles_links):
        content = get_article_content(url)
        cleaned_content = clean_text(content)
        articles_dict[i] = {"url": url, "content": cleaned_content}

    save_articles(articles_dict)
