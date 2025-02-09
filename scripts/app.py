import streamlit as st
import json
import requests

# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000"

# Charger les articles depuis l'API
def get_articles():
    response = requests.get(f"{API_URL}/articles")
    if response.status_code == 200:
        return response.json()["articles"]
    return {}

# Interface Streamlit
st.set_page_config(page_title="📰 BBC Scraper", layout="wide")

st.title("📑 BBC Scraper - Articles, Résumés et Mots-clés")

articles = get_articles()

if articles:
    article_ids = list(articles.keys())
    selected_id = st.sidebar.selectbox("📌 Sélectionne un article :", article_ids)

    if selected_id:
        article = articles[selected_id]

        st.header(f"📰 {article['url']}")
        st.subheader("📜 Contenu Original")
        st.write(article["content"])

        st.subheader("📝 Résumé")
        st.success(article.get("summary", "Résumé non disponible."))

        st.subheader("🔑 Mots-clés")
        st.write(", ".join(article.get("keywords", [])))
else:
    st.warning("⚠️ Aucun article trouvé. Vérifie que l'API est bien en cours d'exécution.")
