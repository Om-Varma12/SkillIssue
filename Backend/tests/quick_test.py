"""
Universal ATS Resume Matcher - Domain Agnostic
Works for ANY profession: CS, Civil, Medical, Marketing, Design, etc.
Uses AI and NLP to extract and match skills dynamically
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
import requests
from collections import Counter

# PDF Processing
try:
    import pdfplumber
except ImportError:
    os.system('pip install pdfplumber')
    import pdfplumber

# NLP and ML
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
except ImportError:
    os.system('pip install sentence-transformers scikit-learn numpy')
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

# Configuration
HF_TOKEN = "your_key_here"
SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class UniversalATSMatcher:
    def __init__(self, hf_token: str):
        self.hf_token = hf_token
        self.sentence_model = SentenceTransformer(SENTENCE_MODEL)
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return ""
    
    def read_text_file(self, file_path: str) -> str:
        """Read text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text
        except Exception as e:
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\+\#\.\,\(\)/]', ' ', text)
        return text.strip()
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """Extract potential skill phrases using linguistic patterns"""
        # Pattern 1: Capitalized multi-word terms (e.g., "Machine Learning", "AutoCAD")
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        
        # Pattern 2: Technical acronyms (e.g., "AI", "ML", "CAD", "BIM")
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        
        # Pattern 3: Hyphenated terms (e.g., "full-stack", "on-site")
        hyphenated = re.findall(r'\b\w+(?:-\w+)+\b', text)
        
        # Pattern 4: Common skill patterns
        skill_patterns = [
            r'\b\w+(?:\s+\w+){0,2}\s+(?:skills?|experience|knowledge|proficiency)\b',
            r'\b(?:expert|proficient|experienced)\s+(?:in|with)\s+\w+(?:\s+\w+){0,2}\b',
        ]
        
        skill_mentions = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skill_mentions.extend(matches)
        
        all_phrases = capitalized + acronyms + hyphenated + skill_mentions
        return [phrase.strip() for phrase in all_phrases if len(phrase.strip()) > 2]
    
    def extract_dynamic_keywords(self, text: str, top_n: int = 100) -> List[str]:
        """Extract keywords dynamically using TF-IDF (no predefined list)"""
        # Comprehensive stop words
        stop_words = {
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
        
        # Extract words and phrases
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        two_grams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        three_grams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
        
        # Combine all
        all_terms = words + two_grams + three_grams
        
        # Filter stop words and short terms
        filtered_terms = [
            term for term in all_terms 
            if not any(stop in term.split() for stop in stop_words) and len(term) > 2
        ]
        
        # Get frequency
        term_freq = Counter(filtered_terms)
        
        # Return top keywords
        return [term for term, _ in term_freq.most_common(top_n)]
    
    def extract_technical_terms(self, text: str) -> Set[str]:
        """Extract technical terms using multiple strategies"""
        terms = set()
        
        # Strategy 1: Noun phrases and acronyms
        noun_phrases = self.extract_noun_phrases(text)
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
            # Extract key terms from bullet points
            words = re.findall(r'\b[A-Za-z][\w\-\.]+\b', line)
            terms.update([w.lower() for w in words if len(w) > 3])
        
        return terms
    
    def semantic_keyword_matching(self, resume_keywords: List[str], jd_keywords: List[str], 
                                  threshold: float = 0.7) -> Tuple[List[str], List[str]]:
        """Match keywords using semantic similarity (AI-powered)"""
        if not resume_keywords or not jd_keywords:
            return [], jd_keywords
        
        # Get embeddings for all keywords
        resume_embeddings = self.sentence_model.encode(resume_keywords)
        jd_embeddings = self.sentence_model.encode(jd_keywords)
        
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
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        # Pattern 1: Explicit years mentioned
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        if years:
            return max(years)
        
        # Pattern 2: Calculate from date ranges (YYYY - YYYY or YYYY - Present)
        date_ranges = re.findall(r'(\d{4})\s*[-–—]\s*(?:(\d{4})|present|current)', text.lower())
        
        if date_ranges:
            total_exp = 0
            current_year = 2025  # Update this as needed
            
            for start, end in date_ranges:
                start_year = int(start)
                end_year = int(end) if end else current_year
                total_exp += (end_year - start_year)
            
            return max(total_exp, 0)
        
        return 0
    
    def identify_sections(self, text: str) -> Dict[str, str]:
        """Identify different sections in resume"""
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'certifications': '',
            'summary': ''
        }
        
        # Universal section patterns (works across all domains)
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
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        embeddings = self.sentence_model.encode([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    
    def extract_relevant_highlights(self, resume_text: str, jd_text: str, top_n: int = 5) -> List[str]:
        """Extract most relevant sentences from resume based on JD"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', resume_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return []
        
        # Get JD embedding
        jd_embedding = self.sentence_model.encode([jd_text])[0]
        
        # Calculate similarity for each sentence
        sentence_scores = []
        for sentence in sentences:
            sent_embedding = self.sentence_model.encode([sentence])[0]
            similarity = cosine_similarity([sent_embedding], [jd_embedding])[0][0]
            
            # Boost score if contains numbers (achievements/metrics)
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
    
    def analyze_section_match(self, resume_sections: Dict[str, str], jd_text: str) -> Dict[str, str]:
        """Analyze how well each section matches the JD"""
        section_analysis = {}
        
        key_sections = ['education', 'certifications', 'skills', 'experience']
        
        for section_name in key_sections:
            section_text = resume_sections.get(section_name, '')
            
            if not section_text or len(section_text) < 10:
                section_analysis[section_name] = "Not Matched"
                continue
            
            # Calculate similarity
            similarity = self.calculate_semantic_similarity(section_text, jd_text)
            
            if similarity > 0.5:
                section_analysis[section_name] = "Strongly Matched"
            elif similarity > 0.25:
                section_analysis[section_name] = "Partially Matched"
            else:
                section_analysis[section_name] = "Not Matched"
        
        # Soft skills analysis (universal)
        soft_skills_keywords = [
            'leadership', 'teamwork', 'communication', 'problem-solving', 
            'collaboration', 'management', 'organized', 'creative',
            'analytical', 'detail-oriented', 'motivated', 'reliable'
        ]
        
        resume_lower = ' '.join(resume_sections.values()).lower()
        jd_lower = jd_text.lower()
        
        # Check which soft skills are required
        required_soft_skills = [skill for skill in soft_skills_keywords if skill in jd_lower]
        found_soft_skills = [skill for skill in required_soft_skills if skill in resume_lower]
        
        if not required_soft_skills:
            section_analysis['soft_skills'] = "Not Required"
        elif len(found_soft_skills) / len(required_soft_skills) >= 0.5:
            section_analysis['soft_skills'] = "Strongly Matched"
        else:
            section_analysis['soft_skills'] = "Not Matched"
        
        return section_analysis
    
    def calculate_ats_score(self, resume_text: str, jd_text: str, 
                           matched_keywords: List[str], jd_keywords: List[str],
                           semantic_similarity: float) -> Tuple[float, str]:
        """Calculate ATS compatibility score"""
        score = 0.0
        
        # 1. Keyword Match (25 points) - Reduced weight
        if jd_keywords:
            keyword_ratio = len(matched_keywords) / len(jd_keywords)
            score += keyword_ratio * 25
        
        # 2. Semantic Similarity (35 points) - INCREASED! Most important
        score += semantic_similarity * 35
        
        # 3. Section Completeness (15 points)
        sections = self.identify_sections(resume_text)
        required_sections = ['education', 'experience', 'skills']
        sections_found = sum(1 for sec in required_sections if sections[sec].strip())
        score += (sections_found / len(required_sections)) * 15
        
        # 4. Contact Information (10 points)
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score += 5
        if re.search(r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', resume_text):
            score += 5
        
        # 5. Formatting Quality (10 points)
        if len(resume_text) > 500:
            score += 5
        if len(resume_text.split('\n')) > 10:
            score += 5
        
        # 6. Contextual Matching (5 points)
        jd_important_phrases = re.findall(r'\b\w+\s+\w+\s+\w+\b', jd_text.lower())[:15]
        resume_lower = resume_text.lower()
        phrase_matches = sum(1 for phrase in jd_important_phrases if phrase in resume_lower)
        score += (phrase_matches / max(len(jd_important_phrases), 1)) * 5
        
        # Determine label with adjusted thresholds
        if score >= 70:
            label = "Excellent"
        elif score >= 55:
            label = "Good"
        elif score >= 35:
            label = "Fair"
        else:
            label = "Poor"
        
        return round(score, 2), label
    
    def analyze(self, resume_path: str, jd_path: str) -> Dict:
        """Main analysis function - Universal for all domains"""
        
        # Load documents
        if resume_path.endswith('.pdf'):
            resume_text = self.extract_text_from_pdf(resume_path)
        else:
            resume_text = self.read_text_file(resume_path)
        
        jd_text = self.read_text_file(jd_path)
        
        if not resume_text or not jd_text:
            return {"error": "Failed to load documents"}
        
        # Clean texts
        resume_text = self.clean_text(resume_text)
        jd_text = self.clean_text(jd_text)
        
        # Extract keywords dynamically
        jd_keywords = self.extract_dynamic_keywords(jd_text, top_n=100)
        jd_technical_terms = self.extract_technical_terms(jd_text)
        
        resume_keywords = self.extract_dynamic_keywords(resume_text, top_n=100)
        resume_technical_terms = self.extract_technical_terms(resume_text)
        
        # Combine keywords and technical terms
        all_jd_terms = list(set(jd_keywords) | jd_technical_terms)
        all_resume_terms = list(set(resume_keywords) | resume_technical_terms)
        
        # Use semantic matching
        matched_keywords, missing_keywords = self.semantic_keyword_matching(
            all_resume_terms, all_jd_terms, threshold=0.65
        )
        
        # Calculate overall semantic similarity
        semantic_similarity = self.calculate_semantic_similarity(resume_text, jd_text)
        
        # Calculate skill match score
        total_jd_terms = len(all_jd_terms)
        if total_jd_terms > 0:
            keyword_match_ratio = len(matched_keywords) / total_jd_terms
            skill_match_score = (keyword_match_ratio * 0.5 + semantic_similarity * 0.5) * 100
        else:
            skill_match_score = 0.0
        
        # Extract experience
        required_years = self.extract_experience_years(jd_text)
        candidate_years = self.extract_experience_years(resume_text)
        
        # Calculate experience match
        if required_years == 0:
            experience_match_score = 100.0
        elif required_years <= 2 and candidate_years > 0:
            experience_match_score = 100.0
        elif candidate_years == 0 and required_years <= 2:
            experience_match_score = 60.0
        else:
            experience_match_score = min((candidate_years / required_years) * 100, 100.0)
        
        # Identify sections
        resume_sections = self.identify_sections(resume_text)
        
        # Extract relevant highlights
        highlights = self.extract_relevant_highlights(resume_text, jd_text, top_n=5)
        
        # Section analysis
        section_analysis = self.analyze_section_match(resume_sections, jd_text)
        
        # Calculate ATS score
        ats_score, ats_label = self.calculate_ats_score(
            resume_text, jd_text, matched_keywords, all_jd_terms, semantic_similarity
        )
        
        # Calculate overall match with optimized weights
        overall_match = (
            skill_match_score * 0.45 +
            semantic_similarity * 100 * 0.25 +
            ats_score * 0.20 +
            experience_match_score * 0.10
        )
        
        # Get top resume keywords for display
        top_resume_keywords = resume_keywords[:20]
        
        # Prioritize most important matched and missing keywords
        # For matched: prioritize by frequency in both documents
        matched_importance = []
        for kw in matched_keywords:
            resume_count = resume_text.lower().count(kw.lower())
            jd_count = jd_text.lower().count(kw.lower())
            importance = resume_count + jd_count * 2  # JD mentions are more important
            matched_importance.append((kw, importance))
        
        matched_importance.sort(key=lambda x: x[1], reverse=True)
        top_matched = [kw for kw, _ in matched_importance[:7]]
        
        # For missing: prioritize by frequency in JD
        missing_importance = []
        for kw in missing_keywords:
            jd_count = jd_text.lower().count(kw.lower())
            missing_importance.append((kw, jd_count))
        
        missing_importance.sort(key=lambda x: x[1], reverse=True)
        top_missing = [kw for kw, _ in missing_importance[:7]]
        
        # Compile results
        results = {
            "skill_match_score_percent": round(skill_match_score, 2),
            "experience_match_score_percent": round(experience_match_score, 2),
            "keywords": {
                "matched": top_matched,  # Only top 7
                "missing": top_missing   # Only top 7
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
            "top_resume_keywords": top_resume_keywords,
            "section_match_analysis": section_analysis,
            "overall_match_percent": round(overall_match, 2)
        }
        
        return results


def main():
    """Main execution function"""
    # Initialize matcher
    matcher = UniversalATSMatcher(HF_TOKEN)
    
    # Define paths - find the project root
    current_file = Path(__file__).resolve()
    
    # Navigate up to find the assets folder
    possible_roots = [
        current_file.parent,
        current_file.parent.parent,
        current_file.parent.parent.parent,
    ]
    
    assets_dir = None
    for root in possible_roots:
        candidate_assets = root / "assets"
        if candidate_assets.exists() and candidate_assets.is_dir():
            assets_dir = candidate_assets
            break
    
    if assets_dir is None:
        print(json.dumps({"error": "Assets folder not found"}))
        return
    
    # Try to find resume file
    resume_path = None
    for ext in ['.pdf', '.txt']:
        candidate_path = assets_dir / f"resume{ext}"
        if candidate_path.exists():
            resume_path = candidate_path
            break
    
    if resume_path is None:
        print(json.dumps({"error": "Resume file not found"}))
        return
    
    jd_path = assets_dir / "job.txt"
    
    if not jd_path.exists():
        print(json.dumps({"error": "Job description file not found"}))
        return
    
    # Run analysis
    results = matcher.analyze(str(resume_path), str(jd_path))
    
    # Print JSON output
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    return results


if __name__ == "__main__":
    main()