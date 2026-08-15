import streamlit as st
from backend import Patient

st.set_page_config(
    page_title="Patient Information",
    page_icon="👤",
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

st.title("👤 Patient Information")

st.markdown("Enter the patient's clinical information below.")

st.markdown("---")

# ----------------------------------------------------
# Patient Details
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=55
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=250.0,
        value=70.0
    )

with col2:

    diabetes = st.checkbox("Diabetes")

    hypertension = st.checkbox("Hypertension")

    smoking = st.checkbox("Smoking")

    family_history = st.checkbox("Family History")

st.markdown("---")

st.subheader("Cardiac Biomarkers")

c1, c2 = st.columns(2)

with c1:

    bnp = st.number_input(
        "BNP (pg/mL)",
        min_value=0.0,
        value=120.0,
        step=10.0
    )

    il6 = st.number_input(
        "IL-6 (pg/mL)",
        min_value=0.0,
        value=6.0,
        step=0.5
    )

with c2:

    gal3 = st.number_input(
        "Galectin-3 (ng/mL)",
        min_value=0.0,
        value=16.0,
        step=0.5
    )

    st2 = st.number_input(
        "ST2 (ng/mL)",
        min_value=0.0,
        value=30.0,
        step=1.0
    )

st.markdown("---")

# ----------------------------------------------------
# BMI
# ----------------------------------------------------

height_m = height / 100

bmi = round(weight / (height_m ** 2), 1)

st.metric("Calculated BMI", bmi)

st.markdown("---")

# ----------------------------------------------------
# Save Patient
# ----------------------------------------------------

if st.button("💾 Save Patient Information", use_container_width=True):

    patient = Patient(
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        diabetes=diabetes,
        hypertension=hypertension,
        smoking=smoking,
        family_history=family_history,
        bnp=bnp,
        il6=il6,
        gal3=gal3,
        st2=st2
    )

    st.session_state.patient = patient
    st.session_state.report = None

    st.success("✅ Patient information saved successfully!")

    st.info("➡️ Open **AI Analysis** from the sidebar to continue.")

# ----------------------------------------------------
# Preview
# ----------------------------------------------------

if st.session_state.get("patient") is not None:

    st.markdown("---")

    st.subheader("Current Patient")

    p = st.session_state.get("patient")

    st.write(f"**Age:** {p.age}")

    st.write(f"**Gender:** {p.gender}")

    st.write(f"**BMI:** {p.bmi}")

    st.write(f"**BNP:** {p.bnp}")

    st.write(f"**IL-6:** {p.il6}")

    st.write(f"**Galectin-3:** {p.gal3}")

    st.write(f"**ST2:** {p.st2}")
