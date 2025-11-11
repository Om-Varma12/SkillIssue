from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document

def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file.
    Supports TXT, PDF, DOCX formats.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = p.suffix.lower()
    text = ""

    if ext == ".txt":
        text = p.read_text(encoding="utf-8", errors="ignore")

    elif ext == ".pdf":
        text = read_pdf(p)

    elif ext in [".docx", ".doc"]:
        text = read_docx(p)

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text.strip()


def read_pdf(path: Path) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    with open(path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def read_docx(path: Path) -> str:
    """
    Extracts text from a DOCX file.
    """
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)
