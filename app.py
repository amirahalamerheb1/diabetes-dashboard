import streamlit as st

st.set_page_config(
    page_title="Diabetes Analytics Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Purple & Lavender Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main { background-color: #F5F3FB; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3B1F6B 0%, #512D8F 100%);
    }
    [data-testid="stSidebar"] * { color: #EDE8F8 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #EDE8F8 !important; }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        color: #3B1F6B;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #7B6A9E;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid #7C3AED;
        box-shadow: 0 1px 6px rgba(124,58,237,0.10);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3B1F6B;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #9B8ABE;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.1rem;
    }
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #3B1F6B;
        margin-bottom: 0.3rem;
    }
    .section-sub {
        font-size: 0.9rem;
        color: #9B8ABE;
        margin-bottom: 1.2rem;
    }
    .stSelectbox label, .stSlider label, .stRadio label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #3B1F6B !important;
    }
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        box-shadow: 0 1px 4px rgba(124,58,237,0.08);
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🩺 Diabetes Analytics")
st.sidebar.markdown("---")

pages = {
    "Overview": "pages/1_Overview.py",
    "Demographics & Risk": "pages/2_Demographics.py",
    "Clinical Analysis": "pages/3_Clinical.py",
    "Global Map": "pages/4_Map.py",
    "ML Risk Predictor": "pages/5_Predictor.py",
}

page = st.sidebar.radio("Navigate", list(pages.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown("<small style='color:#C4B5E8'>Data: Pima Indian Diabetes Dataset + IDF Global Data</small>", unsafe_allow_html=True)

# Route to pages
if page == "Overview":
    exec(open("pages/1_Overview.py").read())
elif page == "Demographics & Risk":
    exec(open("pages/2_Demographics.py").read())
elif page == "Clinical Analysis":
    exec(open("pages/3_Clinical.py").read())
elif page == "Global Map":
    exec(open("pages/4_Map.py").read())
elif page == "ML Risk Predictor":
    exec(open("pages/5_Predictor.py").read())
