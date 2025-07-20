import streamlit as st
import pandas as pd
import numpy as np

# Load Data
df = pd.read_csv("loan_sample_100k.csv")

# Risk Classification
def classify_risk(row):
    if row["LTV"] > 4 and row["BorrowerIncomeRatio"] <= 2 and row["AffordabilityCategory"] >= 3:
        return "High Risk"
    else:
        return "Medium/Low Risk"

df["RiskCategory"] = df.apply(classify_risk, axis=1)

# App Layout
st.title("Defi-Nest: Mortgage Risk & Simulation Dashboard")

st.markdown("#### Current Dataset Size: " + str(len(df)))

# Simulation Slider
st.sidebar.header("Macro Scenario Simulator")
rate_shock = st.sidebar.slider("Interest Rate Shock (%)", 0, 5, 0)
shock_factor = 1 + (rate_shock * 0.1)  # Each 1% = 10% increase in high-risk

# Charts
st.subheader("📊 Delinquency Rate by Loan Program")
loan_program_risk = df.groupby("FederalGuarantee")["RiskCategory"].value_counts(normalize=True).unstack().fillna(0)
st.bar_chart(loan_program_risk["High Risk"] * shock_factor)

st.subheader("📊 Risk by Loan Purpose")
loan_purpose_risk = df.groupby("LoanPurpose")["RiskCategory"].value_counts(normalize=True).unstack().fillna(0)
st.bar_chart(loan_purpose_risk["High Risk"] * shock_factor)

st.subheader("📊 Risk by Program (Real Data)")
st.dataframe(loan_program_risk.style.format("{:.2%}"))

# Optional: Show Full Data
if st.checkbox("Show Raw Data"):
    st.write(df.head(50))

# Footer
st.caption("Capstone Dashboard by Navnita Pandey | NYU Stern Fintech")
