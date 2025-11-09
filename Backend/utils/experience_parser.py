import re

def extract_experience_years(text: str) -> int:
    """
    Heuristic extractor:
      - finds patterns like '3 years', '5+ yrs', '2 years of experience', 'experience: 4'
      - returns the maximum number found (or 0 if none)
    """
    if not text:
        return 0
    txt = text.lower()
    # common patterns
    # find numbers followed by 'year' or 'yrs'
    matches = re.findall(r'(\d+)\s*\+?\s*(?:years|year|yrs|yr)', txt)
    nums = [int(m) for m in matches] if matches else []
    # also look for 'experience: 3' like patterns
    matches2 = re.findall(r'experience[:\s]+(\d+)', txt)
    nums += [int(m) for m in matches2] if matches2 else []
    return max(nums) if nums else 0
