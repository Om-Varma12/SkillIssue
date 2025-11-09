def compute_ats_score(skill_sim: float, exp_ratio: float, matched_kw_count: int, total_jd_kw: int):
    """
    Build an ATS-like score out of 100 combining:
      - skill_sim (0-1) weighted 50%
      - exp_ratio (0-1) weighted 30%
      - keyword coverage (0-1) weighted 20%
    Returns (score, label)
    """
    keyword_cov = (matched_kw_count / total_jd_kw) if total_jd_kw > 0 else 0.0

    score = (skill_sim * 50.0) + (exp_ratio * 30.0) + (keyword_cov * 20.0)
    score = max(0.0, min(100.0, score))  # clamp

    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    else:
        label = "Poor"

    return round(score, 2), label
