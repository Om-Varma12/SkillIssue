"""
Quick Test Script
Simple test to verify backend is working correctly
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Set environment variable to reduce TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from services.matcher_service import MatcherService
from instance.config import Config


def test_file_reading():
    """Test 1: Verify files can be read"""
    print("=" * 60)
    print("TEST 1: File Reading")
    print("=" * 60)
    
    from utils.file_utils import FileUtils
    file_utils = FileUtils()
    
    assets_dir = Path(Config.ASSETS_DIR)
    
    # Find resume
    resume_path = file_utils.find_resume_in_assets(assets_dir)
    if resume_path:
        print(f"✓ Resume found: {resume_path.name}")
        resume_text = file_utils.read_file(str(resume_path))
        print(f"✓ Resume text length: {len(resume_text)} characters")
    else:
        print("✗ Resume not found")
        return False
    
    # Find job description
    jd_path = assets_dir / "job.txt"
    if jd_path.exists():
        print(f"✓ Job description found: {jd_path.name}")
        jd_text = file_utils.read_file(str(jd_path))
        print(f"✓ JD text length: {len(jd_text)} characters")
    else:
        print("✗ Job description not found")
        return False
    
    print("\n✓ All files read successfully!\n")
    return True


def test_text_preprocessing():
    """Test 2: Verify text preprocessing works"""
    print("=" * 60)
    print("TEST 2: Text Preprocessing")
    print("=" * 60)
    
    from utils.text_preprocessing import TextPreprocessor
    preprocessor = TextPreprocessor()
    
    sample_text = "Machine Learning and Data Science skills with Python, TensorFlow"
    cleaned = preprocessor.clean_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Cleaned:  {cleaned}")
    
    technical_terms = preprocessor.extract_technical_terms(sample_text)
    print(f"Technical terms found: {list(technical_terms)[:5]}")
    
    print("\n✓ Text preprocessing working!\n")
    return True


def test_keyword_extraction():
    """Test 3: Verify keyword extraction works"""
    print("=" * 60)
    print("TEST 3: Keyword Extraction")
    print("=" * 60)
    
    from utils.keyword_extraction import KeywordExtractor
    extractor = KeywordExtractor()
    
    sample_text = """
    Required skills: Python, Machine Learning, Data Analysis
    Experience with TensorFlow and PyTorch
    Strong problem-solving and communication skills
    """
    
    keywords = extractor.extract_dynamic_keywords(sample_text, top_n=10)
    print(f"Keywords extracted: {keywords[:5]}")
    
    print("\n✓ Keyword extraction working!\n")
    return True


def test_full_analysis():
    """Test 4: Run complete analysis"""
    print("=" * 60)
    print("TEST 4: Full Analysis")
    print("=" * 60)
    
    matcher = MatcherService()
    
    print("Running analysis...")
    results = matcher.analyze_from_assets()
    
    if "error" in results:
        print(f"✗ Error: {results['error']}")
        return False
    
    # Display key results
    print(f"\n✓ Analysis completed successfully!")
    print(f"\n--- KEY METRICS ---")
    print(f"Overall Match:       {results['overall_match_percent']}%")
    print(f"Skill Match:         {results['skill_match_score_percent']}%")
    print(f"Experience Match:    {results['experience_match_score_percent']}%")
    print(f"ATS Score:           {results['ats']['score_percent']}% ({results['ats']['label']})")
    
    print(f"\n--- KEYWORDS ---")
    print(f"Matched ({len(results['keywords']['matched'])}): {results['keywords']['matched'][:3]}")
    print(f"Missing ({len(results['keywords']['missing'])}): {results['keywords']['missing'][:3]}")
    
    print(f"\n--- EXPERIENCE ---")
    print(f"Required: {results['experience']['required_years']} years")
    print(f"Candidate: {results['experience']['candidate_years']} years")
    
    print(f"\n--- SECTION ANALYSIS ---")
    for section, status in results['section_match_analysis'].items():
        print(f"{section.capitalize()}: {status}")
    
    print("\n✓ Full analysis working!\n")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("BACKEND QUICK TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_file_reading,
        test_text_preprocessing,
        test_keyword_extraction,
        test_full_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}\n")
            results.append(False)
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check errors above.")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()