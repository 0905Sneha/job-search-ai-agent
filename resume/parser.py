import re
from resume.utils import clean_text, extract_skills

def parse_resume(raw_text):
    text = clean_text(raw_text)

    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-\s]?)?\d{10}', text)

    skills = extract_skills(text)

    # crude section detection
    has_education = bool(re.search(r'\b(education|b\.?tech|degree|university|college)\b', text, re.I))
    has_experience = bool(re.search(r'\b(experience|internship|worked|employed)\b', text, re.I))
    has_projects = bool(re.search(r'\b(project|projects)\b', text, re.I))

    return {
        "email": email_match.group() if email_match else None,
        "phone": phone_match.group() if phone_match else None,
        "skills": skills,
        "has_education": has_education,
        "has_experience": has_experience,
        "has_projects": has_projects,
        "raw_text": text
    }