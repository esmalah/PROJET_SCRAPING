import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Chemin du fichier JSON contenant les articles
DATA_FILE = "./data/bbc_articles.json"
INDEX_FILE = "./data/articles_faiss.index"

# Charger le modèle de transformation de texte en vecteurs
print("🔄 Chargement du modèle d'embedding...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Modèle chargé avec succès.")

def load_articles():
    """Charge les articles depuis le fichier JSON."""
    if not os.path.exists(DATA_FILE):
        print("Aucun fichier JSON trouvé.")
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    return [article["content"] for article in articles.values()]

def index_articles():
    """Convertit les articles en vecteurs et les stocke dans FAISS."""
    articles = load_articles()
    
    if not articles:
        print("Aucun article à indexer.")
        return
    
    print(f"🔄 Encodage de {len(articles)} articles en vecteurs...")
    embeddings = model.encode(articles, convert_to_numpy=True)

    # Création de l'index FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Sauvegarde de l'index FAISS
    faiss.write_index(index, INDEX_FILE)
    print(f"Index FAISS sauvegardé dans {INDEX_FILE}")

if __name__ == "__main__":
    index_articles()
