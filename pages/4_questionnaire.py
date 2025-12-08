import streamlit as st
from utils.google_sheets import save_final_survey

# Security Check: Ensure user has been assigned a video
if not st.session_state.get('assigned_video'):
    st.switch_page("pages/1_welcome.py")

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

st.title("Post-Video Questionnaire")
st.write("After watching the video, please rate your level of agreement with each of the following statements.")

# [cite_start]Likert Scale Options [cite: 3-7]
options = [
    "1 - Strongly Disagree", 
    "2 - Disagree", 
    "3 - Neutral", 
    "4 - Agree", 
    "5 - Strongly Agree"
]

with st.form("likert_form"):
    
    # [cite_start]--- Likert Scale Questions [cite: 8-15] ---
    q1 = st.select_slider("1. I trust the information presented in this video.", options=options)
    
    q2 = st.select_slider("2. I feel confident in the accuracy of the information provided.", options=options)
    
    q3 = st.select_slider("3. The presenter appeared knowledgeable about the topic.", options=options)
    
    q4 = st.select_slider("4. The information in this video would influence my treatment decisions.", options=options)
    
    q5 = st.select_slider("5. I believe the presenter had my best interests in mind.", options=options)
    
    q6 = st.select_slider("6. The presenter’s communication style made the information easy to understand.", options=options)
    
    q7 = st.select_slider("7. The presenter’s background made me more likely to trust the video’s content.", options=options)
    
    q8 = st.select_slider("8. I would recommend this video to others seeking information on this topic.", options=options)

    st.divider()
    st.markdown("#### Additional Questions")

    # [cite_start]--- Additional Questions [cite: 17-24] ---
    q9 = st.radio(
        "9. How much of the information presented in this video do you feel you can trust?", 
        ["Almost all of the information", "Most of the information", "Some of the information", "Almost none of the information"]
    )
    
    q10 = st.radio(
        "10. Did you find the presenter competent?", 
        ["Yes", "No"]
    )

    submitted = st.form_submit_button("Finish Study")

    if submitted:
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
            "Competence": q10
        }
        
        p_id = st.session_state['user_data'].get('participant_id', 'Unknown')
        
        # Save to Google Sheets
        with st.spinner("Saving your responses..."):
            success = save_final_survey(p_id, data)
        
        if success:
            st.switch_page("pages/5_finish.py")
        else:
            st.error("There was an error saving your data. Please check your internet connection and try again.")