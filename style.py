import streamlit as st

def apply_custom_style():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    with st.sidebar:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Theme")
        with col2:
            if st.button("🔄"):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()

    if st.session_state.theme == "dark":
        bg = "radial-gradient(circle at 20% 20%, #1a1f3a 0%, #0d1025 50%, #0a0c1a 100%)"
        text_color = "#eef0fa"
        card_bg = "rgba(255, 255, 255, 0.06)"
        card_border = "rgba(124, 131, 253, 0.25)"
        sidebar_bg = "#0d1025"
        heading_gradient = "linear-gradient(90deg, #7c83fd, #22d3ee)"
        subtext_color = "#9aa0c3"
        accent = "#7c83fd"
        accent2 = "#22d3ee"
        select_bg = "rgba(255,255,255,0.06)"
    else:
        bg = "#f6f7fd"
        text_color = "#14162b"
        card_bg = "#ffffff"
        card_border = "rgba(91, 95, 239, 0.25)"
        sidebar_bg = "#ffffff"
        heading_gradient = "linear-gradient(90deg, #5b5fef, #0891b2)"
        subtext_color = "#4b4f6b"
        accent = "#5b5fef"
        accent2 = "#0891b2"
        select_bg = "#ffffff"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

        /* BLANKET OVERRIDE FIRST — catches anything Streamlit's own theme sets */
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] * ,
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: {bg} !important;
        }}
        section[data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            border-right: 1px solid {card_border};
        }}

        h1 {{
            font-family: 'Poppins', sans-serif;
            background: {heading_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.7rem !important;
            letter-spacing: -0.5px;
        }}
        h2, h3, h4 {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
        }}
        .subtext {{
            color: {subtext_color} !important;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }}

        .hero {{
            text-align: center;
            padding: 48px 20px 24px 20px;
        }}
        .hero-badge {{
            display: inline-block;
            background: rgba(124, 131, 253, 0.15);
            color: {accent2} !important;
            padding: 7px 18px;
            border-radius: 24px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 18px;
            border: 1px solid rgba(124, 131, 253, 0.35);
        }}

        .stat-box {{
            background: {card_bg};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 18px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 1.9rem;
            font-weight: 800;
            font-family: 'Poppins', sans-serif;
            background: {heading_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stat-label {{
            color: {subtext_color} !important;
            font-size: 0.85rem;
        }}

        .job-card {{
            background: {card_bg};
            border: 1px solid {card_border};
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 18px;
            height: 100%;
            transition: 0.25s ease;
        }}
        .job-card:hover {{
            border: 1px solid {accent};
            box-shadow: 0 8px 24px rgba(124, 131, 253, 0.3);
            transform: translateY(-3px);
        }}
        .job-company {{ color: {accent2} !important; font-weight: 600; font-size: 0.9rem; }}
        .job-meta {{ color: {subtext_color} !important; font-size: 0.85rem; margin: 6px 0; }}
        .job-desc {{ color: {subtext_color} !important; font-size: 0.85rem; margin: 8px 0; }}
        .job-card a {{ color: {accent} !important; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .job-card a:hover {{ color: {accent2} !important; }}

        .stButton>button {{
            background: {heading_gradient} !important;
            border: none !important;
            border-radius: 10px;
            padding: 11px 26px;
            font-weight: 700;
        }}
        .stButton>button, .stButton>button * {{
            color: #ffffff !important;
        }}
        .stButton>button:hover {{
            opacity: 0.88;
            box-shadow: 0 4px 16px rgba(124, 131, 253, 0.4);
        }}

        div[data-baseweb="select"] > div {{
            background-color: {select_bg} !important;
            border: 1px solid {card_border} !important;
        }}
        input[type="number"] {{
            background-color: {select_bg} !important;
        }}
        /* File uploader widget */
        [data-testid="stFileUploaderDropzone"] {{
            background-color: {card_bg} !important;
            border: 1px dashed {card_border} !important;
        }}
        [data-testid="stFileUploaderDropzone"] * {{
            color: {text_color} !important;
        }}
        [data-testid="stFileUploaderDropzone"] button {{
            background: {heading_gradient} !important;
            color: #ffffff !important;
            border: none !important;
        }}
        [data-testid="stFileUploaderDropzone"] button * {{
            color: #ffffff !important;
        }}
        </style>
    """, unsafe_allow_html=True)