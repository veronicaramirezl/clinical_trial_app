import streamlit as st
from utils.randomizer import get_random_video
from utils.google_sheets import save_assigned_video

# Security Check
if not st.session_state.get('demographics_complete'):
    st.switch_page("pages/2_demographics.py")

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
st.title("Video Session")

# --- ASSIGNMENT LOGIC ---
# If no video assigned yet, pick one AND SAVE IT immediately
if st.session_state.get('assigned_video') is None:
    # 1. Pick Video
    new_video = get_random_video()
    st.session_state['assigned_video'] = new_video
    
    # 2. Save to Google Sheets immediately (Persist changes)
    p_id = st.session_state['user_data']['participant_id']
    save_assigned_video(p_id, new_video)

# Display Video
video_url = st.session_state['assigned_video']

st.info("Please watch the video below in its entirety.")
st.video(video_url)

st.write("---")
st.write("Click 'Next' only when you have finished watching.")

if st.button("Next: Post-Video Questionnaire"):
    st.switch_page("pages/4_questionnaire.py")