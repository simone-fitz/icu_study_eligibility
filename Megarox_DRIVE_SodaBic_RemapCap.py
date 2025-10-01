def study_eligibility():
    """
    study eligibility algorithm Megarox, SODa-BIC, REMAP-CAP, DRIVE
    """
    def ask_yn(q):
        while True:
            ans = input(f"{q} (y/n): ").strip().lower()
            if ans in ("y", "n"): return ans == "y"
            print("Please enter 'y' or 'n'.")

    def ask_float(q):
        while True:
            s = input(q + ": ").strip().replace("%", "")
            try:
                val = float(s)
                return val
            except ValueError:
                print("Please enter a number.")

    def ask_fio2(q):
        while True:
            s = input(q + ": ").strip().replace("%", "")
            try:
                val = float(s)
                # if entered as %, convert to fraction
                if val > 1.0:
                    val = val / 100.0
                if 0.21 <= val <= 1.0:
                    return val
                else:
                    print("FiO2 must be between 0.21 (21%) and 1.0 (100%).")
            except ValueError:
                print("Please enter a valid number (fraction like 0.4 or percent like 40).")

    print("\nWhat studies is my patient eligible for?\n")

    # base questions- is pt I+V and if so how long for
    on_iv = ask_yn("Is the patient intubated and ventilated?")
    iv_hours = None
    fio2 = None
    if on_iv:
        iv_hours = ask_float("Hours since ventilation started?")
        # only ask FiO2 if hours <72 ie. could be eligible for Drive but not Megarox
        if iv_hours < 72:
            fio2 = ask_fio2("Current FiO2")

    # check sodabic eligibility
    sodabic_ok = False
    ph = ask_float("pH on last ABG (enter 7.4 if no ABG available)")
    if ph < 7.3:
        be = ask_float("Base excess on last ABG (include negative sign if required)")
        if be <= -4:
            paco2 = ask_float("PaCO2 on last ABG")
            if paco2 <= 45:
                sodabic_ok = True

    # check REMAP-CAP eligibility
    remap_ok = False
    if ask_yn("LRTI symptoms present eg SOB, cough?"):
        if ask_yn("Consolidation on imaging?"):
            if ask_yn("Any of the following now: I+V, NIV, vasopressor/inotropes, or HFNP ≥40% + ≥30 L/min?"):
                icu_h = ask_float("Hours since ICU admission")
                if icu_h < 24:
                    hosp_h = ask_float("Hours since hospital admission")
                    if hosp_h < 48:
                        remap_ok = True

    # Megarox & DRIVE (depend only on I+V data)
    megarox_ok = False
    drive_ok = False
    if on_iv:
        if iv_hours is not None and iv_hours < 12:
            megarox_ok = True
        if iv_hours is not None and iv_hours < 72 and fio2 is not None and fio2 >= 0.4:
            drive_ok = True

    # collate results
    results = []
    if megarox_ok:
        results.append("Megarox- Eligible for Megarox")
    if drive_ok:
        results.append("DRIVE- Eligible for DRIVE. See ICU Research Coordinators to enrol")
    if sodabic_ok:
        results.append("SODa-BIC- Eligible for SODa-BIC. See ICU Research Coordinators to enrol")
    if remap_ok:
        results.append("REMAP-CAP- Eligible for REMAP-CAP")

    print("\n--- Result ---")
    if results:
        if len(results) > 1:
            print("Eligible for multiple studies:")
        for line in results:
            print(line)
    else:
        print("Not eligible for any study. Thank you for checking")

# pause so the window doesn't close immediately in an .exe build
#input("\nPress Enter to exit...")

# Run
if __name__ == "__main__":
    study_eligibility()


