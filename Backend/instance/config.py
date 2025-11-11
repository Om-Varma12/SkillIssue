"""
Configuration Settings
Stores all environment variables and constants
"""

from pathlib import Path

class Config:
    """Base configuration"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent  # SkillIssue/
    ASSETS_DIR = BASE_DIR / "assets"
    UPLOAD_FOLDER = BASE_DIR / "backend" / "uploads"
    MODELS_DIR = BASE_DIR / "backend" / "models"
    
    # API Configuration
    DEBUG = True
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # HuggingFace Token (for embeddings)
    HF_TOKEN = "your_key_here"  # Optional - models work without token
    
    # Model Configuration
    SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Analysis Parameters
    TOP_KEYWORDS = 100
    SIMILARITY_THRESHOLD = 0.65
    TOP_HIGHLIGHTS = 5
    
    # Scoring Weights
    WEIGHTS = {
        'skills': 0.45,
        'semantic': 0.25,
        'ats': 0.20,
        'experience': 0.10
    }
    
    # ATS Score Thresholds
    ATS_THRESHOLDS = {
        'excellent': 70,
        'good': 55,
        'fair': 35
    }