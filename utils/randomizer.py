import random
import streamlit as st
import uuid

# 8 Private YouTube Videos (Placeholders)
VIDEO_LIST = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=E8gmARGvPlI",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=eDwi-8n054s",
    "https://www.youtube.com/watch?v=kBYHwH1Vb-c",
    "https://www.youtube.com/watch?v=dLl4PZtxia8",
    "https://www.youtube.com/watch?v=f_X5A-BYjO8",
    "https://www.youtube.com/watch?v=LXIWRan3XGY",
]

def generate_participant_id():
    """Generates a unique short ID for the user."""
    return str(uuid.uuid4())[:8].upper()

def get_random_video():
    """Selects a random video."""
    return random.choice(VIDEO_LIST)

def initialize_session_state():
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}
    if 'demographics_complete' not in st.session_state:
        st.session_state['demographics_complete'] = False
    if 'assigned_video' not in st.session_state:
        st.session_state['assigned_video'] = None