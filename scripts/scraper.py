import os
import requests
import json
import re
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# 📌 Initialisation des stopwords en anglais
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

# 📂 Définition des chemins pour stocker les articles
DATA_DIR = "./data"
DATA_FILE = os.path.join(DATA_DIR, "bbc_articles.json")

# ✅ Vérifier si le dossier "data" existe, sinon le créer
if not os.path.exists(DATA_DIR):
    print(f"📂 Création du dossier {DATA_DIR}...")
    os.makedirs(DATA_DIR)

# 🌍 En-têtes pour éviter les blocages
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

# 🔍 Scraper les articles récents depuis BBC News
def get_latest_articles():
    url = "https://www.bbc.com/news"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_links = soup.find_all('a', href=True)

        # Filtrer uniquement les liens des articles
        articles_links = [
            "https://www.bbc.com" + link.get('href')
            for link in all_links if "/news/" in link.get('href') and not link.get('href').startswith("https")
        ]

        return list(set(articles_links))  # Éviter les doublons
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        return []

# ✨ Extraire et nettoyer le texte des articles
def get_article_content(article_url):
    response = requests.get(article_url, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Chercher la section principale de l'article
        article_body = soup.find('article')
        paragraphs = article_body.find_all('p') if article_body else soup.find_all('p')

        clean_text = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        return clean_text if clean_text else "Aucun texte pertinent trouvé."
    
    return "Impossible de récupérer l'article."

# 🧼 Fonction de nettoyage du texte
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)  # Supprime les espaces inutiles
    text = text.translate(str.maketrans("", "", string.punctuation))  # Supprime la ponctuation
    text = " ".join([word for word in text.split() if word not in STOPWORDS])  # Supprime les stopwords
    return text

# 💾 Sauvegarde des articles en JSON
def save_articles(articles_dict):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(articles_dict, f, ensure_ascii=False, indent=4)
        print(f"✅ Données enregistrées dans {DATA_FILE}")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement des données : {e}")

# 🔄 Charger les articles depuis le fichier JSON
def load_articles():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                articles = json.load(f)
                print(f"📂 {len(articles)} articles chargés depuis {DATA_FILE}")
                return articles
        except json.JSONDecodeError:
            print(f"⚠️ Erreur : Fichier JSON corrompu, recréation de {DATA_FILE}.")
            return {}
    return {}

# 🚀 Exécuter le scraping et enregistrer les articles
if __name__ == "__main__":
    print("🔍 Scraping des articles en cours...")
    articles_links = get_latest_articles()
    print(f"\n📢 {len(articles_links)} articles trouvés.")

    articles_dict = {}
    
    for i, url in enumerate(articles_links):
        content = get_article_content(url)
        cleaned_content = clean_text(content)
        articles_dict[i] = {"url": url, "content": cleaned_content}

    # 💾 Sauvegarde des articles
    save_articles(articles_dict)
    print("\n✅ Tous les articles sont enregistrés avec succès !")
