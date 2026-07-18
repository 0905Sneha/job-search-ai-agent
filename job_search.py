import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

def search_jobs(query, location="Pune", experience=None, salary_min=None, num_results=20):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": num_results,
        "content-type": "application/json"
    }
    if salary_min:
        params["salary_min"] = salary_min

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": f"API error: {response.status_code} - {response.text[:300]}", "jobs": []}

    data = response.json()
    raw_jobs = data.get("results", [])

    jobs = []
    for job in raw_jobs:
        jobs.append({
            "title": job.get("title", "N/A"),
            "company": job.get("company", {}).get("display_name", "N/A"),
            "location": job.get("location", {}).get("display_name", "N/A"),
            "salary": format_salary(job),
            "link": job.get("redirect_url", "#"),
            "description": (job.get("description") or "")[:300]
        })

    return {"error": None, "jobs": jobs}


def format_salary(job):
    min_sal = job.get("salary_min")
    max_sal = job.get("salary_max")
    if min_sal and max_sal:
        return f"₹{int(min_sal):,} - ₹{int(max_sal):,}"
    return "Not disclosed"