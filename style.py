import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 50%, #0a0a0a 100%);
        }
        h1 {
            background: linear-gradient(90deg, #ff1744, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        h2, h3, h4 {
            color: #ffffff;
        }
        p, .stMarkdown, .stCaption {
            color: #e0e0e0;
        }
        .job-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 23, 68, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: 0.2s;
        }
        .job-card:hover {
            border: 1px solid #ff1744;
            box-shadow: 0 0 12px rgba(255, 23, 68, 0.25);
        }
        .job-card h3, .job-card h4 {
            color: #ffffff;
        }
        .job-card a {
            color: #ff1744;
            font-weight: 600;
            text-decoration: none;
        }
        .job-card a:hover {
            color: #ffffff;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff1744, #b71c1c);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #ffffff, #e0e0e0);
            color: #000000;
        }
        section[data-testid="stSidebar"] {
            background: #0a0a0a;
            border-right: 1px solid rgba(255, 23, 68, 0.2);
        }
        div[data-baseweb="select"] {
            border-color: rgba(255, 23, 68, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)