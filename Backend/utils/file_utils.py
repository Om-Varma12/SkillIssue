from pathlib import Path
from PyPDF2 import PdfReader

def read_file_content(path: str) -> str:
    """
    Reads content from .txt or .pdf and returns plain text.
    Raises ValueError for unsupported types.
    """
    p = Path(path)
    suffix = p.suffix.lower()

    if suffix == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")
    elif suffix == ".pdf":
        text_parts = []
        reader = PdfReader(str(p))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    else:
        raise ValueError("Unsupported file type. Use .txt or .pdf")
