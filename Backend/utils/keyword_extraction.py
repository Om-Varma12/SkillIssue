from sklearn.feature_extraction.text import CountVectorizer
from typing import Tuple, List, Set

def get_keywords(text: str, top_n: int = 50) -> Set[str]:
    """
    Simple keyword extraction using CountVectorizer.
    Returns a set of top N tokens.
    """
    if not text or not text.strip():
        return set()
    vectorizer = CountVectorizer(max_features=top_n, stop_words="english")
    try:
        _ = vectorizer.fit_transform([text])
    except ValueError:
        return set()
    return set(vectorizer.get_feature_names_out())

def compare_keywords(resume_keywords: Set[str], jd_keywords: Set[str]) -> Tuple[List[str], List[str]]:
    matched = list(sorted(resume_keywords.intersection(jd_keywords)))
    missing = list(sorted(jd_keywords.difference(resume_keywords)))
    return matched, missing
