import streamlit as st

st.set_page_config(
    page_title="Treatment Recommendation",
    page_icon="🩺",
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

st.title("🩺 AI Treatment Recommendation")

st.markdown("---")

# --------------------------------------------------
# CHECK REPORT
# --------------------------------------------------

if st.session_state.get("report") is None:
    st.warning("Please complete the AI Analysis first.")
    st.stop()

report = st.session_state.get("report")

analysis = report["analysis"]
recommendation = report["recommendation"]

patient = st.session_state.get("patient")

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.subheader("Patient Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Diagnosis", analysis["Diagnosis"])

with c2:
    st.metric("Severity", analysis["Severity"])

with c3:
    st.metric("Risk", analysis["Risk"])

st.markdown("---")

# --------------------------------------------------
# PRIMARY DRUG
# --------------------------------------------------

primary = recommendation["Primary Drug"]

st.subheader("🏆 Primary Drug Recommendation")

st.success(
    f"""
### {primary['drug']}

Suitability Score: **{primary['score']}%**
"""
)

# --------------------------------------------------
# WHY THIS DRUG
# --------------------------------------------------

st.subheader("Why was this selected?")

if analysis["Diagnosis"] == "Fibrotic Phenotype":

    st.info("""
• Elevated Galectin-3 indicates myocardial fibrosis.

• Increased ST2 suggests active cardiac remodeling.

• Mineralocorticoid receptor antagonists are appropriate first-line options.
""")

elif analysis["Diagnosis"] == "Inflammatory Phenotype":

    st.info("""
• Elevated IL-6 suggests inflammatory activity.

• SGLT2 inhibitors have demonstrated cardiovascular benefit.

• ACE inhibitors remain useful in long-term management.
""")

else:

    st.info("""
• BNP indicates ventricular overload.

• ARNI therapy improves cardiac function.

• Beta blockers reduce disease progression.
""")

st.markdown("---")

# --------------------------------------------------
# ALTERNATIVES
# --------------------------------------------------

st.subheader("Alternative Drugs")

for drug in recommendation["Alternative Drugs"]:

    st.write(
        f"**{drug['drug']}** — Suitability: {drug['score']}%"
    )

st.markdown("---")

# --------------------------------------------------
# MONITORING
# --------------------------------------------------

if "Monitoring Plan" in recommendation:

    st.subheader("Monitoring Plan")

    for item in recommendation["Monitoring Plan"]:

        st.write("✅", item)

st.markdown("---")

# --------------------------------------------------
# SAFETY CHECKS
# --------------------------------------------------

st.subheader("Clinical Alerts")

alerts = []

if patient.bnp > 500:
    alerts.append(
        "High BNP indicates significant ventricular stress."
    )

if patient.gal3 > 25:
    alerts.append(
        "High Galectin-3 suggests advanced fibrosis."
    )

if patient.st2 > 50:
    alerts.append(
        "Elevated ST2 indicates ongoing cardiac remodeling."
    )

if patient.il6 > 15:
    alerts.append(
        "Raised IL-6 indicates inflammatory activity."
    )

if patient.diabetes:
    alerts.append(
        "Monitor blood glucose during treatment."
    )

if patient.hypertension:
    alerts.append(
        "Regular blood pressure monitoring advised."
    )

if alerts:

    for alert in alerts:

        st.warning(alert)

else:

    st.success("No major clinical alerts detected.")

st.markdown("---")

# --------------------------------------------------
# FINAL DECISION
# --------------------------------------------------

st.subheader("AI Clinical Decision")

st.success(f"""
### Recommended Initial Therapy

**{primary['drug']}**

This recommendation is based on:

- Heart failure subtype
- Biomarker profile
- Patient comorbidities
- AI suitability scoring
- Clinical risk assessment

**This recommendation should support—not replace—clinical judgment.**
""")

st.markdown("---")

st.info("➡️ Proceed to the **Export Report** page to generate the final clinical report.")
