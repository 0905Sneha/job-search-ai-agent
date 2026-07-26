import streamlit as st
import requests
from job_search import search_jobs
from style import apply_custom_style

st.set_page_config(page_title="Company Insights", page_icon="🏢", layout="wide")
apply_custom_style()

st.title("🏢 Company Insights")
st.caption("See which companies are actively hiring right now.")

def get_company_overview(company_name):
    """Fetch a brief company description from Wikipedia, if available."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name.replace(' ', '_')}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", None)
    except Exception:
        pass
    return None

company_query = st.text_input("Enter a role to see hiring companies", "Python Developer")
location = st.selectbox("Location", ["Pune", "Mumbai", "Bangalore", "Hyderabad"])

if st.button("Find Hiring Companies"):
    with st.spinner("Fetching company data..."):
        result = search_jobs(company_query, location=location, num_results=30)

    if result["error"]:
        st.error(result["error"])
    else:
        companies = {}
        for job in result["jobs"]:
            name = job["company"]
            companies[name] = companies.get(name, 0) + 1

        sorted_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)
        st.success(f"Found {len(sorted_companies)} companies hiring")

        for name, count in sorted_companies:
            badge = "Urgently Hiring" if count >= 3 else "Hiring"
            overview = get_company_overview(name)
            google_link = f"https://www.google.com/search?q={name.replace(' ', '+')}+company"
            linkedin_link = f"https://www.linkedin.com/company/{name.replace(' ', '-').lower()}"

            st.markdown(f"""
                <div class="job-card">
                    <h4>{name}</h4>
                    <p>{badge} — {count} open role(s) found</p>
                    <p>{overview if overview else "The company overview is not available here. Please take a moment to search for the company on Google or view its LinkedIn profile.."}</p>
                    <p>
                        <a href="{google_link}" target="_blank"> Search on Google</a> &nbsp;|&nbsp;
                        <a href="{linkedin_link}" target="_blank"> View on LinkedIn</a>
                    </p>
                </div>
            """, unsafe_allow_html=True)