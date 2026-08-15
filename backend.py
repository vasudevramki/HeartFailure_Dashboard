"""
backend.py
=========================================================
Heart Failure Clinical Decision Support System (HF-CDSS)

Backend Version 2
=========================================================
"""

from dataclasses import dataclass
from typing import Dict, List


# =========================================================
# BIOMARKER REFERENCE RANGES
# =========================================================

NORMAL_RANGES = {

    "BNP": 100,
    "IL6": 7,
    "GAL3": 17,
    "ST2": 35

}


# =========================================================
# DRUG DATABASE
# =========================================================

DRUG_DATABASE = {

    "Sacubitril/Valsartan": {
        "category": "ARNI",
        "monitoring": [
            "Blood Pressure",
            "Renal Function",
            "Serum Potassium"
        ]
    },

    "Spironolactone": {
        "category": "Mineralocorticoid Receptor Antagonist",
        "monitoring": [
            "Potassium",
            "Renal Function"
        ]
    },

    "Eplerenone": {
        "category": "Mineralocorticoid Receptor Antagonist",
        "monitoring": [
            "Potassium",
            "Kidney Function"
        ]
    },

    "Dapagliflozin": {
        "category": "SGLT2 Inhibitor",
        "monitoring": [
            "Kidney Function",
            "Blood Glucose"
        ]
    },

    "Empagliflozin": {
        "category": "SGLT2 Inhibitor",
        "monitoring": [
            "Kidney Function",
            "Blood Glucose"
        ]
    },

    "Metoprolol": {
        "category": "Beta Blocker",
        "monitoring": [
            "Heart Rate",
            "Blood Pressure"
        ]
    },

    "ACE Inhibitor": {
        "category": "ACE Inhibitor",
        "monitoring": [
            "Blood Pressure",
            "Renal Function"
        ]
    },

    "Furosemide": {
        "category": "Loop Diuretic",
        "monitoring": [
            "Electrolytes",
            "Fluid Balance"
        ]
    }

}


# =========================================================
# PATIENT CLASS
# =========================================================

@dataclass
class Patient:

    age: int

    gender: str

    height: float

    weight: float

    diabetes: bool

    hypertension: bool

    smoking: bool

    family_history: bool

    bnp: float

    il6: float

    gal3: float

    st2: float

    @property
    def bmi(self):

        h = self.height / 100

        if h <= 0:
            return 0

        return round(self.weight / (h * h), 1)


# =========================================================
# BIOMARKER STATUS
# =========================================================

def biomarker_status(value, normal):

    if value <= normal:

        return "Normal"

    elif value <= normal * 1.5:

        return "Elevated"

    else:

        return "High"


# =========================================================
# GET ALL BIOMARKER STATUS
# =========================================================

def get_biomarker_summary(patient):

    return {

        "BNP": biomarker_status(
            patient.bnp,
            NORMAL_RANGES["BNP"]
        ),

        "IL-6": biomarker_status(
            patient.il6,
            NORMAL_RANGES["IL6"]
        ),

        "Galectin-3": biomarker_status(
            patient.gal3,
            NORMAL_RANGES["GAL3"]
        ),

        "ST2": biomarker_status(
            patient.st2,
            NORMAL_RANGES["ST2"]
        )

    }


# =========================================================
# CLINICAL SEVERITY
# =========================================================

def calculate_severity(patient):

    score = 0

    if patient.bnp > 500:
        score += 3

    elif patient.bnp > 250:
        score += 2

    elif patient.bnp > 100:
        score += 1


    if patient.gal3 > 30:
        score += 3

    elif patient.gal3 > 20:
        score += 2

    elif patient.gal3 > 17:
        score += 1


    if patient.st2 > 70:
        score += 3

    elif patient.st2 > 50:
        score += 2

    elif patient.st2 > 35:
        score += 1


    if patient.il6 > 20:
        score += 2

    elif patient.il6 > 10:
        score += 1


    if score <= 3:
        return "Mild"

    elif score <= 7:
        return "Moderate"

    return "Severe"


# =========================================================
# CLINICAL RISK
# =========================================================

def calculate_risk(patient):

    score = 0

    if patient.age >= 65:
        score += 2

    elif patient.age >= 50:
        score += 1


    if patient.diabetes:
        score += 2

    if patient.hypertension:
        score += 2

    if patient.smoking:
        score += 2

    if patient.family_history:
        score += 1


    if patient.bnp > 500:
        score += 3

    if patient.gal3 > 25:
        score += 2

    if patient.st2 > 50:
        score += 2

    if patient.il6 > 15:
        score += 1


    if score <= 4:
        return "Low"

    elif score <= 8:
        return "Moderate"

    return "High"
# =========================================================
# AI WEIGHTED SCORING
# =========================================================

def calculate_ai_scores(patient):
    fibrosis = (
        (patient.gal3 / NORMAL_RANGES["GAL3"]) +
        (patient.st2 / NORMAL_RANGES["ST2"])
    )

    inflammation = (
        patient.il6 / NORMAL_RANGES["IL6"]
    )

    mechanical = (
        patient.bnp / NORMAL_RANGES["BNP"]
    )

    # Bonus scoring

    if patient.gal3 > 25:
        fibrosis += 1.0

    if patient.st2 > 50:
        fibrosis += 1.0

    if patient.il6 > 15:
        inflammation += 1.5

    if patient.bnp > 500:
        mechanical += 1.5

    # Comorbidities

    if patient.diabetes:
        inflammation += 0.3

    if patient.hypertension:
        mechanical += 0.3

    if patient.smoking:
        inflammation += 0.2

    return {

        "Fibrotic Phenotype": round(fibrosis, 2),

        "Inflammatory Phenotype": round(inflammation, 2),

        "Mechanical Stress Phenotype": round(mechanical, 2)

    }


# =========================================================
# DIAGNOSIS
# =========================================================

def get_diagnosis(scores):
    """
    Returns diagnosis with highest AI score.
    """

    return max(scores, key=scores.get)


# =========================================================
# AI CONFIDENCE
# =========================================================

def calculate_confidence(scores):
    """
    Calculates confidence based on score separation.
    """

    values = sorted(scores.values(), reverse=True)

    highest = values[0]
    second = values[1]

    confidence = 70 + ((highest - second) / highest) * 30

    confidence = max(70, confidence)
    confidence = min(99, confidence)

    return round(confidence, 1)


# =========================================================
# DRUG RANKING
# =========================================================

def rank_drugs(patient, diagnosis):
    """
    Returns ranked drug recommendations.
    """

    drugs = {
        "Sacubitril/Valsartan": 70,
        "Spironolactone": 70,
        "Eplerenone": 65,
        "Dapagliflozin": 65,
        "Empagliflozin": 60,
        "Metoprolol": 60,
        "ACE Inhibitor": 55,
        "Furosemide": 50
    }

    if diagnosis == "Fibrotic Phenotype":
        drugs["Spironolactone"] += patient.gal3 * 0.8
        drugs["Eplerenone"] += patient.st2 * 0.5
        drugs["Sacubitril/Valsartan"] += patient.bnp * 0.04

    elif diagnosis == "Inflammatory Phenotype":
        drugs["Dapagliflozin"] += patient.il6 * 1.5
        drugs["Empagliflozin"] += patient.il6 * 1.2
        drugs["ACE Inhibitor"] += patient.bnp * 0.03

    elif diagnosis == "Mechanical Stress Phenotype":
        drugs["Sacubitril/Valsartan"] += patient.bnp * 0.07
        drugs["Metoprolol"] += patient.bnp * 0.04
        drugs["Furosemide"] += patient.bnp * 0.05

    if patient.diabetes:
        drugs["Dapagliflozin"] += 8
        drugs["Empagliflozin"] += 8

    if patient.hypertension:
        drugs["Sacubitril/Valsartan"] += 5
        drugs["ACE Inhibitor"] += 4

    if patient.age >= 65:
        drugs["Metoprolol"] += 3

    ranked = []

    for drug, score in drugs.items():

        score = round(min(score, 99), 1)

        ranked.append({
            "drug": drug,
            "score": score,
            "category": DRUG_DATABASE[drug]["category"],
            "monitoring": DRUG_DATABASE[drug]["monitoring"]
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked


# =========================================================
# CLINICAL INTERPRETATION
# =========================================================

def generate_interpretation(patient, diagnosis, severity, risk):

    findings = []

    if patient.bnp > NORMAL_RANGES["BNP"]:
        findings.append("Elevated BNP")

    if patient.gal3 > NORMAL_RANGES["GAL3"]:
        findings.append("Elevated Galectin-3")

    if patient.st2 > NORMAL_RANGES["ST2"]:
        findings.append("Elevated ST2")

    if patient.il6 > NORMAL_RANGES["IL6"]:
        findings.append("Elevated IL-6")

    biomarkers = ", ".join(findings)

    summary = (
        f"The patient's biomarker profile ({biomarkers}) "
        f"is consistent with {diagnosis.lower()}. "
        f"Clinical severity is assessed as {severity.lower()} "
        f"with an overall {risk.lower()} risk profile."
    )

    return summary
# =========================================================
# REPORT GENERATION
# =========================================================

def generate_report(patient):

    scores = calculate_ai_scores(patient)

    diagnosis = get_diagnosis(scores)

    confidence = calculate_confidence(scores)

    severity = calculate_severity(patient)

    risk = calculate_risk(patient)

    drug_rankings = rank_drugs(patient, diagnosis)

    primary_drug = drug_rankings[0]

    report = {

        "patient": {

            "Age": patient.age,
            "Gender": patient.gender,
            "Height": patient.height,
            "Weight": patient.weight,
            "BMI": patient.bmi

        },

        "analysis": {

            "Diagnosis": diagnosis,
            "Confidence": confidence,
            "Severity": severity,
            "Risk": risk,
            "Scores": scores,
            "Biomarkers": get_biomarker_summary(patient),
            "Interpretation": generate_interpretation(
                patient,
                diagnosis,
                severity,
                risk
            )

        },

        "recommendation": {

            "Primary Drug": primary_drug,
            "Alternative Drugs": drug_rankings[1:4],
            "Monitoring Plan": primary_drug["monitoring"]

        }

    }

    return report


# =========================================================
# MAIN AI FUNCTION
# =========================================================

def analyze_patient(patient):

    return generate_report(patient)


# =========================================================
# SAMPLE TEST
# =========================================================

if __name__ == "__main__":

    patient = Patient(

        age=58,
        gender="Male",

        height=172,
        weight=76,

        diabetes=True,
        hypertension=True,
        smoking=False,
        family_history=True,

        bnp=620,
        il6=10,
        gal3=31,
        st2=59

    )

    result = analyze_patient(patient)

    print("\n========== AI REPORT ==========\n")

    print("Diagnosis :", result["analysis"]["Diagnosis"])
    print("Confidence :", result["analysis"]["Confidence"], "%")
    print("Severity :", result["analysis"]["Severity"])
    print("Risk :", result["analysis"]["Risk"])

    print("\nDrug Recommendation")

    for drug in result["recommendation"]["Alternative Drugs"]:
        print(
            f"- {drug['drug']} ({drug['score']}%)"
        )

    print(
        "\nPrimary Drug:",
        result["recommendation"]["Primary Drug"]["drug"]
    )

    print(
        "Suitability:",
        result["recommendation"]["Primary Drug"]["score"],
        "%"
    )