"""
ATS Score Calculator
Calculate overall ATS compatibility score
"""

import re
from typing import Tuple, List, Dict


class ATSScoreCalculator:
    """Calculate ATS compatibility score with detailed breakdown"""
    
    # Score component weights
    WEIGHTS = {
        'keyword_match': 25,
        'semantic_similarity': 35,
        'section_completeness': 15,
        'contact_info': 10,
        'formatting': 10,
        'contextual_match': 5
    }
    
    # Thresholds for labels
    THRESHOLDS = {
        'excellent': 70,
        'good': 55,
        'fair': 35
    }
    
    @staticmethod
    def identify_sections(text: str) -> Dict[str, str]:
        """
        Identify different sections in resume
        Works universally across all domains
        """
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'certifications': '',
            'summary': ''
        }
        
        # Universal section patterns
        section_patterns = {
            'education': r'(?:education|academic|qualification|degree|university|college)',
            'experience': r'(?:experience|employment|work|career|history|professional)',
            'skills': r'(?:skills|competencies|expertise|proficiencies|technical|capabilities)',
            'projects': r'(?:projects|portfolio|work samples|achievements)',
            'certifications': r'(?:certifications?|certificates?|licenses?|credentials)',
            'summary': r'(?:summary|profile|objective|about|overview)'
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line_lower) and len(line_lower) < 50:
                    current_section = section
                    break
            
            # Add content to current section
            if current_section and line.strip():
                sections[current_section] += line + '\n'
        
        return sections
    
    @staticmethod
    def calculate_section_score(resume_text: str) -> float:
        """Calculate score based on section completeness"""
        sections = ATSScoreCalculator.identify_sections(resume_text)
        required_sections = ['education', 'experience', 'skills']
        
        sections_found = sum(
            1 for sec in required_sections 
            if sections[sec].strip()
        )
        
        return (sections_found / len(required_sections)) * ATSScoreCalculator.WEIGHTS['section_completeness']
    
    @staticmethod
    def calculate_contact_score(resume_text: str) -> float:
        """Calculate score based on contact information"""
        score = 0
        
        # Check for email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score += 5
        
        # Check for phone
        if re.search(r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', resume_text):
            score += 5
        
        return score
    
    @staticmethod
    def calculate_formatting_score(resume_text: str) -> float:
        """Calculate score based on document formatting"""
        score = 0
        
        # Check minimum length
        if len(resume_text) > 500:
            score += 5
        
        # Check structure (multiple lines/paragraphs)
        if len(resume_text.split('\n')) > 10:
            score += 5
        
        return score
    
    @staticmethod
    def calculate_contextual_score(resume_text: str, jd_text: str) -> float:
        """Calculate contextual matching score"""
        # Extract important phrases from JD
        jd_phrases = re.findall(r'\b\w+\s+\w+\s+\w+\b', jd_text.lower())[:15]
        resume_lower = resume_text.lower()
        
        # Count phrase matches
        phrase_matches = sum(1 for phrase in jd_phrases if phrase in resume_lower)
        
        if not jd_phrases:
            return 0
        
        match_ratio = phrase_matches / len(jd_phrases)
        return match_ratio * ATSScoreCalculator.WEIGHTS['contextual_match']
    
    @staticmethod
    def calculate_ats_score(
        resume_text: str,
        jd_text: str,
        matched_keywords: List[str],
        jd_keywords: List[str],
        semantic_similarity: float
    ) -> Tuple[float, str]:
        """
        Calculate comprehensive ATS score
        Returns: (score, label)
        """
        score = 0.0
        
        # 1. Keyword Match (25 points)
        if jd_keywords:
            keyword_ratio = len(matched_keywords) / len(jd_keywords)
            score += keyword_ratio * ATSScoreCalculator.WEIGHTS['keyword_match']
        
        # 2. Semantic Similarity (35 points) - MOST IMPORTANT
        score += semantic_similarity * ATSScoreCalculator.WEIGHTS['semantic_similarity']
        
        # 3. Section Completeness (15 points)
        score += ATSScoreCalculator.calculate_section_score(resume_text)
        
        # 4. Contact Information (10 points)
        score += ATSScoreCalculator.calculate_contact_score(resume_text)
        
        # 5. Formatting Quality (10 points)
        score += ATSScoreCalculator.calculate_formatting_score(resume_text)
        
        # 6. Contextual Matching (5 points)
        score += ATSScoreCalculator.calculate_contextual_score(resume_text, jd_text)
        
        # Determine label
        if score >= ATSScoreCalculator.THRESHOLDS['excellent']:
            label = "Excellent"
        elif score >= ATSScoreCalculator.THRESHOLDS['good']:
            label = "Good"
        elif score >= ATSScoreCalculator.THRESHOLDS['fair']:
            label = "Fair"
        else:
            label = "Poor"
        
        return round(score, 2), label