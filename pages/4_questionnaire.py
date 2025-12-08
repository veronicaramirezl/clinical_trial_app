import streamlit as st
from utils.google_sheets import write_row

# Security Check
if not st.session_state.get('assigned_video'):
    st.switch_page("pages/1_welcome.py")

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

st.title("Post-Video Questionnaire")
st.write("Please rate your agreement with the following statements.")

options = ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"] # [cite: 3-7]

with st.form("likert_form"):
    
    # Likert Questions [cite: 8-15]
    q1 = st.select_slider("1. I trust the information presented in this video.", options=options)
    q2 = st.select_slider("2. I feel confident in the accuracy of the information provided.", options=options)
    q3 = st.select_slider("3. The presenter appeared knowledgeable about the topic.", options=options)
    q4 = st.select_slider("4. The information in this video would influence my treatment decisions.", options=options)
    q5 = st.select_slider("5. I believe the presenter had my best interests in mind.", options=options)
    q6 = st.select_slider("6. The presenter’s communication style made the information easy to understand.", options=options)
    q7 = st.select_slider("7. The presenter’s background made me more likely to trust the video’s content.", options=options)
    q8 = st.select_slider("8. I would recommend this video to others seeking information on this topic.", options=options)

    st.divider()
    st.markdown("#### Additional Questions") # [cite: 16]

    # Additional Questions [cite: 17, 22]
    q9 = st.radio("9. How much of the information presented do you feel you can trust?", 
                  ["Almost all", "Most", "Some", "Almost none"])
    
    q10 = st.radio("10. Did you find the presenter competent?", ["Yes", "No"])

    submitted = st.form_submit_button("Finish Study")

    if submitted:
        data = {
            "Likert_1": q1, "Likert_2": q2, "Likert_3": q3, "Likert_4": q4,
            "Likert_5": q5, "Likert_6": q6, "Likert_7": q7, "Likert_8": q8,
            "Trust_Level": q9, "Competence": q10
        }
        
        with st.spinner("Saving responses..."):
            success = write_row(st.session_state['user_data'], data, st.session_state['assigned_video'])
        
        if success:
            st.switch_page("pages/5_finish.py")
        else:
            st.error("Error saving data. Please try again.")