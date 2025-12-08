import streamlit as st
from utils.randomizer import initialize_session_state, generate_participant_id
from utils.google_sheets import get_participant_by_id

initialize_session_state()

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

st.title("Login & Background Survey")

# If demographics are already done, auto-forward to video
if st.session_state.get('demographics_complete'):
    st.switch_page("pages/3_video_randomizer.py")

st.subheader("1. Participant Identification")

col1, col2 = st.columns(2)

# --- NEW USER LOGIC ---
with col1:
    if st.button("I am a New Participant"):
        new_id = generate_participant_id()
        st.session_state['user_data'] = {'participant_id': new_id}
        st.rerun()

# --- RETURNING USER LOGIC ---
with col2:
    def check_return_code():
        code = st.session_state.return_code_input
        if code:
            with st.spinner("Searching for your record..."):
                existing_data = get_participant_by_id(code)
                
            if existing_data:
                # User found! Restore ID and skip demographics
                st.session_state['user_data']['participant_id'] = code
                # Restore basic demographics if needed, or just mark complete
                # We mark complete so they don't overwrite their old demographics with blanks
                st.session_state['demographics_complete'] = True
                st.success("Welcome back! Resuming session...")
                st.switch_page("pages/3_video_randomizer.py")
            else:
                st.error("Code not found. Please try again or start as new.")

    st.text_input("Enter existing Return Code:", key="return_code_input", on_change=check_return_code)


# --- DISPLAY ID & FORM (Only if not complete) ---
if 'participant_id' in st.session_state['user_data']:
    p_id = st.session_state['user_data']['participant_id']
    st.success(f"**Your Return Code is: {p_id}**")
    st.warning("Please save this code.")

    with st.form("demographics_form"):
        st.write("Please complete the following sections.")
        
        # A. Demographics
        st.markdown("#### A. Demographics")
        age = st.number_input("1. What is your age?", min_value=18, max_value=110) 
        sex = st.selectbox("2. What is your biological sex?", ["Male", "Female", "Intersex", "Prefer not to say"]) 
        gender = st.selectbox("3. What is your gender identity?", ["Man", "Woman", "Non-binary", "Prefer not to say"]) 
        edu = st.selectbox("4. Highest level of education?", [
            "Less than high school", "High school diploma/GED", "Some college", 
            "Associate degree", "Bachelor’s degree", "Master’s degree", "Doctoral degree"
        ]) 
        insurance = st.radio("5. Do you have health insurance?", ["Yes", "No"]) 
        insurance_type = st.text_input("6. (If Yes) Type of insurance? (e.g. Private, Medicare)") 
        english = st.select_slider("7. English Proficiency", options=["Poor", "Fair", "Good", "Very good", "Fluent"]) 
        income = st.selectbox("8. Annual Household Income", [
            "Less than $25,000", "$25,000 - $49,999", "$50,000 - $74,999", 
            "$75,000 - $99,999", "$100,000 - $149,999", "$150,000 or more", "Prefer not to say"
        ]) 

        # B. Health
        st.markdown("#### B. Health Status")
        health_status = st.select_slider("9. Overall Health", options=["Poor", "Fair", "Good", "Very good", "Excellent"]) 
        chronic = st.radio("10. Do you have chronic health conditions?", ["Yes", "No", "Prefer not to say"]) 
        visit_freq = st.selectbox("11. How often do you visit a healthcare provider?", [
            "Rarely or never", "Once or twice a year", "Once every few months", "More than once a month"
        ]) 

        # C. Trust
        st.markdown("#### C. Trust in Online Information")
        st.write("1 = Strongly Disagree, 4 = Strongly Agree")
        trust_web = st.select_slider("12. I trust health info on the internet.", options=[1, 2, 3, 4]) 
        
        # D. Medical Mistrust
        st.markdown("#### D. Views on Healthcare")
        mistrust_1 = st.select_slider("13. You cannot trust doctors to tell you the truth.", options=["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]) 
        mistrust_2 = st.select_slider("14. Doctors care more about convenience than your needs.", options=["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]) 
        
        # E. Discrimination
        st.markdown("#### E. Experiences")
        discrim_1 = st.selectbox("15. You are treated with less respect than other people.", [
            "Never", "A few times a year", "A few times a month", "At least once a week", "Almost every day"
        ]) 
        
        # F. Nutrition Literacy
        st.markdown("#### F. Nutrition Literacy")
        st.info("""
        **Nutrition Label:**
        * Serving Size: 1 cup (228g)
        * Calories: 260
        * Total Fat: 12g
        * Total Carb: 31g
        * Protein: 5g
        """)
        nutri_1 = st.number_input("16. If you eat the entire container, how many calories will you eat?", step=1) 
        nutri_2 = st.number_input("17. If you can eat 60g of carbs, how many cups can you have?", step=0.5) 

        submit = st.form_submit_button("Submit and Continue")

        if submit:
            st.session_state['user_data'].update({
                "participant_id": p_id,
                "age": age, "sex": sex, "gender_identity": gender, "education": edu,
                "insurance": insurance, "income": income, "health_status": health_status,
                "mistrust_1": mistrust_1, "discrim_1": discrim_1, "nutri_1": nutri_1
            })
            st.session_state['demographics_complete'] = True
            st.switch_page("pages/3_video_randomizer.py")