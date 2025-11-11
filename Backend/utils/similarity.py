"""
Similarity Calculations
Compute semantic similarity between texts
"""

import re
from typing import List
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    import os
    os.system('pip install sentence-transformers scikit-learn')
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """Calculate semantic similarity using embeddings"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        Returns: similarity score (0.0 to 1.0)
        """
        if not text1 or not text2:
            return 0.0
        
        # Generate embeddings
        embeddings = self.model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return float(similarity)
    
    def extract_relevant_highlights(
        self, 
        resume_text: str, 
        jd_text: str, 
        top_n: int = 5
    ) -> List[str]:
        """
        Extract most relevant sentences from resume based on JD
        Uses semantic similarity + heuristics
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', resume_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return []
        
        # Get JD embedding
        jd_embedding = self.model.encode([jd_text])[0]
        
        # Calculate similarity for each sentence
        sentence_scores = []
        
        for sentence in sentences:
            sent_embedding = self.model.encode([sentence])[0]
            similarity = cosine_similarity([sent_embedding], [jd_embedding])[0][0]
            
            # Apply boosting heuristics
            
            # Boost if contains numbers (achievements/metrics)
            if re.search(r'\d+', sentence):
                similarity *= 1.15
            
            # Boost if contains action verbs
            action_verbs = r'\b(developed|created|designed|implemented|managed|led|built|achieved|improved|increased|reduced)\b'
            if re.search(action_verbs, sentence.lower()):
                similarity *= 1.1
            
            sentence_scores.append((sentence, similarity))
        
        # Sort by score and return top N
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [sent for sent, _ in sentence_scores[:top_n]]
    
    def calculate_phrase_overlap(self, text1: str, text2: str, n: int = 15) -> float:
        """
        Calculate overlap of important phrases between two texts
        Returns: overlap ratio (0.0 to 1.0)
        """
        # Extract important n-word phrases
        phrases1 = set(re.findall(r'\b\w+\s+\w+\s+\w+\b', text1.lower())[:n])
        phrases2 = set(re.findall(r'\b\w+\s+\w+\s+\w+\b', text2.lower())[:n])
        
        if not phrases1 or not phrases2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(phrases1 & phrases2)
        union = len(phrases1 | phrases2)
        
        return intersection / union if union > 0 else 0.0