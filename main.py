import streamlit as st

st.set_page_config(
    page_title="Neurosurgery Clinical Trial",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Sidebar Navigation
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    section[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state for data storage
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}
    
    st.title("Clinical Trial Study")
    st.info("Redirecting to Welcome Page...")
    st.switch_page("pages/1_welcome.py")

if __name__ == "__main__":
    main()