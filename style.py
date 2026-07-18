import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
        }
        h1 {
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .job-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: 0.2s;
        }
        .job-card:hover {
            border: 1px solid rgba(0, 212, 255, 0.6);
        }
        .stButton>button {
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
        }
        .stButton>button:hover {
            opacity: 0.9;
        }
        section[data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.9);
        }
        </style>
    """, unsafe_allow_html=True)