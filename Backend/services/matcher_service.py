from utils.text_preprocessing import clean_text
from utils.keyword_extraction import get_keywords, compare_keywords
from utils.experience_parser import extract_experience_years
from utils.similarity import compute_cosine_similarity
from utils.ats_score import compute_ats_score
from utils.section_matcher import evaluate_sections
from services.report_generator import build_report

def process_resume_jobdesc(resume_text: str, jd_text: str):
    """
    Orchestrator: accepts raw resume_text and jd_text, returns structured JSON.
    """
    # 1. clean text for vectorizers
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    # 2. keywords
    resume_kw = get_keywords(resume_clean, top_n=50)
    jd_kw = get_keywords(jd_clean, top_n=50)
    matched_kw, missing_kw = compare_keywords(resume_kw, jd_kw)

    # 3. similarity (semantic)
    skill_similarity = compute_cosine_similarity(resume_clean, jd_clean)  # 0..1

    # 4. experience
    exp_resume = extract_experience_years(resume_text)
    exp_jd = extract_experience_years(jd_text)
    # experience match ratio: if JD requires X years, resume has Y years => score min(Y/X,1)
    exp_ratio = (exp_resume / exp_jd) if (exp_jd and exp_resume) else (1.0 if (not exp_jd) else 0.0)
    exp_ratio = min(exp_ratio, 1.0)

    # 5. ATS score
    ats_score, ats_label = compute_ats_score(skill_similarity, exp_ratio, len(matched_kw), len(jd_kw))

    # 6. top resume keywords (sorted by lexical order, limited)
    top_resume_keywords = sorted(list(resume_kw))[:20]

    # 7. section matches
    section_analysis = evaluate_sections(resume_text, jd_text)

    # 8. overall match percent: weighted blend (example)
    overall_percent = round((skill_similarity * 0.6 + exp_ratio * 0.25 + (ats_score/100) * 0.15) * 100, 2)

    # 9. relevant experience highlights (simple heuristic: sentences containing years/keywords)
    relevant_highlights = []
    for line in resume_text.splitlines():
        low = line.lower()
        if any(k in low for k in ["year", "yrs", "experience", "worked", "project", "lead"]):
            relevant_highlights.append(line.strip())
    relevant_highlights = relevant_highlights[:10]

    # 10. build final report
    report = build_report(
        skill_match=round(skill_similarity * 100, 2),
        experience_match=round(exp_ratio * 100, 2),
        matched_keywords=matched_kw,
        missing_keywords=missing_kw,
        exp_required=exp_jd,
        exp_resume=exp_resume,
        relevant_experience_highlights=relevant_highlights,
        ats_score=ats_score,
        ats_label=ats_label,
        top_resume_keywords=top_resume_keywords,
        section_analysis=section_analysis,
        overall_percent=overall_percent
    )

    return report
