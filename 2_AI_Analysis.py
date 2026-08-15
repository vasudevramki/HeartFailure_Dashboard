import streamlit as st

from backend import analyze_patient

from charts import (
    confidence_gauge,
    risk_indicator,
    biomarker_chart,
    biomarker_status_chart,
    diagnosis_chart
)

st.set_page_config(
    page_title="AI Analysis",
    page_icon="🧠",
    layout="wide"
)

# Load CSS
from pathlib import Path
css_path = Path(__file__).parent.parent / "style.css"
try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("🧠 AI Analysis")

st.markdown("---")

# -----------------------------------------------------
# CHECK IF PATIENT EXISTS
# -----------------------------------------------------

if st.session_state.get("patient") is None:

    st.warning("Please enter patient information first.")

    st.stop()

patient = st.session_state.get("patient")

st.success("Patient information loaded successfully.")

st.markdown("---")

# -----------------------------------------------------
# RUN AI
# -----------------------------------------------------

if st.button("🚀 Run AI Analysis", use_container_width=True):

    with st.spinner("Running AI Model..."):

        report = analyze_patient(patient)

        st.session_state.report = report

    st.success("AI Analysis Completed Successfully!")

st.markdown("---")

# -----------------------------------------------------
# DISPLAY REPORT
# -----------------------------------------------------

if st.session_state.get("report") is not None:

    report = st.session_state.get("report")

    analysis = report["analysis"]

    st.header("AI Diagnosis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Diagnosis",
            analysis["Diagnosis"]
        )

    with col2:
        st.metric(
            "Confidence",
            f"{analysis['Confidence']} %"
        )

    with col3:
        st.metric(
            "Severity",
            analysis["Severity"]
        )

    with col4:
        st.metric(
            "Risk",
            analysis["Risk"]
        )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(
            confidence_gauge(
                analysis["Confidence"]
            ),
            use_container_width=True
        )

    with c2:

        st.plotly_chart(
            risk_indicator(
                analysis["Risk"]
            ),
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Patient Biomarkers")

    st.plotly_chart(

        biomarker_chart(patient),

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Biomarker Status")

    st.plotly_chart(

        biomarker_status_chart(
            analysis["Biomarkers"]
        ),

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Heart Failure Subtype Scores")

    st.plotly_chart(

        diagnosis_chart(
            analysis["Scores"]
        ),

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Clinical Interpretation")

    st.info(
        analysis["Interpretation"]
    )

    st.success(
        "Proceed to the Clinical Report page from the sidebar."
    )