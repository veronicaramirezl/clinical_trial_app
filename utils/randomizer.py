import random
import uuid
from pathlib import Path
import streamlit as st

# -------------------------
# VIDEO PATHS (LOCAL MP4s)
# -------------------------
VIDEO_DIR = Path("assets/videos")

VIDEO_LIST = [
    str(VIDEO_DIR / "Black Female LBP-CT.mp4"),
    str(VIDEO_DIR / "Black Female LBP-S.mp4"),
    str(VIDEO_DIR / "Black Male LBP-CT.mp4"),
    str(VIDEO_DIR / "Black Male LBP-S.mp4"),
    str(VIDEO_DIR / "White Female LBP-CT.mp4"),
    str(VIDEO_DIR / "White Female LBP-SV1.mp4"),
    str(VIDEO_DIR / "White Male LBP-CT.mp4"),
    str(VIDEO_DIR / "White Male LBP-S.mp4"),
]

# -------------------------
# FUNCTIONS
# -------------------------
def generate_participant_id():
    return str(uuid.uuid4())[:8].upper()

def get_random_video():
    return random.choice(VIDEO_LIST)

def initialize_session_state():
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {
            "participant_id": generate_participant_id()
        }
    if "demographics_complete" not in st.session_state:
        st.session_state["demographics_complete"] = False
    if "assigned_video" not in st.session_state:
        st.session_state["assigned_video"] = None
