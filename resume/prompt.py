RESUME_ANALYSIS_PROMPT = """
You are an expert ATS recruiter and career coach.

Analyze the following resume.

Return ONLY valid JSON.

{
  "ats_score": number,
  "recommended_roles": [],
  "strengths": [],
  "missing_skills": [],
  "suggestions": []
}

Scoring Criteria:

- Resume Structure
- Contact Information
- Skills
- Projects
- Experience
- Education
- ATS Compatibility
- Industry Readiness

If information is missing, explain why.

Resume:

{resume_text}
"""