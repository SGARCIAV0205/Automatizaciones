# src/brechas_plot.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import load_cfg, ensure_dirs

def compute_gaps(scores_df: pd.DataFrame, axes: list, focal: str = "UBIMIA") -> pd.DataFrame:
    """
    Calcula la brecha por eje entre el líder y la empresa 'focal' (por defecto UBIMIA).
    Devuelve un DataFrame con columnas: ['eje', 'gap', 'lider'].
    gap = max(0, score_lider - score_focal) en escala 1–5.
    """
    if scores_df.empty or focal not in set(scores_df["provider"]):
        return pd.DataFrame(columns=["eje", "gap", "lider"])

    ub_row = scores_df[scores_df["provider"] == focal].iloc[0]
    rows = []
    for eje in axes:
        leader_idx = scores_df[eje].idxmax()
        leader_val = scores_df.loc[leader_idx, eje]
        leader_name = scores_df.loc[leader_idx, "provider"]
        gap = max(0.0, leader_val - ub_row[eje])
        rows.append({"eje": eje, "gap": gap, "lider": leader_name})

    gaps = pd.DataFrame(rows)
    gaps = gaps.sort_values("gap", ascending=False).reset_index(drop=True)
    return gaps

def main():
    cfg = load_cfg()
    ensure_dirs()
    periodo = cfg["periodo"]
    axes_cfg = cfg["axes"]
    axes = [a["name"] for a in axes_cfg]

    scores_csv = f"data/processed/radar_scores_{periodo}.csv"
    out_png = f"data/processed/brechas_{periodo}.png"

    if not os.path.exists(scores_csv):
        print(f"[WARN] No existe {scores_csv}, no se genera gráfica de brechas.")
        # placeholder
        plt.figure(figsize=(8, 4))
        plt.axis("off")
        plt.text(0.5, 0.5, "Sin datos para brechas", ha="center", va="center")
        plt.savefig(out_png, dpi=180)
        plt.close()
        return

    df = pd.read_csv(scores_csv)
    gaps = compute_gaps(df, axes, focal="UBIMIA")

    plt.figure(figsize=(10, 6))
    if gaps.empty:
        # Caso: no podemos calcular brechas (UBIMIA no está o df vacío)
        plt.axis("off")
        plt.text(0.5, 0.5, "No fue posible calcular brechas vs líder.", ha="center", va="center")
    else:
        max_gap = gaps["gap"].max()
        if max_gap == 0:
            # Caso: UBIMIA está alineada con el líder en todos los ejes
            plt.axis("off")
            plt.text(
                0.5, 0.5,
                "UBIMIA está alineada con el líder en todos los ejes (brechas = 0).",
                ha="center", va="center", wrap=True
            )
        else:
            y = np.arange(len(gaps))
            plt.barh(y, gaps["gap"])
            plt.yticks(y, gaps["eje"])
            plt.gca().invert_yaxis()
            plt.xlabel("Brecha vs líder (puntos en escala 1–5)")
            plt.title("Brechas UBIMIA vs líder por eje")
            plt.xlim(0, max_gap * 1.1)

    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    plt.close()
    print(f"[OK] Gráfica de brechas guardada en {out_png}")

if __name__ == "__main__":
    main()
