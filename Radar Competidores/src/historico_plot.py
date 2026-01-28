# src/historico_plot.py

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import load_cfg, ensure_dirs

def main():
    cfg = load_cfg()
    ensure_dirs()

    periodo_actual = cfg["periodo"]

    # Buscar últimos hasta 3 archivos radar_scores_YYYY-MM.csv
    files = sorted(
        glob.glob("data/processed/radar_scores_*.csv")
    )
    if not files:
        print("[WARN] No hay archivos de histórico para graficar.")
        return

    # Tomar máximo 3 cortes más recientes
    files = files[-3:]

    # Extraer periodo de nombre de archivo
    periodos = [os.path.splitext(os.path.basename(f))[0].split("_")[-1] for f in files]

    # Leer y apilar
    dfs = []
    for f, p in zip(files, periodos):
        df = pd.read_csv(f)
        df["periodo"] = p
        dfs.append(df)
    hist = pd.concat(dfs, ignore_index=True)

    # Proveedores
    proveedores = hist["provider"].unique()
    periodos_ord = sorted(hist["periodo"].unique())  # para eje X ordenado

    # Construir matriz de scores [proveedor x periodo]
    data = {}
    for prov in proveedores:
        sub = hist[hist["provider"] == prov].set_index("periodo")["score_ponderado"]
        data[prov] = [sub.get(p, np.nan) for p in periodos_ord]

    # ---- Gráfica ----
    plt.figure(figsize=(10, 5))

    x = np.arange(len(periodos_ord))
    n_prov = len(proveedores)

    for j, prov in enumerate(proveedores):
        y = np.array(data[prov], dtype=float)

        if len(periodos_ord) == 1:
            # SOLO UN PERIODO: separar ligeramente a cada proveedor en X
            base_x = x[0]
            offset = (j - (n_prov - 1) / 2) * 0.05  # 0.05 = separación visual
            x_j = base_x + offset
            plt.scatter(x_j, y[0], label=prov)  # un punto por proveedor

            # Opcional: etiquetar cada punto con el proveedor
            plt.text(
                x_j + 0.01, y[0],
                prov,
                fontsize=8,
                va="center"
            )
        else:
            # VARIOS PERIODOS: líneas normales por proveedor
            plt.plot(x, y, marker="o", label=prov)

    plt.xticks(x, periodos_ord)
    plt.xlabel("Periodo")
    plt.ylabel("Score total (0–100)")
    plt.title("Tendencia histórica de desempeño competitivo")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    out_png = f"data/processed/historico_{periodo_actual}.png"
    plt.savefig(out_png, dpi=180)
    plt.close()
    print(f"[OK] Histórico guardado en {out_png}")

if __name__ == "__main__":
    main()
