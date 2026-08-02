import streamlit as st
from resume.extractor import extract_text_from_pdf
from resume.parser import parse_resume
from style import apply_custom_style

st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")
apply_custom_style()

st.title("Resume Parser")
st.caption("Upload your resume to extract key details.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your resume..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Resume Text")
        parsed = parse_resume(raw_text)
        st.session_state["parsed_resume"] = parsed
        st.success("Resume stored!")

    st.success("Resume parsed successfully")
    st.write(f"**Email:** {parsed['email'] or 'Not found'}")
    st.write(f"**Phone:** {parsed['phone'] or 'Not found'}")
    st.write(f"**Skills detected:** {', '.join(parsed['skills']) if parsed['skills'] else 'None detected'}")
    st.write(f"**Education section found:** {'YES' if parsed['has_education'] else 'NO'}")
    st.write(f"**Experience section found:** {'YES' if parsed['has_experience'] else 'NO'}")
    st.write(f"**Projects section found:** {'YES' if parsed['has_projects'] else 'NO'}")