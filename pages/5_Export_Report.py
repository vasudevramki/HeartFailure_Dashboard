from pathlib import Path
import streamlit as st
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

st.set_page_config(
    page_title="Export Report",
    page_icon="📄",
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

st.title("📄 Export Clinical Report")

st.markdown("---")

# --------------------------------------------------
# CHECK REPORT
# --------------------------------------------------

if st.session_state.get("report") is None:

    st.warning("Please complete AI Analysis first.")

    st.stop()

patient = st.session_state.get("patient")

report = st.session_state.get("report")

analysis = report["analysis"]

recommendation = report["recommendation"]

# --------------------------------------------------
# PDF FUNCTION
# --------------------------------------------------

def generate_pdf():

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]

    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]

    body = styles["BodyText"]

    elements = []

    # ---------------------------------------
    # LOGO
    # ---------------------------------------

    try:

        project_dir = Path(__file__).resolve().parent.parent

        logo_path = project_dir / "assets" / "healium_logo.png"
                             
        logo = Image(
            str(logo_path),
            width=2.0*inch,
            height=2.0*inch
        )

        logo.hAlign = "CENTER"

        elements.append(logo)

    except:

        pass

    elements.append(
        Paragraph(
            "Heart Failure Clinical Decision Support System",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Clinical Decision Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1,20)
    )
    # ---------------------------------------
    # PATIENT INFORMATION
    # ---------------------------------------

    elements.append(
        Paragraph("Patient Information", heading)
    )

    patient_table = [

        ["Age", str(patient.age)],

        ["Gender", patient.gender],

        ["Height", f"{patient.height} cm"],

        ["Weight", f"{patient.weight} kg"],

        ["BMI", str(patient.bmi)],

        [
            "Diabetes",
            "Yes" if patient.diabetes else "No"
        ],

        [
            "Hypertension",
            "Yes" if patient.hypertension else "No"
        ],

        [
            "Smoking",
            "Yes" if patient.smoking else "No"
        ],

        [
            "Family History",
            "Yes" if patient.family_history else "No"
        ]

    ]

    patient_info = Table(
        patient_table,
        colWidths=[180, 250]
    )

    patient_info.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EAF3FF")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE")

        ])

    )

    elements.append(patient_info)

    elements.append(
        Spacer(1,18)
    )

    # ---------------------------------------
    # BIOMARKER SUMMARY
    # ---------------------------------------

    elements.append(
        Paragraph("Clinical Biomarkers", heading)
    )

    biomarker_table = [

        ["Biomarker", "Value", "Status"],

        [
            "BNP",
            f"{patient.bnp} pg/mL",
            analysis["Biomarkers"]["BNP"]
        ],

        [
            "IL-6",
            f"{patient.il6} pg/mL",
            analysis["Biomarkers"]["IL-6"]
        ],

        [
            "Galectin-3",
            f"{patient.gal3} ng/mL",
            analysis["Biomarkers"]["Galectin-3"]
        ],

        [
            "ST2",
            f"{patient.st2} ng/mL",
            analysis["Biomarkers"]["ST2"]
        ]

    ]

    biomarker_info = Table(
        biomarker_table,
        colWidths=[150, 150, 130]
    )

    biomarker_info.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E88E5")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8),

            ("ALIGN", (1,1), (-1,-1), "CENTER")

        ])

    )

    elements.append(biomarker_info)

    elements.append(
        Spacer(1,18)
    )
        # ---------------------------------------
    # AI ANALYSIS
    # ---------------------------------------

    elements.append(
        Paragraph("AI Analysis", heading)
    )

    analysis_table = [

        ["Parameter", "Result"],

        [
            "Predominant Heart Failure Phenotype",
            analysis["Diagnosis"]
        ],

        [
            "AI Confidence",
            f"{analysis['Confidence']} %"
        ],

        [
            "Clinical Severity",
            analysis["Severity"]
        ],

        [
            "Risk Level",
            analysis["Risk"]
        ]

    ]

    analysis_info = Table(
        analysis_table,
        colWidths=[220, 210]
    )

    analysis_info.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0B5ED7")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE")

        ])

    )

    elements.append(analysis_info)

    elements.append(
        Spacer(1,18)
    )

    # ---------------------------------------
    # CLINICAL INTERPRETATION
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Clinical Interpretation",
            heading
        )
    )

    interpretation = analysis["Interpretation"]

    elements.append(
        Paragraph(
            interpretation,
            body
        )
    )

    elements.append(
        Spacer(1,18)
    )
        # ---------------------------------------
    # TREATMENT RECOMMENDATION
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Treatment Recommendation",
            heading
        )
    )

    primary = recommendation["Primary Drug"]

    treatment_table = [

        ["Primary Drug", primary["drug"]],

        [
            "Suitability",
            f"{primary['score']} %"
        ]

    ]

    treatment_info = Table(
        treatment_table,
        colWidths=[180, 250]
    )

    treatment_info.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EAF3FF")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8)

        ])

    )

    elements.append(treatment_info)

    elements.append(
        Spacer(1,15)
    )

    # ---------------------------------------
    # ALTERNATIVE DRUGS
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Alternative Drugs",
            heading
        )
    )

    alt_table = [["Drug", "Suitability"]]

    for drug in recommendation["Alternative Drugs"]:

        alt_table.append(

            [
                drug["drug"],
                f"{drug['score']} %"
            ]

        )

    alt_info = Table(
        alt_table,
        colWidths=[260,120]
    )

    alt_info.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E88E5")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8),

            ("ALIGN", (1,1), (-1,-1), "CENTER")

        ])

    )

    elements.append(alt_info)

    elements.append(
        Spacer(1,15)
    )

    # ---------------------------------------
    # MONITORING PLAN
    # ---------------------------------------

    if "Monitoring Plan" in recommendation:

        elements.append(
            Paragraph(
                "Monitoring Plan",
                heading
            )
        )

        for item in recommendation["Monitoring Plan"]:

            elements.append(
                Paragraph(
                    f"• {item}",
                    body
                )
            )

        elements.append(
            Spacer(1,15)
        )

    # ---------------------------------------
    # FOOTER
    # ---------------------------------------

    elements.append(
        Paragraph(
            "<b>Confidential Clinical Report</b>",
            styles["Heading3"]
        )
    )

    elements.append(
        Paragraph(
            "For Authorized Clinical Use Only",
            body
        )
    )

    elements.append(
        Spacer(1,10)
    )

    elements.append(
        Paragraph(
            f"Report Generated: {datetime.now().strftime('%d %B %Y | %I:%M %p')}",
            body
        )
    )

    # ---------------------------------------
    # BUILD PDF
    # ---------------------------------------

    doc.build(elements)

    buffer.seek(0)

    return buffer


# --------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------

pdf_file = generate_pdf()

st.success("Clinical report is ready.")

st.download_button(
    label="📥 Download Clinical Report (PDF)",
    data=pdf_file,
    file_name="HEALIUM_Clinical_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)
