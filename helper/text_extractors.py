import io


def _extract_pdf(file_bytes: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_docx(file_bytes: bytes) -> str:
    from docx import Document as DocxDoc
    doc = DocxDoc(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _extract_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def _get_ext(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def _title_from_filename(filename: str) -> str:
    name = filename.rsplit(".", 1)[0]
    return name.replace("-", " ").replace("_", " ").title()

EXTRACTORS = {
    "pdf":  _extract_pdf,
    "docx": _extract_docx,
    "doc":  _extract_docx,
    "txt":  _extract_txt,
    "md":   _extract_txt,
    "rst":  _extract_txt,
}