# ingest/news_fetcher.py

import datetime as dt
import feedparser
from typing import List, Dict

from config import MAX_NEWS_PER_CLIENT


# ============================================================
# Helpers
# ============================================================

def _parse_date(entry):
    """
    Intenta extraer fecha de una entrada RSS
    """
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return dt.date(
            entry.published_parsed.tm_year,
            entry.published_parsed.tm_mon,
            entry.published_parsed.tm_mday
        )
    return None


# ============================================================
# Fuente: Google News RSS
# ============================================================

def fetch_news_google_rss(query: str) -> List[Dict]:
    """
    Busca noticias usando Google News RSS
    """
    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={query}&hl=es-419&gl=MX&ceid=MX:es-419"
    )

    feed = feedparser.parse(rss_url)

    news = []
    for entry in feed.entries[:MAX_NEWS_PER_CLIENT]:
        news.append({
            "fecha": _parse_date(entry),
            "titular": entry.title,
            "fuente": entry.source.title if hasattr(entry, "source") else "Google News",
            "url": entry.link
        })

    return news


# ============================================================
# API pública del módulo
# ============================================================

def fetch_news(cliente: dict, periodo: str) -> List[Dict]:
    """
    Punto único de entrada para obtener noticias de un cliente.

    cliente: dict con keys name, keywords
    periodo: string (ej. 'Q1 2026') – se usa solo como contexto
    """

    keywords = cliente.get("keywords", [])
    if not keywords:
        return []

    query = " ".join(keywords)

    try:
        return fetch_news_google_rss(query)
    except Exception:
        # Fail-safe: nunca romper el flujo
        return []
