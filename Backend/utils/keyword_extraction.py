"""
Keyword Extraction
Extract and compare keywords between resume and JD
"""

import re
from collections import Counter
from typing import List, Tuple, Set
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    import os
    os.system('pip install sentence-transformers scikit-learn')
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

from .text_preprocessing import TextPreprocessor


class KeywordExtractor:
    """Extract and match keywords using NLP"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = TextPreprocessor()
    
    def extract_dynamic_keywords(self, text: str, top_n: int = 100) -> List[str]:
        """
        Extract keywords dynamically using frequency analysis
        No predefined keyword list - works for any domain
        """
        # Extract words and n-grams
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        two_grams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        three_grams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
        
        # Combine all terms
        all_terms = words + two_grams + three_grams
        
        # Filter stop words
        filtered_terms = self.preprocessor.filter_stop_words(all_terms)
        filtered_terms = [term for term in filtered_terms if len(term) > 2]
        
        # Get frequency
        term_freq = Counter(filtered_terms)
        
        # Return top keywords
        return [term for term, _ in term_freq.most_common(top_n)]
    
    def extract_all_terms(self, text: str, top_n: int = 100) -> Set[str]:
        """
        Combine dynamic keywords and technical terms
        """
        # Get frequency-based keywords
        keywords = self.extract_dynamic_keywords(text, top_n)
        
        # Get technical terms
        technical_terms = self.preprocessor.extract_technical_terms(text)
        
        # Combine and return
        all_terms = set(keywords) | technical_terms
        return all_terms
    
    def semantic_keyword_matching(
        self, 
        resume_keywords: List[str], 
        jd_keywords: List[str],
        threshold: float = 0.7
    ) -> Tuple[List[str], List[str]]:
        """
        Match keywords using semantic similarity (AI-powered)
        Returns: (matched_keywords, missing_keywords)
        """
        if not resume_keywords or not jd_keywords:
            return [], jd_keywords
        
        # Get embeddings for all keywords
        resume_embeddings = self.model.encode(resume_keywords)
        jd_embeddings = self.model.encode(jd_keywords)
        
        matched = []
        missing = []
        
        for i, jd_kw in enumerate(jd_keywords):
            # Calculate similarity with all resume keywords
            similarities = cosine_similarity([jd_embeddings[i]], resume_embeddings)[0]
            max_similarity = np.max(similarities)
            
            if max_similarity >= threshold:
                matched.append(jd_kw)
            else:
                missing.append(jd_kw)
        
        return matched, missing
    
    def prioritize_keywords(
        self, 
        keywords: List[str], 
        text: str, 
        top_n: int = 7
    ) -> List[str]:
        """
        Prioritize keywords by frequency in text
        """
        keyword_freq = []
        text_lower = text.lower()
        
        for kw in keywords:
            count = text_lower.count(kw.lower())
            keyword_freq.append((kw, count))
        
        # Sort by frequency
        keyword_freq.sort(key=lambda x: x[1], reverse=True)
        
        return [kw for kw, _ in keyword_freq[:top_n]]