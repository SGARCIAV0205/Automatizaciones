# src/score_builder.py

import os
import numpy as np
import pandas as pd
from .utils import load_cfg, ensure_dirs

MANUAL_PATH = "data/raw/puntajes_manual.csv"  # opcional


def prev_period(p: str) -> str:
    """Devuelve el periodo anterior en formato YYYY-MM."""
    y, m = map(int, p.split("-"))
    m -= 1
    if m == 0:
        y -= 1
        m = 12
    return f"{y}-{m:02d}"


def _build_news_features(news_df: pd.DataFrame, providers: list) -> pd.DataFrame:
    """
    Construye features a partir de las noticias:
    - conteos por tema
    - total de noticias
    - proporciones por tema
    Devuelve un DF indexado por provider.
    """
    if news_df.empty:
        # Crear DF vacío con ceros para todos los competidores
        return pd.DataFrame(
            {
                "provider": providers,
                "n_total": [0] * len(providers),
                "n_producto": [0] * len(providers),
                "n_integraciones": [0] * len(providers),
                "n_ia": [0] * len(providers),
                "n_seguridad": [0] * len(providers),
                "n_implementacion": [0] * len(providers),
                "n_pricing": [0] * len(providers),
                "n_alianzas": [0] * len(providers),
                "n_finanzas": [0] * len(providers),
            }
        ).set_index("provider")

    df = news_df.copy()
    df["empresa"] = df["empresa"].astype(str)

    # Normalizamos nombres de tema por si vienen ligeramente distintos
    df["tema_norm"] = df["tema"].fillna("General").astype(str)

    # Conteos por empresa y tema
    pivot = (
        df.pivot_table(
            index="empresa",
            columns="tema_norm",
            values="titular",
            aggfunc="count",
            fill_value=0,
        )
        .rename_axis(index="provider", columns="tema")
        .reset_index()
    )

    # Asegurar que existan columnas para los temas clave
    for col in [
        "Producto",
        "Integraciones",
        "IA/Automatización",
        "Seguridad/Compliance",
        "Implementación",
        "Pricing/Valor",
        "Alianzas/Expansión",
        "Finanzas/Capital",
    ]:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot["n_total"] = pivot[
        [
            "Producto",
            "Integraciones",
            "IA/Automatización",
            "Seguridad/Compliance",
            "Implementación",
            "Pricing/Valor",
            "Alianzas/Expansión",
            "Finanzas/Capital",
        ]
    ].sum(axis=1)

    pivot = pivot.rename(
        columns={
            "Producto": "n_producto",
            "Integraciones": "n_integraciones",
            "IA/Automatización": "n_ia",
            "Seguridad/Compliance": "n_seguridad",
            "Implementación": "n_implementacion",
            "Pricing/Valor": "n_pricing",
            "Alianzas/Expansión": "n_alianzas",
            "Finanzas/Capital": "n_finanzas",
        }
    )

    # Asegurar filas para todos los providers, aunque no tengan noticias
    pivot = pivot.set_index("provider")
    for p in providers:
        if p not in pivot.index:
            pivot.loc[p] = 0

    return pivot.sort_index()


def _axis_score_from_features(axis_name: str, feats: pd.Series) -> float:
    """
    Regla más compleja por eje, basada en conteos de noticias.
    Usamos una base y ajustamos con log(1 + conteos) de distintos temas.
    """
    base = 3.0  # neutro

    # Intensidades por tema
    log_total = np.log1p(feats.get("n_total", 0))
    log_prod = np.log1p(feats.get("n_producto", 0))
    log_int = np.log1p(feats.get("n_integraciones", 0))
    log_ia = np.log1p(feats.get("n_ia", 0))
    log_seg = np.log1p(feats.get("n_seguridad", 0))
    log_impl = np.log1p(feats.get("n_implementacion", 0))
    log_prc = np.log1p(feats.get("n_pricing", 0))
    log_ali = np.log1p(feats.get("n_alianzas", 0))
    log_fin = np.log1p(feats.get("n_finanzas", 0))

    v = base

    if axis_name == "Integraciones":
        v += 0.6 * log_int + 0.2 * log_prod
    elif axis_name == "Implementación":
        v += 0.5 * log_impl + 0.2 * log_prod
    elif axis_name == "IA/Automatización":
        v += 0.7 * log_ia + 0.2 * log_prod
    elif axis_name == "Seguridad/Compliance":
        v += 0.7 * log_seg + 0.3 * log_total
    elif axis_name == "Pricing/Valor":
        v += 0.5 * log_prc + 0.2 * log_fin
    elif axis_name == "Soporte/SLAs":
        # No tenemos tema explícito de soporte; usamos total y producto como proxy
        v += 0.4 * log_total + 0.3 * log_prod
    elif axis_name == "Tracción de mercado":
        v += 0.5 * log_ali + 0.4 * log_fin + 0.2 * log_total
    else:
        # Eje desconocido: usar total
        v += 0.4 * log_total

    # Clip a escala 1–5
    v = max(1.0, min(5.0, v))
    return float(v)


def _heuristic_scores(providers, axes, news_df, periodo: str) -> pd.DataFrame:
    """
    Construye puntajes por eje usando:
    - Features de noticias.
    - Suavizado con periodo anterior si hay histórico.
    """
    # Features por competidor
    feats = _build_news_features(news_df, providers)  # index = provider

    # Intentar cargar periodo anterior para suavizar
    prev_p = prev_period(periodo)
    prev_path = f"data/processed/radar_scores_{prev_p}.csv"
    if os.path.exists(prev_path):
        prev_df = pd.read_csv(prev_path)
        prev_df = prev_df.set_index("provider")
    else:
        prev_df = None

    rows = []
    for comp in providers:
        row = {"provider": comp}
        f = feats.loc[comp]

        for ax in axes:
            name = ax["name"]

            # Score "actual" según noticias
            score_cur = _axis_score_from_features(name, f)

            # Suavizado con periodo anterior si existe
            if prev_df is not None and name in prev_df.columns and comp in prev_df.index:
                prev_val = float(prev_df.loc[comp, name])
                # 70% peso actual, 30% histórico
                score = 0.7 * score_cur + 0.3 * prev_val
            else:
                score = score_cur

            # Clip final por seguridad
            score = max(1.0, min(5.0, score))
            row[name] = score

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    cfg = load_cfg()
    ensure_dirs()
    periodo = cfg["periodo"]
    axes = cfg["axes"]
    axis_names = [a["name"] for a in axes]
    weights = np.array([a["weight"] for a in axes], dtype=float)

    # Ahora leemos competidores desde config, con fallback a "empresas"
    providers = cfg.get("competitors", cfg.get("empresas", []))

    # Noticias del periodo (si no hay, DF vacío pero con columnas mínimas)
    news_csv = f"data/processed/noticias_{periodo}.csv"
    if os.path.exists(news_csv):
        news_df = pd.read_csv(news_csv)
    else:
        news_df = pd.DataFrame(columns=["empresa", "tema"])

    # 1) Si existe un archivo manual, usamos override completo
    if os.path.exists(MANUAL_PATH):
        scores = pd.read_csv(MANUAL_PATH)
        expected = set(["provider"] + axis_names)
        if not expected.issubset(scores.columns):
            raise ValueError(f"El CSV manual debe tener columnas al menos: {expected}")
        # Filtrar solo competidores actuales por si hay otros en el manual
        if providers:
            scores = scores[scores["provider"].isin(providers)].copy()
            # Si falta algún competidor, podríamos añadirlo
            faltan = set(providers) - set(scores["provider"])
            for comp in faltan:
                # asignación neutra si no está en manual
                row = {"provider": comp}
                for name in axis_names:
                    row[name] = 3.0
                scores = pd.concat([scores, pd.DataFrame([row])], ignore_index=True)
    else:
        # 2) Heurístico avanzado con noticias + histórico
        scores = _heuristic_scores(providers, axes, news_df, periodo)

    # Score ponderado 0–100
    X = scores[axis_names].values
    # Normalización lineal a 0–100; si todos iguales, evitamos división por 0
    raw = (X * weights).sum(axis=1) / max(weights.sum(), 1e-6)
    raw_min = raw.min()
    raw_max = raw.max()
    if raw_max > raw_min:
        score_norm = 100.0 * (raw - raw_min) / (raw_max - raw_min)
    else:
        score_norm = np.full_like(raw, 50.0)  # si todos iguales, todos 50

    scores["score_ponderado"] = score_norm

    out_csv = f"data/processed/radar_scores_{periodo}.csv"
    scores.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"[OK] Puntajes guardados en {out_csv}")

if __name__ == "__main__":
    main()
