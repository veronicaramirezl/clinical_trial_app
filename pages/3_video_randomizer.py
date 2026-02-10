import streamlit as st
from utils.randomizer import (
    initialize_session_state,
    get_stratum,
    assign_balanced_video,
    VIDEO_LIST
)
from utils.google_sheets import save_assigned_video, get_video_counts_for_stratum

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
# ASSIGN VIDEO ONCE (WITH STRATIFIED RANDOMIZATION)
# -------------------------
if st.session_state["assigned_video"] is None:
    # Get participant demographics
    gender = st.session_state["user_data"]["gender_identity"]
    race = st.session_state["user_data"]["race"]
    
    # Determine stratum
    stratum = get_stratum(gender, race)
    
    # Get current video counts for this stratum
    video_counts = get_video_counts_for_stratum(stratum)
    
    # Assign video using weighted randomization
    new_video = assign_balanced_video(stratum, video_counts)
    
    # Save to session and database
    st.session_state["assigned_video"] = new_video
    p_id = st.session_state["user_data"]["participant_id"]
    save_assigned_video(p_id, new_video, stratum)

# -------------------------
# DISPLAY VIDEO
# -------------------------
st.info("Please watch the video below in its entirety.")

# Convert path to string and ensure it's properly formatted
video_path = str(st.session_state["assigned_video"])

# Debug: Show what video is being loaded (remove this in production)
# st.write(f"Loading video: {video_path}")

st.video(video_path)

st.write("---")
st.write("Click 'Next' only when you have finished watching.")

if st.button("Next: Post-Video Questionnaire"):
    st.switch_page("pages/4_questionnaire.py")