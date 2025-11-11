"""
Text Preprocessing Utilities
Clean and normalize text for analysis
"""

import re
from typing import List, Set


class TextPreprocessor:
    """Clean and prepare text for analysis"""
    
    # Comprehensive stop words
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'who', 'which', 'what', 'where', 'when', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'than', 'too', 'very', 'own', 'same', 'so', 'about', 'after',
        'also', 'any', 'because', 'before', 'between', 'into', 'through',
        'during', 'only', 'our', 'their', 'its', 'his', 'her', 'your',
        'my', 'me', 'him', 'them', 'us', 'up', 'out', 'if', 'about', 'then'
    }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Basic text cleaning
        - Remove extra whitespace
        - Keep important punctuation
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\+\#\.\,\(\)/]', ' ', text)
        return text.strip()
    
    @staticmethod
    def extract_noun_phrases(text: str) -> List[str]:
        """Extract potential skill phrases using linguistic patterns"""
        phrases = []
        
        # Pattern 1: Capitalized multi-word terms
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        phrases.extend(capitalized)
        
        # Pattern 2: Technical acronyms
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        phrases.extend(acronyms)
        
        # Pattern 3: Hyphenated terms
        hyphenated = re.findall(r'\b\w+(?:-\w+)+\b', text)
        phrases.extend(hyphenated)
        
        # Pattern 4: Common skill patterns
        skill_patterns = [
            r'\b\w+(?:\s+\w+){0,2}\s+(?:skills?|experience|knowledge|proficiency)\b',
            r'\b(?:expert|proficient|experienced)\s+(?:in|with)\s+\w+(?:\s+\w+){0,2}\b',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)
        
        return [phrase.strip() for phrase in phrases if len(phrase.strip()) > 2]
    
    @staticmethod
    def extract_technical_terms(text: str) -> Set[str]:
        """Extract technical terms using multiple strategies"""
        terms = set()
        
        # Strategy 1: Noun phrases and acronyms
        noun_phrases = TextPreprocessor.extract_noun_phrases(text)
        terms.update([p.lower() for p in noun_phrases])
        
        # Strategy 2: Terms after key indicators
        skill_indicators = [
            r'(?:skills?|technologies|tools|software|languages|frameworks|platforms|systems)[:\s]+([^.!?\n]+)',
            r'(?:experience|proficiency|expertise|knowledge)\s+(?:in|with)[:\s]+([^.!?\n]+)',
            r'(?:using|worked with|utilized|implemented)[:\s]+([^.!?\n]+)',
        ]
        
        for pattern in skill_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                items = re.split(r'[,;/&]|\sand\s|\sor\s', match)
                terms.update([item.strip().lower() for item in items if len(item.strip()) > 2])
        
        # Strategy 3: Bullet points often contain skills
        bullet_lines = re.findall(r'[•\-\*]\s*(.+)', text)
        for line in bullet_lines:
            words = re.findall(r'\b[A-Za-z][\w\-\.]+\b', line)
            terms.update([w.lower() for w in words if len(w) > 3])
        
        return terms
    
    @staticmethod
    def filter_stop_words(terms: List[str]) -> List[str]:
        """Remove stop words from list of terms"""
        return [
            term for term in terms 
            if not any(stop in term.lower().split() for stop in TextPreprocessor.STOP_WORDS)
        ]