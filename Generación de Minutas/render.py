import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pypandoc

def render_markdown(payload: dict, templates_dir=None, tpl_name="minuta.md.j2") -> str:
    # Si no se especifica templates_dir, usar la ruta relativa al archivo actual
    if templates_dir is None:
        current_dir = Path(__file__).parent
        templates_dir = current_dir / "templates"
    
    # Asegurar que templates_dir sea un Path y existe
    templates_path = Path(templates_dir)
    if not templates_path.exists():
        raise FileNotFoundError(f"Directorio de templates no encontrado: {templates_path}")
    
    env = Environment(
        loader=FileSystemLoader(str(templates_path)), 
        autoescape=False, 
        trim_blocks=True, 
        lstrip_blocks=True
    )
    tpl = env.get_template(tpl_name)
    return tpl.render(**payload)

def save_outputs(md: str, payload: dict, out_base: Path):
    out_base.parent.mkdir(parents=True, exist_ok=True)
    (out_base.with_suffix(".md")).write_text(md, encoding="utf-8")
    (out_base.with_suffix(".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        pypandoc.convert_text(md, "pdf", format="md", outputfile=str(out_base.with_suffix(".pdf")))
        pypandoc.convert_text(md, "docx", format="md", outputfile=str(out_base.with_suffix(".docx")))
    except Exception:
        pass  # si no hay pandoc, seguimos con .md y .json
