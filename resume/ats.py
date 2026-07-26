def ats_score(parsed_resume):
    """
    Simple rule-based ATS-friendliness score out of 100.
    """
    score = 0
    issues = []

    if parsed_resume["email"]:
        score += 20
    else:
        issues.append("No email address detected — add one clearly in the header.")

    if parsed_resume["phone"]:
        score += 15
    else:
        issues.append("No phone number detected.")

    if parsed_resume["has_education"]:
        score += 15
    else:
        issues.append("Education section not clearly detected.")

    if parsed_resume["has_experience"]:
        score += 20
    else:
        issues.append("Experience/internship section not clearly detected.")

    if parsed_resume["has_projects"]:
        score += 15
    else:
        issues.append("Projects section not clearly detected — add one, especially as a fresher.")

    if len(parsed_resume["skills"]) >= 5:
        score += 15
    else:
        issues.append("Few recognizable technical skills found — list them explicitly (e.g., a 'Skills' section).")

    return {"score": score, "issues": issues}