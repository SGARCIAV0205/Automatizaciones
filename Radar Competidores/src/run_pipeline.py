# src/run_pipeline.py
import os
from .utils import ensure_dirs, load_cfg
from . import scrape_news, score_builder, radar_plot, brechas_plot, historico_plot, build_report

def main():
    ensure_dirs()
    print("1) Scrapear noticias...")
    scrape_news.main()

    print("2) Construir puntajes...")
    score_builder.main()

    print("3) Generar imagen del radar...")
    radar_plot.main()

    print("4) Generar gráfica de brechas UBIMIA vs líder...")
    brechas_plot.main()

    print("5) Generar histórico (hasta 3 cortes)...")
    historico_plot.main()

    print("6) Armar reporte PPTX...")
    build_report.main()

    cfg = load_cfg()
    if cfg.get("pdf", {}).get("use_libreoffice", False):
        from subprocess import run
        periodo = cfg["periodo"]
        pptx_in = f"reports/out/reporte_radar_UBIMIA_auto_v3_{periodo}.pptx"
        out_dir = "reports/out"
        soffice = cfg["pdf"].get("libreoffice_path", "soffice")
        print("7) Exportar a PDF con LibreOffice...")
        run([soffice, "--headless", "--convert-to", "pdf", pptx_in, "--outdir", out_dir], check=False)
        print("[OK] Exportación PDF (si LibreOffice está instalado).")

if __name__ == "__main__":
    main()
