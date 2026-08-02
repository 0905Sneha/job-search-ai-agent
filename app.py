import streamlit as st
from job_search import search_jobs
from style import apply_custom_style

st.set_page_config(page_title="AI Job Search Assistant", page_icon="🔍", layout="wide")
apply_custom_style()

# Hero section
st.markdown("""
    <div class="hero">
        <div class="hero-badge">🇮🇳 Live Indian Job Listings</div>
        <h1>🔍 AI-Powered Job Search Assistant</h1>
        <p class="subtext">Find real jobs across India, matched to exactly what you're looking for.</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("🎯 Filters")
location = st.sidebar.selectbox("Location", ["Pune", "Mumbai", "Bangalore", "Hyderabad"])
experience = st.sidebar.selectbox(" Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
work_mode = st.sidebar.selectbox(" Work Mode", ["Any", "Remote", "On-site", "Hybrid"])
salary_min = st.sidebar.number_input(" Minimum Salary (LPA)", min_value=0, value=0)

col_a, col_b = st.columns([3, 1])
with col_a:
    query = st.selectbox("What job are you looking for?",
                          ["Python Developer", "Web Developer", "Full Stack Developer", "DevOps Engineer", "Java Developer"])
with col_b:
    st.write("")
    st.write("")
    search_clicked = st.button("Search Jobs", use_container_width=True)

if search_clicked:
    with st.spinner("Searching across sources..."):
        search_query = query if work_mode == "Any" else f"{query} {work_mode}"
        result = search_jobs(search_query, location=location, experience=experience, salary_min=salary_min)

    if result["error"]:
        st.error(result["error"])
    elif not result["jobs"]:
        st.warning("No jobs found. Try different filters.")
    else:
        jobs = result["jobs"]
        if work_mode != "Any":
            jobs = [j for j in jobs if work_mode.lower() in j["description"].lower() or work_mode.lower() in j["title"].lower()] or jobs

        # Stats row
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f'<div class="stat-box"><div class="stat-number">{len(jobs)}</div><div class="stat-label">Jobs Found</div></div>', unsafe_allow_html=True)
        with s2:
            unique_companies = len(set(j["company"] for j in jobs))
            st.markdown(f'<div class="stat-box"><div class="stat-number">{unique_companies}</div><div class="stat-label">Companies</div></div>', unsafe_allow_html=True)
        with s3:
            st.markdown(f'<div class="stat-box"><div class="stat-number">{location}</div><div class="stat-label">Location</div></div>', unsafe_allow_html=True)

        st.write("")

        # Job cards in a 2-column grid
        cols = st.columns(2)
        for idx, job in enumerate(jobs):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="job-card">
                        <h4>{job['title']}</h4>
                        <div class="job-company">{job['company']}</div>
                        <div class="job-meta">{job['location']} &nbsp;|&nbsp; {job['salary']}</div>
                        <div class="job-desc">{job['description']}...</div>
                        <a href="{job['link']}" target="_blank">Apply here →</a>
                    </div>
                """, unsafe_allow_html=True)