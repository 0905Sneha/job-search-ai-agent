import streamlit as st
from style import apply_custom_style
from resume.analyzer import analyze_resume

st.set_page_config(
    page_title="Resume Analysis",
    page_icon="🎯",
    layout="wide"
)

apply_custom_style()

st.title("AI Resume Analysis")

if "parsed_resume" not in st.session_state:
    st.warning("Please upload your resume on the Resume Parser page first.")
    st.stop()

parsed_resume = st.session_state["parsed_resume"]

if st.button("Analyze Resume"):

    result = analyze_resume(parsed_resume)

    st.metric("ATS Score", f"{result['ats_score']}%")

    st.subheader("Recommended Roles")
    for role in result["recommended_roles"]:
        st.write(f"✅ {role}")

    st.subheader("Strengths")
    for item in result["strengths"]:
        st.write(f"• {item}")

    st.subheader("Missing Skills")
    for item in result["missing_skills"]:
        st.write(f"• {item}")

    st.subheader("AI Suggestions")
    for item in result["suggestions"]:
        st.write(f"• {item}")

    