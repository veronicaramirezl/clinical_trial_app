import streamlit as st

# Hide sidebar and center content
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .centered {text-align: center;}
    .big-button button {font-size: 18px; padding: 0.75em 1em;}
</style>
""", unsafe_allow_html=True)

st.title("Patient Education Research Study")
st.subheader("Department of Neurosurgery")

# Centered Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("assets/logo/logo.png", use_container_width=True)
    except:
        pass

# --- MAIN INFORMATION ---
st.markdown("""
### Welcome

Thank you for your interest in this research study. We are examining how patients understand and interpret medical information when it is presented by different types of physicians in online educational videos. Your participation will help us improve the clarity, trustworthiness, and effectiveness of neurosurgical patient education materials.

### What You Will Do

Participation takes approximately **10 to 15 minutes**. The study has three parts:

1. **Short Background Survey** You will answer questions about demographics, health history, and your general trust in online medical information.

2. **Educational Video** You will watch a brief video explaining a neurosurgical topic.

3. **Post-Video Survey** You will complete a second questionnaire assessing your impression of the presenter, your trust in the information, and how the video influenced your understanding.

Both surveys are based on validated research instruments and have been shortened for clarity and ease of completion.

### Privacy and Confidentiality

* **Anonymous participation** We will not collect your name, contact information, or any personally identifying details.

* **Secure data storage** Your responses are stored in a secure system and used only for academic research.

* **Voluntary participation** You may stop at any time without penalty or explanation.
""")

st.divider()

# --- SECURITY SECTION ---
st.subheader("Study Access")

# CHANGE PASSWORD HERE IF NEEDED
SECRET_PASSWORD = "NEURO2025"

access_code = st.text_input("Please enter the Access Code to begin:", type="password")

if access_code == SECRET_PASSWORD:
    st.success("Access Granted.")
    
    # --- CONSENT SECTION (Only visible after password) ---
    st.markdown("""
    ### Consent to Participate

    By clicking the button below, you confirm that:

    * You are **18 years of age or older**
    * You have read and understood the information above
    * You voluntarily agree to participate in this study
    """)

    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        if st.button("I Agree and Begin", type="primary", use_container_width=True):
            st.switch_page("pages/2_demographics.py")

elif access_code:
    st.error("Incorrect Access Code. Please contact the research team.")
else:
    st.info("🔒 This study is password protected. Please enter the code above.")