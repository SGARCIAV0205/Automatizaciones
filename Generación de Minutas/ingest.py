# ingest.py
from pathlib import Path
from docx import Document
import webvtt
import srt

def load_transcript(path: str) -> str:
    """
    Lee una transcripción desde .txt, .docx, .vtt o .srt y devuelve texto plano.
    """
    p = Path(path)
    suf = p.suffix.lower()

    if suf == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")

    if suf == ".docx":
        doc = Document(p)
        return "\n".join([para.text for para in doc.paragraphs])

    if suf == ".vtt":
        # webvtt.read itera por cues; unimos solo el texto
        return "\n".join([cue.text for cue in webvtt.read(str(p))])

    if suf == ".srt":
        subs = list(srt.parse(p.read_text(encoding="utf-8", errors="ignore")))
        return "\n".join([seg.content for seg in subs])

    raise ValueError(f"Formato no soportado: {suf}")
