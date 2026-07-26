import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

JOOBLE_KEY = os.getenv("JOOBLE_API_KEY")


def format_salary(job):
    min_sal = job.get("salary_min")
    max_sal = job.get("salary_max")
    if min_sal and max_sal:
        return f"₹{int(min_sal):,} - ₹{int(max_sal):,}"
    return "Not disclosed"


def search_jobs_adzuna(query, location="Pune", salary_min=None, num_results=20):
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

    try:
        response = requests.get(BASE_URL, params=params, timeout=8)
        if response.status_code != 200:
            return []
        data = response.json()
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "salary": format_salary(job),
                "link": job.get("redirect_url", "#"),
                "description": (job.get("description") or "")[:300]
            })
        return jobs
    except Exception as e:
        print("Adzuna error:", e)
        return []


def search_jobs_jooble(query, location="Pune", num_results=20):
    print("JOOBLE_KEY:", JOOBLE_KEY)
    if not JOOBLE_KEY:
        return []
    url = f"https://jooble.org/api/{JOOBLE_KEY}"
    payload = {"keywords": query, "location": location}
    try:
        response = requests.post(url, json=payload, timeout=8)
        print("Jooble status code:", response.status_code)
        print("Jooble response text:", response.text[:500])
        if response.status_code != 200:
            return []
        data = response.json()
        jobs = []
        for job in data.get("jobs", [])[:num_results]:
            jobs.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "N/A"),
                "salary": job.get("salary") or "Not disclosed",
                "link": job.get("link", "#"),
                "description": (job.get("snippet") or "")[:300]
            })
        return jobs
    except Exception as e:
        print("Jooble error:", e)
        return []


def search_jobs(query, location="Pune", experience=None, salary_min=None, num_results=20):
    adzuna_jobs = search_jobs_adzuna(query, location=location, salary_min=salary_min, num_results=num_results)
    jooble_jobs = search_jobs_jooble(query, location=location, num_results=num_results)

    combined = adzuna_jobs + jooble_jobs

    seen = set()
    unique_jobs = []
    for job in combined:
        key = (job["title"].strip().lower(), job["company"].strip().lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    if not unique_jobs:
        return {"error": "No jobs found from either source. Check your API keys.", "jobs": []}

    return {"error": None, "jobs": unique_jobs}