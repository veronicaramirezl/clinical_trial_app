import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import datetime
import gspread.utils

# Google Sheets API scope
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# -------------------------------------------------------
# LOAD SHEET
# -------------------------------------------------------
def get_sheet():
    try:
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)

        client = gspread.authorize(creds)
        return client.open("Clinical_Trial_Data").sheet1

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None


# -------------------------------------------------------
# LOAD PARTICIPANT DATA
# -------------------------------------------------------
def load_participant_data(participant_id):
    """
    Loads user row and returns video URL from column AC (index 28)
    """
    sheet = get_sheet()
    if not sheet:
        return None

    try:
        cell = sheet.find(participant_id)

        if cell:
            row = sheet.row_values(cell.row)
            video_url = row[28] if len(row) > 28 else None  # Column AC index=28

            return {
                "found": True,
                "row_num": cell.row,
                "video_url": video_url,
                "data": row
            }
        else:
            return {"found": False}

    except Exception as e:
        st.error(f"Load Error: {e}")
        return {"found": False}


# -------------------------------------------------------
# SAVE DEMOGRAPHICS  (Cols A to AC)
# -------------------------------------------------------
def save_demographics(user_data):
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_id = user_data.get("participant_id")

        # EXACT FIXED COLUMN ORDER
        row_values = [
            timestamp,                                 # A
            p_id,                                      # B
            user_data.get("age", ""),                  # C
            user_data.get("sex", ""),                  # D
            user_data.get("gender_identity", ""),      # E
            user_data.get("education", ""),            # F
            user_data.get("insurance", ""),            # G
            user_data.get("insurance_type", ""),       # H
            user_data.get("english_proficiency", ""),  # I
            user_data.get("income", ""),               # J
            user_data.get("health_status", ""),        # K
            user_data.get("chronic_conditions", ""),   # L
            user_data.get("visit_frequency", ""),      # M
            user_data.get("trust_web_1", ""),          # N
            user_data.get("trust_web_2", ""),          # O
            user_data.get("trust_web_3", ""),          # P
            user_data.get("mistrust_1", ""),           # Q
            user_data.get("mistrust_2", ""),           # R
            user_data.get("mistrust_3", ""),           # S
            user_data.get("mistrust_4", ""),           # T
            user_data.get("discrim_1", ""),            # U
            user_data.get("discrim_2", ""),            # V
            user_data.get("discrim_3", ""),            # W
            user_data.get("discrim_4", ""),            # X
            user_data.get("discrim_healthcare", ""),   # Y
            user_data.get("nutri_calories", ""),       # Z
            user_data.get("nutri_carbs", ""),          # AA
            user_data.get("nutri_protein", ""),        # AB
            ""                                          # AC (video placeholder)
        ]

        cell = sheet.find(p_id)

        if cell:
            # Write exactly A:AC (29 columns)
            sheet.update(f"A{cell.row}:AC{cell.row}", [row_values])
        else:
            sheet.append_row(row_values)

        return True

    except Exception as e:
        st.error(f"Save Error: {e}")
        return False


# -------------------------------------------------------
# SAVE VIDEO URL (Column AC = 29)
# -------------------------------------------------------
def save_assigned_video(participant_id, video_url):
    sheet = get_sheet()
    if not sheet:
        return

    try:
        cell = sheet.find(participant_id)
        if cell:
            sheet.update_cell(cell.row, 29, video_url)

    except Exception as e:
        print(f"Video Save Error: {e}")


# -------------------------------------------------------
# SAVE FINAL SURVEY (Columns AD–AM)
# -------------------------------------------------------
def save_final_survey(participant_id, survey_data):
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        cell = sheet.find(participant_id)

        if cell:
            values = [
                survey_data.get("Likert_1", ""),
                survey_data.get("Likert_2", ""),
                survey_data.get("Likert_3", ""),
                survey_data.get("Likert_4", ""),
                survey_data.get("Likert_5", ""),
                survey_data.get("Likert_6", ""),
                survey_data.get("Likert_7", ""),
                survey_data.get("Likert_8", ""),
                survey_data.get("Trust_Level", ""),
                survey_data.get("Competence", "")
            ]

            start_col = 30   # AD
            end_col = start_col + len(values) - 1  # AM

            start_a1 = gspread.utils.rowcol_to_a1(cell.row, start_col)
            end_a1 = gspread.utils.rowcol_to_a1(cell.row, end_col)

            sheet.update(f"{start_a1}:{end_a1}", [values])
            return True

        else:
            st.error("Error: Participant ID not found in sheet.")
            return False

    except Exception as e:
        st.error(f"Survey Save Error: {e}")
        return False
