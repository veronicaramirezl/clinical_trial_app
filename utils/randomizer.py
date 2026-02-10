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



def get_stratum(gender, race):
    gender_key = gender if gender in ["Man", "Woman"] else "OtherGender"
    race_key = race if race in ["White", "Black or African American"] else "OtherRace"
    return f"{gender_key}_{race_key}"

def get_video_counts_for_stratum(stratum):
    """
    Returns a dict: {video_path: count}
    """
    sheet = get_sheet()  # use your existing connection
    records = sheet.get_all_records()

    counts = {}
    for r in records:
        if r.get("stratum") == stratum:
            v = r.get("video_url")
            counts[v] = counts.get(v, 0) + 1

    return counts
