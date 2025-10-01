git initgitgit --version
gi

import streamlit as st

def study_eligibility():
    st.title("Study Eligibility Checker")
    st.write("For trials: **Megarox, SODa-BIC, REMAP-CAP, DRIVE**")

    # --- Intubation & Ventilation ---
    on_iv = st.radio("Is the patient intubated and ventilated?", ["Yes", "No"]) == "Yes"
    iv_hours = None
    fio2 = None

    if on_iv:
        iv_hours = st.number_input("Hours since ventilation started:", min_value=0.0, step=1.0)
        if iv_hours < 72:
            fio2 = st.number_input("Current FiO₂ (enter as fraction, e.g. 0.4 for 40%)",
                                   min_value=0.21, max_value=1.0, step=0.01)

    # --- SODa-BIC ---
    sodabic_ok = False
    ph = st.number_input("pH on last ABG (enter 7.4 if no ABG available):",
                         min_value=6.0, max_value=8.0, step=0.01, value=7.4)
    if ph < 7.3:
        be = st.number_input("Base excess on last ABG (negative allowed):")
        if be <= -4:
            paco2 = st.number_input("PaCO₂ on last ABG:", min_value=0.0, step=1.0)
            if paco2 <= 45:
                sodabic_ok = True

    # --- REMAP-CAP ---
    remap_ok = False
    if st.checkbox("LRTI symptoms present (e.g. SOB, cough)?"):
        if st.checkbox("Consolidation on imaging?"):
            if st.checkbox("Any of: I+V, NIV, vasopressor/inotropes, or HFNP ≥40% + ≥30 L/min?"):
                icu_h = st.number_input("Hours since ICU admission:", min_value=0.0, step=1.0)
                if icu_h < 24:
                    hosp_h = st.number_input("Hours since hospital admission:", min_value=0.0, step=1.0)
                    if hosp_h < 48:
                        remap_ok = True

    # --- Megarox & DRIVE ---
    megarox_ok = False
    drive_ok = False
    if on_iv:
        if iv_hours < 12:
            megarox_ok = True
        if iv_hours < 72 and fio2 is not None and fio2 >= 0.4:
            drive_ok = True

    # --- Results ---
    st.subheader("Eligibility Results")
    results = []
    if megarox_ok:
        results.append("✅ **Megarox** - Eligible")
    if drive_ok:
        results.append("✅ **DRIVE** - Eligible (see ICU Research Coordinators to enrol)")
    if sodabic_ok:
        results.append("✅ **SODa-BIC** - Eligible (see ICU Research Coordinators to enrol)")
    if remap_ok:
        results.append("✅ **REMAP-CAP** - Eligible")

    if results:
        if len(results) > 1:
            st.success("Eligible for multiple studies:\n\n" + "\n".join(results))
        else:
            st.success("\n".join(results))
    else:
        st.error("Not eligible for any study. Thank you for checking.")

if __name__ == "__main__":
    study_eligibility()
