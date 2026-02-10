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
            video_url = row[29] if len(row) > 29 else None  # Column AC index=29

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
        p_id = user_data["participant_id"]

        # Force string values for Google Sheets
        def clean(v):
            return "" if v is None else str(v)

        row_values = [
            clean(timestamp),                 # A (col 1)
            clean(p_id),                      # B (col 2)
            clean(user_data.get("age")),      # C (col 3)
            clean(user_data.get("sex")),      # D (col 4)
            clean(user_data.get("gender_identity")),  # E (col 5)
            clean(user_data.get("race")),      # F (col 6)
            clean(user_data.get("education")),         # G (col 7)
            clean(user_data.get("insurance")),         # H (col 8)
            clean(user_data.get("insurance_type")),    # I (col 9)
            clean(user_data.get("english_proficiency")), # J (col 10)
            clean(user_data.get("income")),              # K (col 11)
            clean(user_data.get("health_status")),       # L (col 12)
            clean(user_data.get("chronic_conditions")),  # M (col 13)
            clean(user_data.get("visit_frequency")),     # N (col 14)
            clean(user_data.get("trust_web_1")),         # O (col 15)
            clean(user_data.get("trust_web_2")),         # P (col 16)
            clean(user_data.get("trust_web_3")),         # Q (col 17)
            clean(user_data.get("mistrust_1")),          # R (col 18)
            clean(user_data.get("mistrust_2")),          # S (col 19)
            clean(user_data.get("mistrust_3")),          # T (col 20)
            clean(user_data.get("mistrust_4")),          # U (col 21)
            clean(user_data.get("discrim_1")),           # V (col 22)
            clean(user_data.get("discrim_2")),           # W (col 23)
            clean(user_data.get("discrim_3")),           # X (col 24)
            clean(user_data.get("discrim_4")),           # Y (col 25)
            clean(user_data.get("discrim_healthcare")),  # Z (col 26)
            clean(user_data.get("nutri_calories")),      # AA (col 27)
            clean(user_data.get("nutri_carbs")),         # AB (col 28)
            clean(user_data.get("nutri_protein")),       # AC (col 29)
            "",                                           # AD (col 30) video URL placeholder
            ""                                            # AE (col 31) stratum placeholder
        ]

        # Lookup row - search in column B only for efficiency
        try:
            cell = sheet.find(p_id, in_column=2)
        except:
            cell = None

        if cell:
            # Update existing row - use proper range notation
            range_notation = f"A{cell.row}:AD{cell.row}"
            sheet.update(range_notation, [row_values], value_input_option='RAW')
        else:
            # Append new row
            sheet.append_row(row_values, value_input_option='RAW')

        return True

    except Exception as e:
        st.error(f"Save Error: {e}")
        return False


# -------------------------------------------------------
# SAVE VIDEO URL (Column AC = 29)
# -------------------------------------------------------
def save_assigned_video(participant_id, video_url, stratum):
    sheet = get_sheet()
    if not sheet:
        return

    try:
        cell = sheet.find(participant_id, in_column=2)
        if cell:
            sheet.update_cell(cell.row, 30, video_url)  # AD
            sheet.update_cell(cell.row, 31, stratum)    # AE

    except Exception as e:
        print(f"Video Save Error: {e}")
        
def get_video_counts_for_stratum(stratum):
    sheet = get_sheet()
    if not sheet:
        return {}

    records = sheet.get_all_values()[1:]  # skip header

    counts = {}
    for row in records:
        if len(row) > 30 and row[30] == stratum:  # AE index = 30
            video = row[29]  # AD index = 29
            if video:
                counts[video] = counts.get(video, 0) + 1

    return counts


# -------------------------------------------------------
# SAVE FINAL SURVEY (Columns AD–AM)
# -------------------------------------------------------
def save_final_survey(participant_id, survey_data):
    sheet = get_sheet()
    if not sheet:
        return False

    try:
        cell = sheet.find(participant_id, in_column=2)

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

            # AD is column 30, AM is column 39
            start_col = 32   # AF
            end_col = start_col + len(values) - 1  # AM

            start_a1 = gspread.utils.rowcol_to_a1(cell.row, start_col)
            end_a1 = gspread.utils.rowcol_to_a1(cell.row, end_col)

            range_notation = f"{start_a1}:{end_a1}"
            sheet.update(range_notation, [values], value_input_option='RAW')
            return True

        else:
            st.error("Error: Participant ID not found in sheet.")
            return False

    except Exception as e:
        st.error(f"Survey Save Error: {e}")
        return False