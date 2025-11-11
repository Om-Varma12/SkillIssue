"""
Matcher Service - Main Orchestrator
Coordinates all analysis operations
"""

import sys
from pathlib import Path
from typing import Dict

# Add utils to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from utils.file_utils import FileUtils
from utils.text_preprocessing import TextPreprocessor
from utils.keyword_extraction import KeywordExtractor
from utils.experience_parser import ExperienceParser
from utils.similarity import SimilarityCalculator
from utils.ats_score import ATSScoreCalculator
from utils.section_matcher import SectionMatcher
from instance.config import Config


class MatcherService:
    """
    Main service that orchestrates the entire analysis
    This is the 'project manager' that coordinates all modules
    """
    
    def __init__(self):
        # Initialize all components
        self.file_utils = FileUtils()
        self.preprocessor = TextPreprocessor()
        self.keyword_extractor = KeywordExtractor(Config.SENTENCE_MODEL)
        self.experience_parser = ExperienceParser()
        self.similarity_calculator = SimilarityCalculator(Config.SENTENCE_MODEL)
        self.ats_calculator = ATSScoreCalculator()
        self.section_matcher = SectionMatcher(Config.SENTENCE_MODEL)
    
    def analyze(self, resume_text: str, jd_text: str) -> Dict:
        """
        Main analysis function - coordinates all operations
        
        Args:
            resume_text: Raw resume text
            jd_text: Raw job description text
        
        Returns:
            Complete analysis results dictionary
        """
        # 1. Clean texts
        resume_text = self.preprocessor.clean_text(resume_text)
        jd_text = self.preprocessor.clean_text(jd_text)
        
        # 2. Extract keywords and technical terms
        jd_terms = self.keyword_extractor.extract_all_terms(
            jd_text, 
            Config.TOP_KEYWORDS
        )
        resume_terms = self.keyword_extractor.extract_all_terms(
            resume_text, 
            Config.TOP_KEYWORDS
        )
        
        # Convert to lists for processing
        all_jd_terms = list(jd_terms)
        all_resume_terms = list(resume_terms)
        
        # 3. Semantic keyword matching
        matched_keywords, missing_keywords = self.keyword_extractor.semantic_keyword_matching(
            all_resume_terms,
            all_jd_terms,
            threshold=Config.SIMILARITY_THRESHOLD
        )
        
        # 4. Calculate overall semantic similarity
        semantic_similarity = self.similarity_calculator.calculate_semantic_similarity(
            resume_text, 
            jd_text
        )
        
        # 5. Calculate skill match score
        total_jd_terms = len(all_jd_terms)
        if total_jd_terms > 0:
            keyword_match_ratio = len(matched_keywords) / total_jd_terms
            skill_match_score = (keyword_match_ratio * 0.5 + semantic_similarity * 0.5) * 100
        else:
            skill_match_score = 0.0
        
        # 6. Extract experience
        required_years = self.experience_parser.extract_experience_years(jd_text)
        candidate_years = self.experience_parser.extract_experience_years(resume_text)
        experience_match_score = self.experience_parser.calculate_experience_match(
            required_years, 
            candidate_years
        )
        
        # 7. Extract relevant highlights
        highlights = self.similarity_calculator.extract_relevant_highlights(
            resume_text, 
            jd_text, 
            Config.TOP_HIGHLIGHTS
        )
        
        # 8. Section analysis
        section_analysis = self.section_matcher.analyze_section_match(
            resume_text, 
            jd_text
        )
        
        # 9. Calculate ATS score
        ats_score, ats_label = self.ats_calculator.calculate_ats_score(
            resume_text,
            jd_text,
            matched_keywords,
            all_jd_terms,
            semantic_similarity
        )
        
        # 10. Prioritize keywords for display
        top_matched = self.keyword_extractor.prioritize_keywords(
            matched_keywords, 
            jd_text, 
            top_n=7
        )
        top_missing = self.keyword_extractor.prioritize_keywords(
            missing_keywords, 
            jd_text, 
            top_n=7
        )
        
        # 11. Get top resume keywords
        resume_keywords = self.keyword_extractor.extract_dynamic_keywords(
            resume_text, 
            top_n=20
        )
        
        # 12. Calculate overall match
        overall_match = (
            skill_match_score * Config.WEIGHTS['skills'] +
            semantic_similarity * 100 * Config.WEIGHTS['semantic'] +
            ats_score * Config.WEIGHTS['ats'] +
            experience_match_score * Config.WEIGHTS['experience']
        )
        
        # 13. Compile results
        results = {
            "skill_match_score_percent": round(skill_match_score, 2),
            "experience_match_score_percent": round(experience_match_score, 2),
            "keywords": {
                "matched": top_matched,
                "missing": top_missing
            },
            "experience": {
                "required_years": required_years,
                "candidate_years": candidate_years
            },
            "relevant_experience_highlights": highlights,
            "ats": {
                "score_percent": ats_score,
                "label": ats_label
            },
            "top_resume_keywords": resume_keywords,
            "section_match_analysis": section_analysis,
            "overall_match_percent": round(overall_match, 2)
        }
        
        return results
    
    def analyze_from_assets(self) -> Dict:
        """
        Convenience method to analyze files from assets directory
        Used for testing
        """
        assets_dir = Path(Config.ASSETS_DIR)
        
        # Find resume file
        resume_path = self.file_utils.find_resume_in_assets(assets_dir)
        if not resume_path:
            return {"error": "Resume file not found in assets/"}
        
        jd_path = assets_dir / "job.txt"
        if not jd_path.exists():
            return {"error": "Job description file not found in assets/"}
        
        # Read files
        resume_text = self.file_utils.read_file(str(resume_path))
        jd_text = self.file_utils.read_file(str(jd_path))
        
        if not resume_text or not jd_text:
            return {"error": "Failed to extract text from files"}
        
        # Run analysis
        return self.analyze(resume_text, jd_text)