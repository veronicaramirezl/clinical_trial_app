import random
import uuid
from pathlib import Path
import streamlit as st

# -------------------------
# VIDEO PATHS (LOCAL MP4s)
# -------------------------
VIDEO_DIR = Path("assets/videos")

# Using forward slashes - works cross-platform
VIDEO_LIST = [
    "assets/videos/Black Female LBP-CT.mp4",
    "assets/videos/Black Female LBP-S.mp4",
    "assets/videos/Black Male LBP-CT.mp4",
    "assets/videos/Black Male LBP-S.mp4",
    "assets/videos/White Female LBP-CT.mp4",
    "assets/videos/White Female LBP-SV1.mp4",
    "assets/videos/White Male LBP-CT.mp4",
    "assets/videos/White Male LBP-S.mp4",
]

# -------------------------
# FUNCTIONS
# -------------------------
def generate_participant_id():
    return str(uuid.uuid4())[:8].upper()

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
    """
    Creates stratum key based on gender and race.
    Participants are grouped into strata to ensure balanced video assignment.
    """
    gender_key = gender if gender in ["Man", "Woman"] else "OtherGender"
    race_key = race if race in ["White", "Black or African American"] else "OtherRace"
    return f"{gender_key}_{race_key}"

def assign_balanced_video(stratum, video_counts):
    """
    Assigns a video using weighted randomization to balance assignments within a stratum.
    
    Args:
        stratum: The demographic stratum (e.g., "Man_White")
        video_counts: Dict of {video_path: count} for this stratum
        
    Returns:
        Selected video path
        
    Logic:
    - If no videos assigned yet in this stratum, pick randomly
    - Otherwise, weight selection inversely by current counts
    - Videos with fewer assignments get higher probability
    """
    if not video_counts or sum(video_counts.values()) == 0:
        # No assignments yet in this stratum - pick randomly
        return random.choice(VIDEO_LIST)
    
    # Calculate weights: videos with FEWER assignments get HIGHER weight
    # Use inverse weighting: weight = (max_count + 1) - current_count
    max_count = max(video_counts.values())
    
    # Build weighted list
    videos = []
    weights = []
    
    for video in VIDEO_LIST:
        current_count = video_counts.get(video, 0)
        # Inverse weight: fewer assignments = higher weight
        weight = (max_count + 1) - current_count
        videos.append(video)
        weights.append(weight)
    
    # Weighted random selection
    selected = random.choices(videos, weights=weights, k=1)[0]
    return selected