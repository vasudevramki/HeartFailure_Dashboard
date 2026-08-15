"""
charts.py
-------------------------------------------------------
Interactive Plotly Charts for HF-CDSS Dashboard
Styled with a Futuristic Light-Beige AI Theme
-------------------------------------------------------
"""

import plotly.graph_objects as go
import plotly.express as px

# ==========================================================
# THEME UTILITY FUNCTION
# ==========================================================

def apply_futuristic_theme(fig):
    """
    Applies a clean, futuristic glassmorphic style to the chart layout,
    blending with the warm beige background.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Segoe UI, system-ui, -apple-system, sans-serif",
            size=12,
            color="#3D3530"
        ),
        title_font=dict(
            family="Segoe UI, system-ui, -apple-system, sans-serif",
            size=16,
            color="#3C332E"
        ),
        xaxis=dict(
            gridcolor="rgba(169, 146, 96, 0.08)",
            zerolinecolor="rgba(169, 146, 96, 0.15)",
            tickfont=dict(color="#6E6359"),
            title_font=dict(color="#4D4540")
        ),
        yaxis=dict(
            gridcolor="rgba(169, 146, 96, 0.08)",
            zerolinecolor="rgba(169, 146, 96, 0.15)",
            tickfont=dict(color="#6E6359"),
            title_font=dict(color="#4D4540")
        ),
        margin=dict(l=20, r=20, t=55, b=20)
    )
    return fig


# ==========================================================
# AI CONFIDENCE GAUGE
# ==========================================================

def confidence_gauge(confidence):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={
                "suffix": "%",
                "font": {
                    "size": 34,
                    "color": "#2D2723",
                    "family": "Segoe UI, sans-serif"
                }
            },
            title={
                "text": "AI Confidence",
                "font": {
                    "size": 15,
                    "color": "#3C332E"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#6E6359",
                    "tickwidth": 1
                },
                "bar": {
                    "color": "#A99260",
                    "thickness": 0.24
                },
                "bgcolor": "rgba(255, 255, 255, 0.35)",
                "borderwidth": 1,
                "bordercolor": "rgba(169, 146, 96, 0.2)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(236, 112, 99, 0.15)"},
                    {"range": [40, 70], "color": "rgba(248, 196, 113, 0.15)"},
                    {"range": [70, 100], "color": "rgba(130, 224, 170, 0.15)"},
                ],
            },
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        height=320,
        margin=dict(l=25, r=25, t=55, b=25)
    )

    return fig


# ==========================================================
# RISK INDICATOR
# ==========================================================

def risk_indicator(risk):

    colors = {
        "Low": "#27AE60",
        "Moderate": "#D35400",
        "High": "#C0392B"
    }

    values = {
        "Low": 35,
        "Moderate": 70,
        "High": 100
    }

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=values[risk],
            number={
                "suffix": "",
                "font": {
                    "size": 34,
                    "color": "#2D2723",
                    "family": "Segoe UI, sans-serif"
                }
            },
            title={
                "text": f"Risk Level : {risk}",
                "font": {
                    "size": 15,
                    "color": "#3C332E"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#6E6359",
                    "tickwidth": 1
                },
                "bar": {
                    "color": colors[risk],
                    "thickness": 0.24
                },
                "bgcolor": "rgba(255, 255, 255, 0.35)",
                "borderwidth": 1,
                "bordercolor": "rgba(169, 146, 96, 0.2)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(88, 214, 141, 0.12)"},
                    {"range": [35, 70], "color": "rgba(245, 176, 65, 0.12)"},
                    {"range": [70, 100], "color": "rgba(236, 112, 99, 0.12)"}
                ]
            }
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        height=300,
        margin=dict(l=25, r=25, t=55, b=25)
    )

    return fig


# ==========================================================
# BIOMARKER VALUES
# ==========================================================

def biomarker_chart(patient):

    biomarkers = [
        "BNP",
        "IL-6",
        "Galectin-3",
        "ST2"
    ]

    values = [
        patient.bnp,
        patient.il6,
        patient.gal3,
        patient.st2
    ]

    fig = px.bar(
        x=biomarkers,
        y=values,
        text=values,
        labels={
            "x": "Biomarker",
            "y": "Value"
        }
    )

    fig.update_traces(
        marker_color="rgba(94, 207, 194, 0.8)", # glowing clinical cyan
        marker_line_color="#3EAE9F",
        marker_line_width=1.5,
        textposition="outside",
        textfont=dict(
            family="Segoe UI, system-ui, -apple-system, sans-serif",
            size=14,
            color="#1F1916"
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        title="Patient Biomarker Levels",
        height=420,
        xaxis_title="",
        yaxis_title="Measured Value"
    )

    return fig


# ==========================================================
# BIOMARKER STATUS
# ==========================================================

def biomarker_status_chart(summary):

    status_map = {
        "Normal": 1,
        "Elevated": 2,
        "High": 3
    }

    biomarkers = list(summary.keys())

    values = [
        status_map[x]
        for x in summary.values()
    ]

    colors = []
    line_colors = []

    for status in summary.values():

        if status == "Normal":
            colors.append("rgba(88, 214, 141, 0.75)") # glowing green
            line_colors.append("#27AE60")

        elif status == "Elevated":
            colors.append("rgba(245, 176, 65, 0.75)") # glowing yellow
            line_colors.append("#D35400")

        else:
            colors.append("rgba(236, 112, 99, 0.75)") # glowing red
            line_colors.append("#C0392B")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=biomarkers,
            y=values,
            marker_color=colors,
            marker_line_color=line_colors,
            marker_line_width=1.5,
            text=list(summary.values()),
            textposition="outside",
            textfont=dict(
                family="Segoe UI, sans-serif",
                size=12,
                color="#3D3530"
            )
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        title="Biomarker Status",
        yaxis=dict(
            tickvals=[1, 2, 3],
            ticktext=[
                "Normal",
                "Elevated",
                "High"
            ],
            gridcolor="rgba(169, 146, 96, 0.08)"
        ),
        height=420
    )

    return fig


# ==========================================================
# DRUG SUITABILITY
# ==========================================================

def drug_chart(drugs):

    names = []
    scores = []

    for drug in drugs:

        names.append(drug["drug"])
        scores.append(drug["score"])

    fig = px.bar(
        x=scores,
        y=names,
        orientation="h",
        text=scores,
        labels={
            "x": "Suitability Score (%)",
            "y": ""
        }
    )

    fig.update_traces(
        marker_color="rgba(169, 146, 96, 0.75)", # glowing gold
        marker_line_color="#A99260",
        marker_line_width=1.5,
        textposition="outside",
        textfont=dict(
            family="Segoe UI, sans-serif",
            size=11,
            color="#3D3530"
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        title="AI Drug Recommendation",
        height=420,
        yaxis=dict(
            autorange="reversed",
            gridcolor="rgba(169, 146, 96, 0.08)"
        )
    )

    return fig


# ==========================================================
# HEART FAILURE SUBTYPE SCORES
# ==========================================================

def diagnosis_chart(scores):

    diagnosis = list(scores.keys())
    values = list(scores.values())

    fig = px.bar(
        x=diagnosis,
        y=values,
        text=values
    )

    fig.update_traces(
        marker_color="rgba(169, 146, 96, 0.75)", # glowing gold
        marker_line_color="#A99260",
        marker_line_width=1.5,
        textposition="outside",
        textfont=dict(
            family="Segoe UI, sans-serif",
            size=12,
            color="#3D3530"
        )
    )

    apply_futuristic_theme(fig)
    fig.update_layout(
        title="AI Diagnostic Scores",
        height=420,
        xaxis_title="",
        yaxis_title="AI Score"
    )

    return fig


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def dashboard_metrics(report):

    return {

        "Diagnosis":
            report["analysis"]["Diagnosis"],

        "Confidence":
            report["analysis"]["Confidence"],

        "Risk":
            report["analysis"]["Risk"],

        "Severity":
            report["analysis"]["Severity"]

    }