def match_resume_to_job(resume_skills, job_description):
    job_desc_lower = job_description.lower()
    matched = [s for s in resume_skills if s in job_desc_lower]
    missing = [s for s in resume_skills if s not in job_desc_lower]

    match_percent = int((len(matched) / len(resume_skills)) * 100) if resume_skills else 0

    return {
        "match_percent": match_percent,
        "matched_skills": matched,
        "missing_from_job": missing
    }