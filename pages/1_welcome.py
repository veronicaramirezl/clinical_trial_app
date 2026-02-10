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

Thank you for your interest in this research study. This study examines how people understand and evaluate medical information presented in online educational videos related to spine care. Your participation will help improve how educational health information is developed and communicated to patients.

### What You Will Do

Participation takes approximately **10 to 15 minutes** and includes three parts:

1. **Background Survey** You will answer brief questions about your demographics, health background, and general use of online medical information.

2. **Educational Video** You will watch a short educational video explaining a topic related to treatment options or clinical trials for back pain.

3. **Post-Video Survey** You will complete a questionnaire about your impressions of the video, the presenter, and the information provided. 

The survey questions are adapted from established research instruments and have been shortened to reduce burden.

### About the Video Content 

The educational video features a digitally generated clinician delivering standardized medical information. All videos use the same script and content. Minor visual artifacts may be present. The video is for research and educational purposes only and does not provide personal medical advice.

### Privacy and Voluntary Participation

* **Anonymous participation** No names, contact information, or direct identifiers are collected.

* **Confidentiality** Responses are stored securely and used only for research purposes.

* **Voluntary participation** Your participation is voluntary, and you may stop at any time without penalty.
""")

st.divider()

# --- CONSENT SECTION ---
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
