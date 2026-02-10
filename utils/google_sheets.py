import gspread
from google.oauth2.service_account import Credentials
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
    """Connect to Google Sheets using service account credentials"""
    try:
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        else:
            creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)

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
    Loads participant row and returns video URL from column AD (index 29)
    Column mapping:
    - A-AB: Demographics (indices 0-27)
    - AC: Nutrition protein (index 28)
    - AD: Video URL (index 29)
    - AE: Stratum (index 30)
    - AF-AO: Survey responses (indices 31-40)
    """
    sheet = get_sheet()
    if not sheet:
        return None

    try:
        cell = sheet.find(participant_id, in_column=2)  # Search column B (participant_id)

        if cell:
            row = sheet.row_values(cell.row)
            video_url = row[29] if len(row) > 29 else None  # Column AD (index 29)
            stratum = row[30] if len(row) > 30 else None    # Column AE (index 30)

            return {
                "found": True,
                "row_num": cell.row,
                "video_url": video_url,
                "stratum": stratum,
                "data": row
            }
        else:
            return {"found": False}

    except gspread.exceptions.CellNotFound:
        return {"found": False}
    except Exception as e:
        st.error(f"Load Error: {e}")
        return {"found": False}


# -------------------------------------------------------
# SAVE DEMOGRAPHICS (Cols A to AC)
# -------------------------------------------------------
def save_demographics(user_data):
    """
    Save demographic and baseline data to columns A-AC
    Columns AD (video) and AE (stratum) are left empty for later assignment
    """
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_id = user_data["participant_id"]

        # Force string values for Google Sheets
        def clean(v):
            return "" if v is None else str(v)

        # Build row: A (timestamp) through AC (nutri_protein) = 29 columns
        row_values = [
            clean(timestamp),                           # A  (index 0)
            clean(p_id),                                # B  (index 1)
            clean(user_data.get("age")),                # C  (index 2)
            clean(user_data.get("sex")),                # D  (index 3)
            clean(user_data.get("gender_identity")),    # E  (index 4)
            clean(user_data.get("race")),               # F  (index 5)
            clean(user_data.get("education")),          # G  (index 6)
            clean(user_data.get("insurance")),          # H  (index 7)
            clean(user_data.get("insurance_type")),     # I  (index 8)
            clean(user_data.get("english_proficiency")),# J  (index 9)
            clean(user_data.get("income")),             # K  (index 10)
            clean(user_data.get("health_status")),      # L  (index 11)
            clean(user_data.get("chronic_conditions")), # M  (index 12)
            clean(user_data.get("visit_frequency")),    # N  (index 13)
            clean(user_data.get("trust_web_1")),        # O  (index 14)
            clean(user_data.get("trust_web_2")),        # P  (index 15)
            clean(user_data.get("trust_web_3")),        # Q  (index 16)
            clean(user_data.get("mistrust_1")),         # R  (index 17)
            clean(user_data.get("mistrust_2")),         # S  (index 18)
            clean(user_data.get("mistrust_3")),         # T  (index 19)
            clean(user_data.get("mistrust_4")),         # U  (index 20)
            clean(user_data.get("discrim_1")),          # V  (index 21)
            clean(user_data.get("discrim_2")),          # W  (index 22)
            clean(user_data.get("discrim_3")),          # X  (index 23)
            clean(user_data.get("discrim_4")),          # Y  (index 24)
            clean(user_data.get("discrim_healthcare")), # Z  (index 25)
            clean(user_data.get("nutri_calories")),     # AA (index 26)
            clean(user_data.get("nutri_carbs")),        # AB (index 27)
            clean(user_data.get("nutri_protein")),      # AC (index 28)
            "",                                         # AD (index 29) - video URL (filled later)
            ""                                          # AE (index 30) - stratum (filled later)
        ]

        # Look up existing participant
        try:
            cell = sheet.find(p_id, in_column=2)  # Column B
        except gspread.exceptions.CellNotFound:
            cell = None

        if cell:
            # Update existing row A through AE
            range_notation = f"A{cell.row}:AE{cell.row}"
            sheet.update(range_notation, [row_values], value_input_option='RAW')
            st.success(f"Updated existing record for participant {p_id}")
        else:
            # Append new row
            sheet.append_row(row_values, value_input_option='RAW')
            st.success(f"Created new record for participant {p_id}")

        return True

    except Exception as e:
        st.error(f"Save Error: {e}")
        return False


# -------------------------------------------------------
# SAVE VIDEO URL (Column AD) and STRATUM (Column AE)
# -------------------------------------------------------
def save_assigned_video(participant_id, video_url, stratum):
    """
    Save video assignment to column AD (index 29) and stratum to AE (index 30)
    """
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        cell = sheet.find(participant_id, in_column=2)  # Column B
        
        if cell:
            # Batch update both cells at once for efficiency
            range_notation = f"AD{cell.row}:AE{cell.row}"
            sheet.update(range_notation, [[video_url, stratum]], value_input_option='RAW')
            return True
        else:
            st.error(f"Participant {participant_id} not found in sheet")
            return False

    except Exception as e:
        st.error(f"Video Save Error: {e}")
        return False


# -------------------------------------------------------
# GET VIDEO COUNTS FOR STRATUM (for randomization balancing)
# -------------------------------------------------------
def get_video_counts_for_stratum(stratum):
    """
    Count how many times each video has been assigned within a stratum
    Used for balanced randomization
    """
    sheet = get_sheet()
    if not sheet:
        return {}

    try:
        # Get all data at once (more efficient than row-by-row)
        records = sheet.get_all_values()[1:]  # Skip header row

        counts = {}
        for row in records:
            # Check if row has stratum column (AE = index 30)
            if len(row) > 30 and row[30] == stratum:
                video = row[29] if len(row) > 29 else None  # AD = index 29
                if video and video.strip():  # Only count non-empty videos
                    counts[video] = counts.get(video, 0) + 1

        return counts

    except Exception as e:
        st.error(f"Error getting video counts: {e}")
        return {}


# -------------------------------------------------------
# SAVE FINAL SURVEY (Columns AF–AO)
# -------------------------------------------------------
def save_final_survey(participant_id, survey_data):
    """
    Save post-video survey responses to columns AF-AO
    Column mapping:
    - AF: Likert_1 (index 31)
    - AG: Likert_2 (index 32)
    - AH: Likert_3 (index 33)
    - AI: Likert_4 (index 34)
    - AJ: Likert_5 (index 35)
    - AK: Likert_6 (index 36)
    - AL: Likert_7 (index 37)
    - AM: Likert_8 (index 38)
    - AN: Trust_Level (index 39)
    - AO: Competence (index 40)
    """
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        cell = sheet.find(participant_id, in_column=2)  # Column B

        if cell:
            # Clean survey data
            def clean(v):
                return "" if v is None else str(v)

            values = [
                clean(survey_data.get("Likert_1")),      # AF
                clean(survey_data.get("Likert_2")),      # AG
                clean(survey_data.get("Likert_3")),      # AH
                clean(survey_data.get("Likert_4")),      # AI
                clean(survey_data.get("Likert_5")),      # AJ
                clean(survey_data.get("Likert_6")),      # AK
                clean(survey_data.get("Likert_7")),      # AL
                clean(survey_data.get("Likert_8")),      # AM
                clean(survey_data.get("Trust_Level")),   # AN
                clean(survey_data.get("Competence"))     # AO
            ]

            # AF is column 32 (index 31), AO is column 41 (index 40)
            range_notation = f"AF{cell.row}:AO{cell.row}"
            sheet.update(range_notation, [values], value_input_option='RAW')
            
            st.success("Survey responses saved successfully")
            return True

        else:
            st.error("Error: Participant ID not found in sheet")
            return False

    except Exception as e:
        st.error(f"Survey Save Error: {e}")
        return False


# -------------------------------------------------------
# HELPER: Get all participant IDs (useful for validation)
# -------------------------------------------------------
def get_all_participant_ids():
    """Return list of all participant IDs in the sheet"""
    sheet = get_sheet()
    if not sheet:
        return []
    
    try:
        # Get column B (participant IDs), skip header
        ids = sheet.col_values(2)[1:]
        return [id for id in ids if id.strip()]
    except Exception as e:
        st.error(f"Error fetching participant IDs: {e}")
        return []