import re

# small builtin stoplist to avoid external downloads
STOPWORDS = {
    "the","and","is","in","to","of","a","for","with","on","that","as","by","an","be","are","this","it","from"
}

def clean_text(text: str) -> str:
    """
    Minimal text cleaning:
      - Lowercase
      - Remove non-alphanumeric (except spaces)
      - Remove extra spaces
      - Remove stopwords
    Returns cleaned, space-joined string.
    """
    if not text:
        return ""
    t = text.lower()
    # Replace non-alphanum with space
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    tokens = [tok.strip() for tok in t.split() if tok.strip()]
    filtered = [tok for tok in tokens if tok not in STOPWORDS and len(tok) > 1]
    return " ".join(filtered)
