import streamlit as st

st.set_page_config(
    page_title="Clinical Report",
    page_icon="📋",
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

st.title("📋 Clinical Report")

st.markdown("---")

# -----------------------------------------------------
# CHECK REPORT
# -----------------------------------------------------

if st.session_state.get("report") is None:
    st.warning("Please complete the AI Analysis first.")
    st.stop()

report = st.session_state.get("report")
analysis = report["analysis"]
recommendation = report["recommendation"]

patient = st.session_state.get("patient")

# -----------------------------------------------------
# PATIENT SUMMARY
# -----------------------------------------------------

st.subheader("👤 Patient Summary")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Age:** {patient.age}")
    st.write(f"**Gender:** {patient.gender}")
    st.write(f"**BMI:** {patient.bmi}")

with col2:
    st.write(f"**Diabetes:** {'Yes' if patient.diabetes else 'No'}")
    st.write(f"**Hypertension:** {'Yes' if patient.hypertension else 'No'}")
    st.write(f"**Smoking:** {'Yes' if patient.smoking else 'No'}")

st.markdown("---")

# -----------------------------------------------------
# AI RESULTS
# -----------------------------------------------------

st.subheader("🧠 AI Results")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Diagnosis", analysis["Diagnosis"])

with c2:
    st.metric("Confidence", f"{analysis['Confidence']}%")

with c3:
    st.metric("Severity", analysis["Severity"])

with c4:
    st.metric("Risk", analysis["Risk"])

st.markdown("---")

# -----------------------------------------------------
# BIOMARKERS
# -----------------------------------------------------

st.subheader("🧪 Biomarker Status")

for marker, status in analysis["Biomarkers"].items():
    st.write(f"**{marker}:** {status}")

st.markdown("---")

# -----------------------------------------------------
# INTERPRETATION
# -----------------------------------------------------

st.subheader("📝 Clinical Interpretation")

st.info(analysis["Interpretation"])

st.markdown("---")

# -----------------------------------------------------
# PRIMARY DRUG
# -----------------------------------------------------

st.subheader("💊 Primary Drug Recommendation")

primary = recommendation["Primary Drug"]

st.success(
    f"{primary['drug']}  |  Suitability: {primary['score']}%"
)

st.markdown("---")

# -----------------------------------------------------
# ALTERNATIVE DRUGS
# -----------------------------------------------------

st.subheader("🔄 Alternative Drugs")

for drug in recommendation["Alternative Drugs"]:
    st.write(f"• {drug['drug']} ({drug['score']}%)")

st.markdown("---")

# -----------------------------------------------------
# MONITORING
# -----------------------------------------------------

if "Monitoring Plan" in recommendation:

    st.subheader("📅 Monitoring Plan")

    for item in recommendation["Monitoring Plan"]:
        st.write(f"• {item}")

st.success("Proceed to the Treatment page from the sidebar.")
