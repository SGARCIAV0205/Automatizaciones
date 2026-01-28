import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from .utils import load_cfg, ensure_dirs

def plot_radar(df, axes_names, out_png):
    N = len(axes_names)
    angles = [n/float(N)*2*np.pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(7,7))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi/2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(axes_names)
    ax.set_yticks([1,2,3,4,5])
    ax.set_ylim(0,5)

    for _, row in df.iterrows():
        vals = [row[c] for c in axes_names]
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=1, linestyle="solid", label=row["provider"])
        ax.fill(angles, vals, alpha=0.1)

    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.10))
    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    plt.close()

def main():
    cfg = load_cfg()
    ensure_dirs()
    periodo = cfg["periodo"]
    axes = cfg["axes"]
    axes_names = [a["name"] for a in axes]

    scores_csv = f"data/processed/radar_scores_{periodo}.csv"
    df = pd.read_csv(scores_csv)

    out_png = f"data/processed/radar_{periodo}.png"
    plot_radar(df, axes_names, out_png)
    print(f"[OK] Radar PNG guardado en {out_png}")

if __name__ == "__main__":
    main()
