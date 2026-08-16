import streamlit as st
from datetime import datetime, date, time
from resume.calendar_utils import generate_ics
from style import apply_custom_style

st.set_page_config(page_title="Interview Scheduler", page_icon="📅", layout="wide")
apply_custom_style()

st.title("Interview Scheduler")
st.caption("Schedule an interview and add it directly to your calendar.")

job_title = st.selectbox("Job Title",[ "Python Developer", "Full Stack Developer","Web Developer","DevOPs Engineer","Java Developer"])
company = st.selectbox("Company Name",[ "TCS", "Infosys", "RockWell", "HoneyWell", "Hexaware","Entrata","Cognizant","Cognify","WNS"])

col1, col2 = st.columns(2)
with col1:
    interview_date = st.date_input("Interview Date", date.today())
with col2:
    interview_time = st.time_input("Interview Time", time(10, 0))

duration = st.selectbox("Duration", [30, 45, 60, 90], index=2)
notes = st.text_area("Notes", "Round 1-")

if st.button("Generate Calendar Invite"):
    interview_datetime = datetime.combine(interview_date, interview_time)
    ics_content = generate_ics(job_title, company, interview_datetime, duration, notes)

    st.success("Calendar invite ready! Download and open it to add to your calendar.")
    st.download_button(
        label="⬇Download Calendar Invite (.ics)",
        data=ics_content,
        file_name=f"interview_{company.replace(' ', '_')}.ics",
        mime="text/calendar"
    )

    