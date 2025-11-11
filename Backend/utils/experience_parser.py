"""
Experience Parser
Extract years of experience from text
"""

import re
from typing import Optional


class ExperienceParser:
    """Parse and extract years of experience"""
    
    @staticmethod
    def extract_experience_years(text: str) -> int:
        """
        Extract years of experience from text
        Handles multiple formats and date ranges
        """
        years = []
        
        # Pattern 1: Explicit years mentioned
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        if years:
            return max(years)
        
        # Pattern 2: Calculate from date ranges
        total_exp = ExperienceParser._calculate_from_date_ranges(text)
        if total_exp > 0:
            return total_exp
        
        return 0
    
    @staticmethod
    def _calculate_from_date_ranges(text: str) -> int:
        """
        Calculate experience from date ranges like:
        - 2020 - 2023
        - Jan 2020 - Present
        """
        # Find date ranges (YYYY - YYYY or YYYY - Present)
        date_ranges = re.findall(
            r'(\d{4})\s*[-–—]\s*(?:(\d{4})|present|current)', 
            text.lower()
        )
        
        if not date_ranges:
            return 0
        
        total_exp = 0
        current_year = 2025  # Update as needed
        
        for start, end in date_ranges:
            start_year = int(start)
            end_year = int(end) if end else current_year
            
            # Validate reasonable range
            if 1980 <= start_year <= current_year and start_year <= end_year <= current_year:
                total_exp += (end_year - start_year)
        
        return max(total_exp, 0)
    
    @staticmethod
    def calculate_experience_match(
        required_years: int, 
        candidate_years: int
    ) -> float:
        """
        Calculate experience match percentage
        Returns score from 0-100
        """
        if required_years == 0:
            return 100.0
        
        # Entry-level positions (<=2 years required)
        if required_years <= 2 and candidate_years > 0:
            return 100.0
        
        # Candidate has no experience but job requires <=2
        if candidate_years == 0 and required_years <= 2:
            return 60.0
        
        # Calculate ratio (capped at 100%)
        ratio = (candidate_years / required_years) * 100
        return min(ratio, 100.0)