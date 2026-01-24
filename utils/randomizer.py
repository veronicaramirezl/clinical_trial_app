import random
import streamlit as st
import uuid

# 8 Private YouTube Videos (Placeholders)


VIDEO_LIST = [
    "https://youtu.be/1_FI9K4kI6Y",
    "https://youtu.be/0qsSkuKcpSc",
    "https://youtu.be/r-Lb4GMRJqE",
    "https://youtu.be/d91zMMHgNs0",
    "https://youtu.be/HxI5QC9HzdU",
    "https://youtu.be/zgecejuWgZ8",
    "https://youtu.be/BvTEQL3VKvo"
]

st.title("Videos")

for url in VIDEO_LIST:
    st.video(url)


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