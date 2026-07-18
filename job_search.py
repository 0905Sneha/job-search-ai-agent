import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

def search_jobs(query, location="India", experience=None, salary_min=None, num_pages=1):
    """
    Search jobs using JSearch API.
    query: e.g. "Python Developer", "Web Developer","Full Stack Developer","DevOps Engineer","Java Developer"
    location: e.g. "Pune", "Mumbai","Banglore","Hyderabad" "India"
    experience: e.g. "fresher", "1-3 years" (used as text filter, not a strict API param)
    salary_min: minimum salary in INR (used for post-filtering, JSearch doesn't filter by salary directly)
    """
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    search_query = f"{query} in {location}"
    params = {
        "query": search_query,
        "page": "1",
        "num_pages": str(num_pages),
        "country": "in"
    }

    response = requests.get(JSEARCH_URL, headers=headers, params=params)

    if response.status_code != 200:
        return {"error": f"API error: {response.status_code}", "jobs": []}

    data = response.json()
    raw_jobs = data.get("data", [])

    jobs = []
    for job in raw_jobs:
        cleaned = {
            "title": job.get("job_title", "N/A"),
            "company": job.get("employer_name", "N/A"),
            "location": job.get("job_city") or job.get("job_country", "N/A"),
            "salary": format_salary(job),
            "link": job.get("job_apply_link", "#"),
            "description": (job.get("job_description") or "")[:300]
        }
        jobs.append(cleaned)

    # basic salary post-filter if user specified a minimum
    if salary_min:
        jobs = [j for j in jobs if job_meets_salary(j, salary_min)]

    return {"error": None, "jobs": jobs}


def format_salary(job):
    min_sal = job.get("job_min_salary")
    max_sal = job.get("job_max_salary")
    if min_sal and max_sal:
        return f"{min_sal} - {max_sal} {job.get('job_salary_currency', '')}"
    return "Not disclosed"


def job_meets_salary(job, salary_min):
    # placeholder logic — refine once you see real API salary formats
    return True