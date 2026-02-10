import streamlit as st
from utils.google_sheets import save_final_survey

# Security Check: Ensure user has been assigned a video
if not st.session_state.get('assigned_video'):
    st.switch_page("pages/1_welcome.py")

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
st.title("Post-Video Questionnaire")
st.write("After watching the video, please rate your level of agreement with each of the following statements.")
st.caption("⚠️ All questions are required.")

# Likert Scale Options
options = [
    "",
    "1 - Strongly Disagree", 
    "2 - Disagree", 
    "3 - Neutral", 
    "4 - Agree", 
    "5 - Strongly Agree"
]

with st.form("likert_form"):
    
    # --- Likert Scale Questions ---
    q1 = st.selectbox("1. I trust the information presented in this video. *", options=options)
    
    q2 = st.selectbox("2. I feel confident in the accuracy of the information provided. *", options=options)
    
    q3 = st.selectbox("3. The presenter appeared knowledgeable about the topic. *", options=options)
    
    q4 = st.selectbox("4. The information in this video would influence my treatment decisions. *", options=options)
    
    q5 = st.selectbox("5. I believe the presenter had my best interests in mind. *", options=options)
    
    q6 = st.selectbox("6. The presenter's communication style made the information easy to understand. *", options=options)
    
    q7 = st.selectbox("7. The presenter's background made me more likely to trust the video's content. *", options=options)
    
    q8 = st.selectbox("8. I would recommend this video to others seeking information on this topic. *", options=options)
    
    st.divider()
    st.markdown("#### Additional Questions")
    
    # --- Additional Questions ---
    q9 = st.radio(
        "9. How much of the information presented in this video do you feel you can trust? *", 
        ["", "Almost all of the information", "Most of the information", "Some of the information", "Almost none of the information"],
        index=0
    )
    
    q10 = st.radio(
        "10. Did you find the presenter competent? *", 
        ["", "Yes", "No"],
        index=0
    )

    st.divider()
    st.markdown("#### Perceptions of the Presenter")

    q11 = st.selectbox(
        "11. What gender did the presenter seem to be? *",
        ["", "Man", "Woman", "Non-binary", "Prefer not to say", "Not sure"],
    )

    q12 = st.selectbox(
        "12. What race/ethnicity did the presenter seem to be? *",
        [
            "",
            "White",
            "Black or African American",
            "Hispanic or Latino",
            "Asian",
            "Other",
            "Not sure",
            "Prefer not to say",
        ],
    )

    q13 = st.radio(
        "13. Did the presenter seem AI-generated? *",
        ["", "Yes", "No", "Not sure"],
        index=0,
    )
    
    submitted = st.form_submit_button("Finish Study")
    
    if submitted:
        # Validation
        errors = []
        
        if not q1 or q1 == "":
            errors.append("Question 1")
        if not q2 or q2 == "":
            errors.append("Question 2")
        if not q3 or q3 == "":
            errors.append("Question 3")
        if not q4 or q4 == "":
            errors.append("Question 4")
        if not q5 or q5 == "":
            errors.append("Question 5")
        if not q6 or q6 == "":
            errors.append("Question 6")
        if not q7 or q7 == "":
            errors.append("Question 7")
        if not q8 or q8 == "":
            errors.append("Question 8")
        if not q9 or q9 == "":
            errors.append("Question 9")
        if not q10 or q10 == "":
            errors.append("Question 10")
        if not q11 or q11 == "":
            errors.append("Question 11")
        if not q12 or q12 == "":
            errors.append("Question 12")
        if not q13 or q13 == "":
            errors.append("Question 13")
        
        if errors:
            st.error(f"⚠️ Please answer all required questions. Missing: {', '.join(errors)}")
        else:
            # Collect all data
            data = {
                "Likert_1": q1,
                "Likert_2": q2,
                "Likert_3": q3,
                "Likert_4": q4,
                "Likert_5": q5,
                "Likert_6": q6,
                "Likert_7": q7,
                "Likert_8": q8,
                "Trust_Level": q9,
                "Competence": q10,
                "Perceived_Gender": q11,
                "Perceived_Race_Ethnicity": q12,
                "Perceived_AI_Generated": q13
            }
            
            p_id = st.session_state['user_data'].get('participant_id', 'Unknown')
            
            # Save to Google Sheets
            with st.spinner("Saving your responses..."):
                success = save_final_survey(p_id, data)
            
            if success:
                st.switch_page("pages/5_finish.py")
            else:
                st.error("There was an error saving your data. Please check your internet connection and try again.")