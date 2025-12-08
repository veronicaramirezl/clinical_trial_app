import streamlit as st
from utils.randomizer import initialize_session_state, generate_participant_id
from utils.google_sheets import save_demographics, load_participant_data

initialize_session_state()

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
st.title("Login & Background Survey")

# --- CHECK FOR RETURNING USER ---
col1, col2 = st.columns(2)

# ---- NEW PARTICIPANT ----
with col1:
    if st.button("I am a New Participant"):
        st.session_state.user_data = {'participant_id': generate_participant_id()}
        st.session_state.new_user_flag = True
        st.rerun()

    if st.session_state.get("new_user_flag"):
        st.session_state.new_user_flag = False


# ---- RETURNING USER ----
with col2:
    code = st.text_input("Enter Return Code:", key="return_code")

    if code and st.button("Restore Session"):
        with st.spinner("Restoring your session..."):
            result = load_participant_data(code)

            if result and result["found"]:
                st.session_state.user_data = {"participant_id": code}
                st.session_state.demographics_complete = True

                if result.get("video_url"):
                    st.session_state.assigned_video = result["video_url"]

                st.success("Session restored!")
                st.session_state.go_to_video = True
                st.rerun()
            else:
                st.error("Code not found.")

# Redirect after restoration
if st.session_state.get("go_to_video"):
    st.session_state.go_to_video = False
    st.switch_page("pages/3_video_randomizer.py")


# -----------------------------
# --- DEMOGRAPHICS FORM ---
# -----------------------------
if "user_data" in st.session_state and "participant_id" in st.session_state.user_data:

    p_id = st.session_state.user_data["participant_id"]
    st.info(f"**Your Return Code: {p_id}** (Please save this to resume your progress.)")

    with st.form("demographics_form"):
        st.write("Please complete the following sections.")
        st.caption("⚠️ All questions are required.")
        
        # ---------------------------------------
        # A. Demographics
        # ---------------------------------------
        st.markdown("#### A. Demographics")

        age = st.number_input("1. What is your age? *", min_value=18, max_value=110, step=1, value=None, format="%d")
        sex = st.selectbox("2. What is your biological sex? *", ["", "Male", "Female", "Intersex", "Prefer not to say"])
        gender = st.selectbox("3. What is your gender identity? *", ["", "Man", "Woman", "Non-binary", "Prefer not to say"])
        edu = st.selectbox("4. Education level: *", [
            "",
            "Less than high school",
            "High school diploma or GED",
            "Some college, no degree",
            "Associate degree",
            "Bachelor's degree",
            "Master's degree",
            "Doctoral or professional degree"
        ])
        insurance = st.radio("5. Do you have health insurance? *", ["", "Yes", "No"], index=0)

        insurance_type = st.selectbox(
                "6. What type of health insurance do you have? *",
                [
                    "",
                    "Private (Employer or Marketplace)",
                    "Medicare",
                    "Medicaid",
                    "Military / VA",
                    "Public (Other)",
                    "Prefer not to say",
                    "None"
                ]
            )


        english = st.selectbox("7. English proficiency: *", 
                          ["", "Poor", "Fair", "Good", "Very good", "Fluent"])

        income = st.selectbox("8. Annual household income: *", [
            "",
            "Less than $25,000",
            "$25,000 - $49,999",
            "$50,000 - $74,999",
            "$75,000 - $99,999",
            "$100,000 - $149,999",
            "$150,000 or more",
            "Prefer not to say"
        ])

        # ---------------------------------------
        # B. HEALTH ACCESS
        # ---------------------------------------
        st.markdown("#### B. Health & Healthcare Access")

        health_status = st.selectbox("9. Overall health: *", 
                                 ["", "Poor", "Fair", "Good", "Very good", "Excellent"])

        chronic = st.radio("10. Chronic conditions: *", ["", "Yes", "No", "Prefer not to say"], index=0)

        visit_freq = st.selectbox("11. Healthcare visits: *", [
            "",
            "Rarely or never",
            "Once or twice a year",
            "Once every few months",
            "More than once a month"
        ])

        # ---------------------------------------
        # C. TRUST ONLINE INFO
        # ---------------------------------------
        st.markdown("#### C. Trust in Online Health Information")
        st.caption("Rate your agreement (1 = Strongly Disagree, 5 = Strongly Agree).")

        tohi_options = ["", "1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"]

        trust_web_1 = st.selectbox("12. I trust the information I find online. *", options=tohi_options)
        trust_web_2 = st.selectbox("13. I feel confident in online health accuracy. *", options=tohi_options)
        trust_web_3 = st.selectbox("14. I would follow online medical advice. *", options=tohi_options)

        # ---------------------------------------
        # D. MISTRUST
        # ---------------------------------------
        st.markdown("#### D. Views on Healthcare")
        st.caption("Rate your agreement (1 = Strongly Disagree, 5 = Strongly Agree).")

        mistrust_1 = st.selectbox("15. You cannot trust doctors to tell the truth. *", options=tohi_options)
        mistrust_2 = st.selectbox("16. Doctors care more about convenience than patient needs. *", options=tohi_options)
        mistrust_3 = st.selectbox("17. Health professionals do not always keep information private. *", options=tohi_options)
        mistrust_4 = st.selectbox("18. Professionals treat some people better than others. *", options=tohi_options)

        # ---------------------------------------
        # E. DISCRIMINATION
        # ---------------------------------------
        st.markdown("#### E. Experiences of Discrimination")
        st.caption("How often do you experience the following?")

        freq_options = ["", "Never", "A few times a year", "A few times a month", "At least once a week", "Almost every day"]

        discrim_1 = st.selectbox("19. Treated with less respect. *", options=freq_options)
        discrim_2 = st.selectbox("20. People assume you are dishonest. *", options=freq_options)
        discrim_3 = st.selectbox("21. People act superior. *", options=freq_options)
        discrim_4 = st.selectbox("22. Called names or insulted. *", options=freq_options)

        discrim_healthcare = st.radio("23. Experienced discrimination in healthcare? *", ["", "Yes", "No", "Prefer not to say"], index=0)

        # ---------------------------------------
        # F. NUTRITION LITERACY
        # ---------------------------------------
        st.markdown("#### F. Nutrition Literacy")
        st.info("""
        **Nutrition Facts**
        Serving Size: 1 cup (228 g)
        Servings Per Container: 2
        Calories: 260
        Total Fat: 12 g
        Saturated Fat: 3 g
        Cholesterol: 30 mg
        Sodium: 660 mg
        Total Carbohydrate: 31 g
        Sugars: 5 g
        Protein: 5 g
        """)

        nutri_1 = st.number_input("24. Total calories if you eat the entire container: *", step=1, value=None, format="%d")
        nutri_2 = st.number_input("25. Cups allowed if limit is 60 g carbs: *", step=0.5, value=None, format="%.1f")
        nutri_3 = st.number_input("26. Total protein if eating the container: *", step=1, value=None, format="%d")

        # ------------------------
        # SUBMIT
        # ------------------------
        submit = st.form_submit_button("Submit and Continue")

        if submit:
            # Validation
            errors = []
            
            if age is None:
                errors.append("Age")
            if not sex or sex == "":
                errors.append("Biological sex")
            if not gender or gender == "":
                errors.append("Gender identity")
            if not edu or edu == "":
                errors.append("Education level")
            if not insurance or insurance == "":
                errors.append("Health insurance")
            if insurance == "Yes" and (not insurance_type or insurance_type == ""):
                errors.append("Insurance type")
            if not english or english == "":
                errors.append("English proficiency")
            if not income or income == "":
                errors.append("Income")
            if not health_status or health_status == "":
                errors.append("Overall health")
            if not chronic or chronic == "":
                errors.append("Chronic conditions")
            if not visit_freq or visit_freq == "":
                errors.append("Healthcare visits")
            if not trust_web_1 or trust_web_1 == "":
                errors.append("Question 12")
            if not trust_web_2 or trust_web_2 == "":
                errors.append("Question 13")
            if not trust_web_3 or trust_web_3 == "":
                errors.append("Question 14")
            if not mistrust_1 or mistrust_1 == "":
                errors.append("Question 15")
            if not mistrust_2 or mistrust_2 == "":
                errors.append("Question 16")
            if not mistrust_3 or mistrust_3 == "":
                errors.append("Question 17")
            if not mistrust_4 or mistrust_4 == "":
                errors.append("Question 18")
            if not discrim_1 or discrim_1 == "":
                errors.append("Question 19")
            if not discrim_2 or discrim_2 == "":
                errors.append("Question 20")
            if not discrim_3 or discrim_3 == "":
                errors.append("Question 21")
            if not discrim_4 or discrim_4 == "":
                errors.append("Question 22")
            if not discrim_healthcare or discrim_healthcare == "":
                errors.append("Question 23")
            if nutri_1 is None:
                errors.append("Question 24")
            if nutri_2 is None:
                errors.append("Question 25")
            if nutri_3 is None:
                errors.append("Question 26")

            if errors:
                st.error(f"⚠️ Please answer all required questions. Missing: {', '.join(errors)}")
            else:
                st.session_state.user_data.update({
                    "participant_id": p_id,
                    "age": age,
                    "sex": sex,
                    "gender_identity": gender,
                    "education": edu,
                    "insurance": insurance,
                    "insurance_type": insurance_type,
                    "english_proficiency": english,
                    "income": income,
                    "health_status": health_status,
                    "chronic_conditions": chronic,
                    "visit_frequency": visit_freq,
                    "trust_web_1": trust_web_1,
                    "trust_web_2": trust_web_2,
                    "trust_web_3": trust_web_3,
                    "mistrust_1": mistrust_1,
                    "mistrust_2": mistrust_2,
                    "mistrust_3": mistrust_3,
                    "mistrust_4": mistrust_4,
                    "discrim_1": discrim_1,
                    "discrim_2": discrim_2,
                    "discrim_3": discrim_3,
                    "discrim_4": discrim_4,
                    "discrim_healthcare": discrim_healthcare,
                    "nutri_calories": nutri_1,
                    "nutri_carbs": nutri_2,
                    "nutri_protein": nutri_3
                })

                with st.spinner("Saving progress..."):
                    saved = save_demographics(st.session_state.user_data)

                if saved:
                    st.session_state.demographics_complete = True
                    st.switch_page("pages/3_video_randomizer.py")
                else:
                    st.error("Connection error. Please try again.")