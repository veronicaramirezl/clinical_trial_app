import random
import streamlit as st
import uuid

# 8 Private YouTube Videos (Placeholders)


VIDEO_LIST = [
    "https://www.youtube.com/watch?v=r-Lb4GMRJqE",
    "https://www.youtube.com/watch?v=0qsSkuKcpSc",
    "https://www.youtube.com/watch?v=r-Lb4GMRJqE",
    "https://www.youtube.com/watch?v=d91zMMHgNs0",
    "https://www.youtube.com/watch?v=HxI5QC9HzdU",
    "https://www.youtube.com/watch?v=zgecejuWgZ8",
    "https://www.youtube.com/watch?v=BvTEQL3VKvo"
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
        
def normalize_youtube_url(url):
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url
