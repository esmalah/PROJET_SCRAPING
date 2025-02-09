from fastapi import FastAPI
import json
import os

#Chemins des fichiers JSON
DATA_FILE = "./data/bbc_articles_keywords.json"

#Initialisation de l'API
app = FastAPI(title="BBC Scraper API", description="API pour accéder aux articles scrappés, résumés et mots-clés.")

def load_articles():
    """Charge les articles depuis le fichier JSON."""
    if not os.path.exists(DATA_FILE):
        return {"error": "Aucun fichier JSON trouvé."}
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

#Endpoint pour récupérer tous les articles
@app.get("/articles", summary="Récupérer tous les articles")
async def get_articles():
    articles = load_articles()
    return {"articles": articles}

#Endpoint pour récupérer un article par son ID
@app.get("/articles/{article_id}", summary="Récupérer un article spécifique")
async def get_article(article_id: int):
    articles = load_articles()
    if str(article_id) not in articles:
        return {"error": "Article non trouvé"}
    return articles[str(article_id)]

#Endpoint pour récupérer les mots-clés d'un article
@app.get("/articles/{article_id}/keywords", summary="Récupérer les mots-clés d'un article")
async def get_article_keywords(article_id: int):
    articles = load_articles()
    if str(article_id) not in articles:
        return {"error": "Article non trouvé"}
    return {"keywords": articles[str(article_id)].get("keywords", [])}

#Endpoint pour récupérer le résumé d'un article
@app.get("/articles/{article_id}/summary", summary="Récupérer le résumé d'un article")
async def get_article_summary(article_id: int):
    articles = load_articles()
    if str(article_id) not in articles:
        return {"error": "Article non trouvé"}
    return {"summary": articles[str(article_id)].get("summary", "Résumé non disponible")}

#Endpoint de test
@app.get("/", summary="Endpoint de test")
async def root():
    return {"message": "API BBC Scraper est en ligne 🚀"}

