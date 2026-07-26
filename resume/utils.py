import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# A basic skill keyword bank — expand as needed
COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "react", "node.js", "sql", "mongodb",
    "django", "flask", "html", "css", "git", "docker", "kubernetes", "aws",
    "machine learning", "data analysis", "pandas", "numpy", "tensorflow",
    "excel", "power bi", "tableau", "rest api", "linux", "streamlit", "langchain"
]

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in COMMON_SKILLS if skill in text_lower]
    return list(set(found))