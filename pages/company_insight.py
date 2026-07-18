import streamlit as st
from job_search import search_jobs
from style import apply_custom_style

st.set_page_config(page_title="Company Insights", page_icon="🏢", layout="wide")
apply_custom_style()

st.title("Company Insights")
st.caption("See which companies are actively hiring right now.")

company_query = st.text_input("Enter a role to see hiring companies", "Python Developer")
location = st.selectbox("Location", ["Pune", "Mumbai", "Bangalore", "Hyderabad"])

if st.button("🔍 Find Hiring Companies"):
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
            badge = "🔥 Urgently Hiring" if count >= 3 else "Hiring"
            st.markdown(f"""
                <div class="job-card">
                    <h4>{name}</h4>
                    <p>{badge} — {count} open role(s) found</p>
                </div>
            """, unsafe_allow_html=True)