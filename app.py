import streamlit as st
from job_search import search_jobs

st.set_page_config(page_title="AI Job Search Assistant", layout="wide")
st.title("🔍 AI-Powered Job Search Assistant")

# Sidebar filters
st.sidebar.header("Filters")
location = st.sidebar.text_input("Location", "Pune","Mumbia","Banglore","Hyderabad")
experience = st.sidebar.selectbox("Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
salary_min = st.sidebar.number_input("Minimum Salary (LPA)", min_value=0, value=0)

# Main chat-style input
query = st.text_input("What job are you looking for?", "Python Developer","Web Developer","Full Stack Developer","DevOps Engineer","Java Developer")

if st.button("Search Jobs"):
    with st.spinner("Searching..."):
        result = search_jobs(query, location=location, experience=experience, salary_min=salary_min)

    if result["error"]:
        st.error(result["error"])
    elif not result["jobs"]:
        st.warning("No jobs found. Try different filters.")
    else:
        st.success(f"Found {len(result['jobs'])} jobs")
        for job in result["jobs"]:
            with st.container():
                st.subheader(job["title"])
                st.write(f"**{job['company']}** — {job['location']}")
                st.write(f"💰 {job['salary']}")
                st.write(job["description"] + "...")
                st.markdown(f"[Apply here]({job['link']})")
                st.divider()