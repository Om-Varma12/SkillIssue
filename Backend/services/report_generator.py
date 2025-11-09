def build_report(
    skill_match,
    experience_match,
    matched_keywords,
    missing_keywords,
    exp_required,
    exp_resume,
    relevant_experience_highlights,
    ats_score,
    ats_label,
    top_resume_keywords,
    section_analysis,
    overall_percent
):
    """
    Standardize the JSON response structure.
    """
    return {
        "skill_match_score_percent": skill_match,
        "experience_match_score_percent": experience_match,
        "keywords": {
            "matched": matched_keywords,
            "missing": missing_keywords
        },
        "experience": {
            "required_years": exp_required,
            "candidate_years": exp_resume
        },
        "relevant_experience_highlights": relevant_experience_highlights,
        "ats": {
            "score_percent": ats_score,
            "label": ats_label
        },
        "top_resume_keywords": top_resume_keywords,
        "section_match_analysis": section_analysis,
        "overall_match_percent": overall_percent
    }
