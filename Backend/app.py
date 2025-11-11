"""
Main Flask Application - Entry Point
Handles API endpoints and request routing
"""

from flask import Flask, request, jsonify
from pathlib import Path
import sys

# Add backend to path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from services.matcher_service import MatcherService
from utils.file_utils import FileUtils
from instance.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
file_utils = FileUtils()
matcher_service = MatcherService()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ATS Resume Matcher API",
        "version": "1.0.0"
    })


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Main endpoint for resume analysis
    Accepts either file paths or uploaded files
    """
    try:
        # Option 1: Using file paths from assets/
        if request.json and 'use_assets' in request.json:
            # Use default files from assets
            assets_dir = Path(app.config['ASSETS_DIR'])
            
            # Find resume file
            resume_path = None
            for ext in ['.pdf', '.txt']:
                candidate = assets_dir / f"resume{ext}"
                if candidate.exists():
                    resume_path = str(candidate)
                    break
            
            jd_path = str(assets_dir / "job.txt")
            
            if not resume_path or not Path(jd_path).exists():
                return jsonify({
                    "error": "Resume or job description not found in assets/"
                }), 404
            
            # Extract text
            resume_text = file_utils.read_file(resume_path)
            jd_text = file_utils.read_file(jd_path)
        
        # Option 2: File upload (for future enhancement)
        elif 'resume' in request.files and 'job_description' in request.files:
            resume_file = request.files['resume']
            jd_file = request.files['job_description']
            
            # Save temporarily and read
            resume_path = Path(app.config['UPLOAD_FOLDER']) / resume_file.filename
            jd_path = Path(app.config['UPLOAD_FOLDER']) / jd_file.filename
            
            resume_file.save(resume_path)
            jd_file.save(jd_path)
            
            resume_text = file_utils.read_file(str(resume_path))
            jd_text = file_utils.read_file(str(jd_path))
        
        else:
            return jsonify({
                "error": "Please provide either 'use_assets': true or upload files"
            }), 400
        
        # Validate text extraction
        if not resume_text or not jd_text:
            return jsonify({
                "error": "Failed to extract text from files"
            }), 400
        
        # Run analysis
        results = matcher_service.analyze(resume_text, jd_text)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


@app.route('/analyze/quick', methods=['POST'])
def quick_analyze():
    """
    Quick analysis endpoint for testing
    Uses files from assets/ directory
    """
    try:
        results = matcher_service.analyze_from_assets()
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


if __name__ == '__main__':
    # Create necessary directories
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )