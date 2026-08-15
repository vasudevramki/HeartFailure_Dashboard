import streamlit as st

st.set_page_config(
    page_title="Heart Failure AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# SESSION STATE
# -----------------------------

defaults = {
    "patient": None,
    "report": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# CSS
# -----------------------------

from pathlib import Path

css_path = Path(__file__).parent / "style.css"
try:
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass


# -----------------------------
# TITLE
# -----------------------------

from pathlib import Path

logo_path = Path(__file__).parent / "assets" / "healium_logo.png"

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([2, 1, 2])

with center:
    st.image(str(logo_path), use_container_width=True)

st.markdown(
    """
    <h1 style='text-align:center;
               color:#1565C0;
               font-size:48px;
               margin-bottom:0px;'>
        HEALIUM
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center;
               color:#555555;
               margin-top:-15px;'>
        Heart Failure Clinical Decision Support System
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;
              font-size:18px;
              color:#666666;'>
        AI-Powered Proteomics Decision Support Platform
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.warning(
    "⚠️ This is an educational/demo tool using simulated rule-based scoring, "
    "not a validated clinical model. It is not intended for real diagnostic "
    "or treatment decisions — always consult a qualified healthcare professional."
)

st.markdown("---")

st.markdown("""
### Welcome

This AI-powered Clinical Decision Support System assists clinicians by:

- Predicting Heart Failure subtype
- Assessing clinical risk
- Recommending medications
- Providing AI confidence
- Generating a clinical report

Use the sidebar to begin.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Workflow

1. Patient Information

2. AI Analysis

3. Clinical Report

4. Treatment Recommendation

5. Export Report
""")

with col2:

    st.success("""
### AI Features

✔ Biomarker Analysis

✔ Risk Prediction

✔ Severity Assessment

✔ Drug Ranking

✔ Clinical Interpretation
""")

st.markdown("---")

st.subheader("System Status")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Backend", "Online")

with c2:
    st.metric("AI Engine", "Ready")

with c3:
    st.metric("Charts", "Loaded")

st.markdown("---")

st.caption("Heart Failure AI Clinical Decision Support System")
