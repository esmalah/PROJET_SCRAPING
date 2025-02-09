import os
import json
from transformers import pipeline

# Chemins des fichiers
DATA_FILE = "./data/bbc_articles.json"
OUTPUT_FILE = "./data/bbc_articles_summarized.json"

# Charger le modèle BART pour le résumé
print("Chargement du modèle BART pour le résumé...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Modèle BART chargé avec succès.")

def load_articles():
    """Charge les articles depuis le fichier JSON."""
    if not os.path.exists(DATA_FILE):
        print("Aucun fichier JSON trouvé.")
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_text(text):
    """Génère un résumé avec BART."""
    if len(text) > 1024:
        text = text[:1024]  # Limiter la taille pour éviter les erreurs

    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def generate_summaries():
    """Ajoute un résumé à chaque article."""
    articles = load_articles()
    if not articles:
        return
    
    print(f"Génération des résumés pour {len(articles)} articles...")

    for i, article in articles.items():
        articles[i]["summary"] = summarize_text(article["content"])
    
    # Sauvegarde des articles avec résumés
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Résumés générés et enregistrés dans {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_summaries()
