import streamlit as st
from utils.randomizer import (
    get_random_video,
    initialize_session_state
)
from utils.google_sheets import save_assigned_video

# -------------------------
# SESSION INIT
# -------------------------
initialize_session_state()

# -------------------------
# SECURITY CHECK
# -------------------------
if not st.session_state["demographics_complete"]:
    st.switch_page("pages/2_demographics.py")

st.markdown(
    "<style>[data-testid='stSidebar'] {display: none;}</style>",
    unsafe_allow_html=True
)

st.title("Video Session")

# -------------------------
# ASSIGN VIDEO ONCE
# -------------------------
if st.session_state["assigned_video"] is None:
    new_video = get_random_video()
    st.session_state["assigned_video"] = new_video

    p_id = st.session_state["user_data"]["participant_id"]
    save_assigned_video(p_id, new_video)

# -------------------------
# DISPLAY VIDEO
# -------------------------
st.info("Please watch the video below in its entirety.")
st.video(st.session_state["assigned_video"])

st.write("---")
st.write("Click 'Next' only when you have finished watching.")

if st.button("Next: Post-Video Questionnaire"):
    st.switch_page("pages/4_questionnaire.py")
