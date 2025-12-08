import streamlit as st
from utils.randomizer import get_random_video

# Security Check
if not st.session_state.get('demographics_complete'):
    st.warning("Please complete the demographics section first.")
    st.switch_page("pages/2_demographics.py")

st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

st.title("Video Session")

# Assign video if not already assigned
if st.session_state.get('assigned_video') is None:
    st.session_state['assigned_video'] = get_random_video()

video_url = st.session_state['assigned_video']

st.info("Please watch the video below in its entirety.")
st.video(video_url)

st.write("---")
st.write("Click 'Next' only when you have finished watching.")

if st.button("Next: Post-Video Questionnaire"):
    st.switch_page("pages/4_questionnaire.py")