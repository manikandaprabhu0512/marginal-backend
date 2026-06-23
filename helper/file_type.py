import os
from urllib.parse import urlparse


def detect_source_type(url: str) -> str:
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()

    if ext == ".pdf":
        return "pdf"
    elif ext in [".txt", ".md", ".rst"]:
        return "text"
    elif ext in [".doc", ".docx"]:
        return "document"
    elif ext in [".csv", ".xlsx", ".xls"]:
        return "spreadsheet"
    elif ext in [".mp3", ".mp4", ".wav", ".youtube.com", ".youtu.be"]:
        return "media"
    elif "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
        return "video"
    elif not ext:
        return "link"
    else:
        return "link"