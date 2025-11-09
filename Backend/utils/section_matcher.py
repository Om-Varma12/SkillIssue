def evaluate_sections(resume_text: str, jd_text: str):
    """
    Compare four high-level sections: education, certifications, soft skills, technical skills.
    Returns categorical match levels for each section.
    """
    resume = resume_text.lower() if resume_text else ""
    jd = jd_text.lower() if jd_text else ""

    sections = {
        "education": ["bachelor", "master", "b.tech", "b.e", "degree", "phd"],
        "certifications": ["certified", "certificate", "certification", "aws", "gcp", "azure", "cert"],
        "soft_skills": ["communication", "leadership", "teamwork", "problem solving", "collaboration", "adaptable"],
        "technical_skills": ["python", "sql", "docker", "aws", "tensorflow", "pytorch", "flask", "react", "ml", "ai"]
    }

    result = {}
    for section, keys in sections.items():
        resume_count = sum(1 for k in keys if k in resume)
        jd_count = sum(1 for k in keys if k in jd)
        ratio = (resume_count / jd_count) if jd_count > 0 else (1.0 if resume_count > 0 else 0.0)

        if ratio >= 0.7:
            level = "Strongly Matched"
        elif ratio >= 0.4:
            level = "Moderately Matched"
        elif ratio >= 0.1:
            level = "Poorly Matched"
        else:
            level = "Not Matched"

        result[section] = level

    return result
