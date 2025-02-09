import os
import json
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# Chemins des fichiers JSON
DATA_FILE = "./data/bbc_articles_summarized.json"
OUTPUT_FILE = "./data/bbc_articles_keywords.json"

# Charger le modèle d'embedding pour KeyBERT
print("Chargement du modèle KeyBERT...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=embedding_model)
print("Modèle KeyBERT chargé avec succès.")

def load_articles():
    """Charge les articles avec résumés depuis le fichier JSON."""
    if not os.path.exists(DATA_FILE):
        print("Aucun fichier JSON trouvé.")
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_keywords(text, top_n=5):
    """Extrait les mots-clés d'un texte."""
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]

def generate_keywords():
    """Ajoute des mots-clés à chaque article."""
    articles = load_articles()
    if not articles:
        return
    
    print(f"Extraction des mots-clés pour {len(articles)} articles...")

    for i, article in articles.items():
        articles[i]["keywords"] = extract_keywords(article["content"])

    # Sauvegarde des articles avec mots-clés
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Mots-clés extraits et enregistrés dans {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_keywords()
