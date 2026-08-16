import streamlit as st
from job_search import get_salary_benchmark
from style import apply_custom_style

st.set_page_config(page_title="Salary Benchmark", page_icon="💰", layout="wide")
apply_custom_style()

st.title(" Salary Benchmarking")
st.caption("See real salary ranges for a role in a specific city, based on live job listings.")

role = st.selectbox("Role", ["Python Developer", "Web Developer", "Full Stack Developer", "DevOps Engineer", "Java Developer"])
location = st.selectbox("Location", ["Pune", "Mumbai", "Bangalore", "Hyderabad"])

if st.button(" Get Salary Data"):
    with st.spinner("Analyzing live salary data..."):
        data = get_salary_benchmark(role, location)

    if not data:
        st.warning("Not enough salary data available for this role/location combination. Many listings don't disclose salary.")
    else:
        st.success(f"Based on {data['sample_size']} listings with disclosed salary")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="stat-number">₹{data["minimum"]:,}</div><div class="stat-label">Minimum</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><div class="stat-number">₹{data["average"]:,}</div><div class="stat-label">Average</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-box"><div class="stat-number">₹{data["maximum"]:,}</div><div class="stat-label">Maximum</div></div>', unsafe_allow_html=True)

        