"""
Section Matcher
Analyze how well each resume section matches the JD
"""

from typing import Dict, List

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    import os
    os.system('pip install sentence-transformers scikit-learn')
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

from .ats_score import ATSScoreCalculator


class SectionMatcher:
    """Analyze section-level matching between resume and JD"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two text sections"""
        if not text1 or not text2:
            return 0.0
        
        embeddings = self.model.encode([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return float(similarity)
    
    def analyze_soft_skills(
        self, 
        resume_sections: Dict[str, str], 
        jd_text: str
    ) -> str:
        """
        Analyze soft skills match
        Universal across all domains
        """
        soft_skills_keywords = [
            'leadership', 'teamwork', 'communication', 'problem-solving',
            'collaboration', 'management', 'organized', 'creative',
            'analytical', 'detail-oriented', 'motivated', 'reliable',
            'adaptable', 'innovative', 'strategic', 'efficient'
        ]
        
        resume_lower = ' '.join(resume_sections.values()).lower()
        jd_lower = jd_text.lower()
        
        # Check which soft skills are required
        required_soft_skills = [
            skill for skill in soft_skills_keywords 
            if skill in jd_lower
        ]
        
        if not required_soft_skills:
            return "Not Required"
        
        # Check which are found in resume
        found_soft_skills = [
            skill for skill in required_soft_skills 
            if skill in resume_lower
        ]
        
        # Calculate match ratio
        match_ratio = len(found_soft_skills) / len(required_soft_skills)
        
        if match_ratio >= 0.5:
            return "Strongly Matched"
        elif match_ratio >= 0.25:
            return "Partially Matched"
        else:
            return "Not Matched"
    
    def analyze_section_match(
        self, 
        resume_text: str, 
        jd_text: str
    ) -> Dict[str, str]:
        """
        Analyze how well each section matches the JD
        Returns match status for each section
        """
        # Identify sections
        resume_sections = ATSScoreCalculator.identify_sections(resume_text)
        
        section_analysis = {}
        key_sections = ['education', 'certifications', 'skills', 'experience']
        
        for section_name in key_sections:
            section_text = resume_sections.get(section_name, '')
            
            # Check if section exists
            if not section_text or len(section_text) < 10:
                section_analysis[section_name] = "Not Matched"
                continue
            
            # Calculate similarity
            similarity = self.calculate_semantic_similarity(section_text, jd_text)
            
            # Determine match level
            if similarity > 0.5:
                section_analysis[section_name] = "Strongly Matched"
            elif similarity > 0.25:
                section_analysis[section_name] = "Partially Matched"
            else:
                section_analysis[section_name] = "Not Matched"
        
        # Analyze soft skills separately
        section_analysis['soft_skills'] = self.analyze_soft_skills(
            resume_sections, 
            jd_text
        )
        
        return section_analysis