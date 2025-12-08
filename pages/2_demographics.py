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
        # now the participant ID exists and form appears


# ---- RETURNING USER ----
with col2:
    code = st.text_input("Enter Return Code:", key="return_code")

    if code and st.button("Restore Session"):
        with st.spinner("Restoring your session..."):
            result = load_participant_data(code)

            if result and result["found"]:
                # Restore minimal required data
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
        
        # ---------------------------------------
        # A. Demographics
        # ---------------------------------------
        st.markdown("#### A. Demographics")

        age = st.number_input("1. What is your age?", min_value=18, max_value=110, step=1)
        sex = st.selectbox("2. What is your biological sex?", ["Male", "Female", "Intersex", "Prefer not to say"])
        gender = st.selectbox("3. What is your gender identity?", ["Man", "Woman", "Non-binary", "Prefer not to say"])
        edu = st.selectbox("4. Education level:", [
            "Less than high school",
            "High school diploma or GED",
            "Some college, no degree",
            "Associate degree",
            "Bachelor’s degree",
            "Master’s degree",
            "Doctoral or professional degree"
        ])
        insurance = st.radio("5. Do you have health insurance?", ["Yes", "No"])
        insurance_type = st.text_input("6. If yes, what type?")

        english = st.select_slider("7. English proficiency:", 
                                   options=["Poor", "Fair", "Good", "Very good", "Fluent"])

        income = st.selectbox("8. Annual household income:", [
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

        health_status = st.select_slider("9. Overall health:", 
                                         options=["Poor", "Fair", "Good", "Very good", "Excellent"])

        chronic = st.radio("10. Chronic conditions:", ["Yes", "No", "Prefer not to say"])

        visit_freq = st.selectbox("11. Healthcare visits:", [
            "Rarely or never",
            "Once or twice a year",
            "Once every few months",
            "More than once a month"
        ])

        # ---------------------------------------
        # C. TRUST ONLINE INFO
        # ---------------------------------------
        st.markdown("#### C. Trust in Online Health Information")
        st.caption("Rate your agreement.")

        tohi_options = ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]

        trust_web_1 = st.select_slider("12. I trust the information I find online.", options=tohi_options)
        trust_web_2 = st.select_slider("13. I feel confident in online health accuracy.", options=tohi_options)
        trust_web_3 = st.select_slider("14. I would follow online medical advice.", options=tohi_options)

        # ---------------------------------------
        # D. MISTRUST
        # ---------------------------------------
        st.markdown("#### D. Views on Healthcare")
        st.caption("Rate your agreement.")

        mistrust_1 = st.select_slider("15. You cannot trust doctors to tell the truth.", options=tohi_options)
        mistrust_2 = st.select_slider("16. Doctors care more about convenience than patient needs.", options=tohi_options)
        mistrust_3 = st.select_slider("17. Health professionals do not always keep information private.", options=tohi_options)
        mistrust_4 = st.select_slider("18. Professionals treat some people better than others.", options=tohi_options)

        # ---------------------------------------
        # E. DISCRIMINATION
        # ---------------------------------------
        st.markdown("#### E. Experiences of Discrimination")

        freq_options = ["Never", "A few times a year", "A few times a month", "At least once a week", "Almost every day"]

        discrim_1 = st.select_slider("19. Treated with less respect.", options=freq_options)
        discrim_2 = st.select_slider("20. People assume you are dishonest.", options=freq_options)
        discrim_3 = st.select_slider("21. People act superior.", options=freq_options)
        discrim_4 = st.select_slider("22. Called names or insulted.", options=freq_options)

        discrim_healthcare = st.radio("23. Experienced discrimination in healthcare?", ["Yes", "No", "Prefer not to say"])

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

        nutri_1 = st.number_input("24. Total calories if you eat the entire container:", step=1)
        nutri_2 = st.number_input("25. Cups allowed if limit is 60 g carbs:", step=0.5)
        nutri_3 = st.number_input("26. Total protein if eating the container:", step=1)

        # ------------------------
        # SUBMIT
        # ------------------------
        submit = st.form_submit_button("Submit and Continue")

        if submit:
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
