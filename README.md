# 🧠 Neurosurgery & Racial Equity Clinical Trial App

A secure, web-based clinical trial application built with **Python** and **Streamlit**. This tool is designed to conduct randomized controlled trials (RCTs) assessing patient perception of medical information, specifically focusing on racial equity in neurosurgery.

## 📋 Features

* **Automated Randomization:** Participants are randomly assigned one of 8 private educational videos.
* **Session Restoration:** Generates a unique "Return Code" (Participant ID) allowing users to pause and resume their session without losing data.
* **Google Sheets Database:** All data (demographics, video assignment, survey responses) is saved instantly to a secure Google Sheet.
* **Smart Logic:** Prevents users from "re-rolling" for a different video; once assigned, the video is locked to their ID.
* **Full Questionnaire Suite:** Includes validated scales for Medical Mistrust, Health Literacy, and Discrimination.

---

## 📂 Project Structure

```text
clinical_trial_app/
├── main.py                   # Entry point (handles redirection)
├── requirements.txt          # Python dependencies
├── service_account.json      # (YOU MUST CREATE THIS) Google API Keys
├── README.md                 # Project documentation
├── assets/
│   └── logo/
│       └── logo.png          # App branding
├── pages/
│   ├── 1_welcome.py          # Consent & Intro
│   ├── 2_demographics.py     # Login, Return Code & Background Survey
│   ├── 3_video_randomizer.py # Video Assignment & Viewing
│   ├── 4_questionnaire.py    # Post-intervention Survey
│   └── 5_finish.py           # Completion Page
└── utils/
    ├── google_sheets.py      # API Connection & Data Saving Logic
    └── randomizer.py         # ID Generation & Randomization Logic