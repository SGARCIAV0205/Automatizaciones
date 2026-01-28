# src/scrape_news.py

import re
import time
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .utils import load_cfg, ensure_dirs, today_iso

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; UBIMIA-Competitive-Radar/1.0)"}


def classify_topic(text, topic_rules):
    t = (text or "").lower()
    for topic, kws in topic_rules.items():
        if any(k in t for k in kws):
            return topic
    return "General"


def scrape_company_news(name, urls, topic_rules):
    rows = []
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            # heurísticas: titulares <a>, <h3>, <h2>
            candidates = []
            for tag in soup.select("a"):
                title = tag.get_text(strip=True)
                href = tag.get("href", "")
                if title and len(title) > 30 and href and not href.startswith("#"):
                    candidates.append((title, href))
            for tag in soup.select("h3, h2"):
                title = tag.get_text(strip=True)
                if title and len(title) > 30:
                    candidates.append((title, None))

            # normalizar
            seen = set()
            for title, href in candidates[:30]:
                key = (title, href)
                if key in seen:
                    continue
                seen.add(key)
                domain = ""
                if href:
                    try:
                        domain = urlparse(href).netloc
                    except Exception:
                        domain = ""
                topic = classify_topic(title, topic_rules)
                rows.append({
                    "fecha": today_iso(),             # si no hay fecha en la fuente
                    "empresa": name,
                    "titular": title,
                    "fuente": domain or urlparse(url).netloc,
                    "url": href or url,
                    "tema": topic,
                    "impacto": "Medio" if topic != "Alianzas/Expansión" else "Alto"
                })
            time.sleep(1.0)  # respetar
        except Exception as e:
            rows.append({
                "fecha": today_iso(),
                "empresa": name,
                "titular": f"[WARN] No se pudo leer {url}: {e}",
                "fuente": urlparse(url).netloc if '//' in url else url,
                "url": url,
                "tema": "General",
                "impacto": "Bajo"
            })
    return rows


def main():
    cfg = load_cfg()
    ensure_dirs()
    periodo = cfg["periodo"]
    topic_rules = cfg.get("topic_keywords", {})

    # AHORA: leer competidores desde config.yaml
    # Preferimos `competitors`; si no existe, usamos `empresas` para compatibilidad.
    competitors = cfg.get("competitors", cfg.get("empresas", []))

    sources = cfg.get("news_sources", {})

    all_rows = []
    for comp in competitors:
        urls = sources.get(comp, [])
        if not urls:
            # Si no hay fuentes definidas para este competidor, lo saltamos silenciosamente
            # (o aquí podrías implementar un fallback con Google News si quieres).
            continue
        rows = scrape_company_news(comp, urls, topic_rules)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows) if all_rows else pd.DataFrame(
        columns=["fecha", "empresa", "titular", "fuente", "url", "tema", "impacto"]
    )
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date.astype(str)

    out_csv = f"data/processed/noticias_{periodo}.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"[OK] Noticias guardadas en {out_csv} (filas={len(df)})")


if __name__ == "__main__":
    main()
