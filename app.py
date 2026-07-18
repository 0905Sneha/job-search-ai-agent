import streamlit as st
from job_search import search_jobs
from style import apply_custom_style

st.set_page_config(page_title="AI Job Search Assistant", page_icon="🔍", layout="wide")
apply_custom_style()

st.title("🔍 AI-Powered Job Search Assistant")
st.caption("Find real, live job listings across India — matched to your filters.")

st.sidebar.header("🎯 Filters")
location = st.sidebar.selectbox("📍 Location", ["Pune", "Mumbai", "Bangalore", "Hyderabad"])
experience = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
salary_min = st.sidebar.number_input("💰 Minimum Salary (LPA)", min_value=0, value=0)

query = st.selectbox("What job are you looking for?",
                      ["Python Developer", "Web Developer", "Full Stack Developer", "DevOps Engineer", "Java Developer"])

if st.button("🔎 Search Jobs"):
    with st.spinner("Searching..."):
        result = search_jobs(query, location=location, experience=experience, salary_min=salary_min)

    if result["error"]:
        st.error(result["error"])
    elif not result["jobs"]:
        st.warning("No jobs found. Try different filters.")
    else:
        st.success(f"Found {len(result['jobs'])} jobs")
        for job in result["jobs"]:
            st.markdown(f"""
                <div class="job-card">
                    <h3>{job['title']}</h3>
                    <p><b>{job['company']}</b> — {job['location']}</p>
                    <p>💰 {job['salary']}</p>
                    <p>{job['description']}...</p>
                    <a href="{job['link']}" target="_blank">Apply here →</a>
                </div>
            """, unsafe_allow_html=True)