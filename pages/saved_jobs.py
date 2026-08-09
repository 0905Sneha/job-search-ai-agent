import streamlit as st
from database import get_saved_jobs, update_status, delete_saved_job
from style import apply_custom_style

st.set_page_config(page_title="Saved Jobs", page_icon="💾", layout="wide")
apply_custom_style()

st.title("My Saved Jobs")
st.caption("Track jobs you've saved and update your application status.")

jobs = get_saved_jobs()

if not jobs:
    st.info("No saved jobs yet. Go to the job search page and save some!")
else:
    for job in jobs:
        job_id, title, company, location, salary, link, status, saved_at = job
        st.markdown(f"""
            <div class="job-card">
                <h4>{title}</h4>
                <div class="job-company">{company}</div>
                <div class="job-meta">{location} |  {salary} | Saved: {saved_at}</div>
                <a href="{link}" target="_blank">View job →</a>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_status = st.selectbox("Status", ["Saved", "Applied", "Interviewing", "Rejected", "Offer"],
                                       index=["Saved", "Applied", "Interviewing", "Rejected", "Offer"].index(status),
                                       key=f"status_{job_id}")
            if new_status != status:
                update_status(job_id, new_status)
                st.rerun()
        with col2:
            if st.button("Remove", key=f"del_{job_id}"):
                delete_saved_job(job_id)
                st.rerun()