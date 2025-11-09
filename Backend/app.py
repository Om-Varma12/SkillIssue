import os
from pathlib import Path
from flask import Flask, jsonify, request

from services.matcher_service import process_resume_jobdesc
from utils.file_utils import read_file_content

# create app
app = Flask(__name__)

# determine project root and assets path (assets is sibling to backend)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_PATH = PROJECT_ROOT / "assets"

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"status": "SkillIssue backend running", "assets_path": str(ASSETS_PATH)})

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Default behavior:
      - If no form data provided, will attempt to read:
            assets/resume.txt  and assets/job.txt
      - Or provide form data: resume_path and jd_path (relative or absolute)
    """
    try:
        # Decide which files to read
        resume_path = request.form.get("resume_path")
        jd_path = request.form.get("jd_path")

        if resume_path and jd_path:
            resume_file = Path(resume_path)
            jd_file = Path(jd_path)
        else:
            # default filenames in sibling assets folder
            resume_file = ASSETS_PATH / "resume.txt"
            jd_file = ASSETS_PATH / "job.txt"

        # Make sure files exist
        if not resume_file.exists():
            return jsonify({"error": f"Resume file not found: {resume_file}"}), 400
        if not jd_file.exists():
            return jsonify({"error": f"JD file not found: {jd_file}"}), 400

        resume_text = read_file_content(str(resume_file))
        jd_text = read_file_content(str(jd_file))

        result = process_resume_jobdesc(resume_text, jd_text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # run with debug for quick tests; set debug=False in production
    app.run(host="0.0.0.0", port=5000, debug=True)