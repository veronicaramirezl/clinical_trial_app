import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import datetime

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
        client = gspread.authorize(creds)
        # Opens the first sheet of the workbook
        return client.open("Clinical_Trial_Data").sheet1
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def load_participant_data(participant_id):
    """
    Fetches the user's progress from the sheet.
    """
    sheet = get_sheet()
    if not sheet: return None

    try:
        # UPDATED: find() now returns None if not found, it does not error.
        cell = sheet.find(participant_id)
        
        if cell:
            row_values = sheet.row_values(cell.row)
            # Check if video (Col 11) is already assigned. 
            # (Index 10 because python lists start at 0)
            video_url = row_values[10] if len(row_values) > 10 else None
            
            return {
                "found": True,
                "row_num": cell.row,
                "video_url": video_url,
                "data": row_values
            }
        else:
            return {"found": False}
            
    except Exception as e:
        # Catch other unforeseen errors
        st.error(f"Load Error: {e}")
        return {"found": False}

def save_demographics(user_data):
    """Creates the initial row with demographics or updates if exists."""
    sheet = get_sheet()
    if not sheet: return False

    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_id = user_data.get("participant_id")
        
        # Format: [Timestamp, ID, Age, Sex, Gender, Edu, Insur, Income, FullDict, VideoPlaceholder]
        row_values = [
            timestamp,
            p_id,
            user_data.get("age", ""),
            user_data.get("sex", ""),
            user_data.get("gender_identity", ""),
            user_data.get("education", ""),
            user_data.get("insurance", ""),
            user_data.get("income", ""),
            str(user_data), 
            "" # Column 10 (J) Video URL Placeholder
        ]
        
        # UPDATED LOGIC: Check if cell exists first
        cell = sheet.find(p_id)
        
        if cell:
            # If exists, update the demographics part (Columns A-I)
            # Row number is cell.row
            sheet.update(range_name=f"A{cell.row}:I{cell.row}", values=[row_values[:-1]])
        else:
            # If not found, append new row
            sheet.append_row(row_values)
            
        return True
    except Exception as e:
        st.error(f"Save Error: {e}")
        return False

def save_assigned_video(participant_id, video_url):
    """Updates ONLY the video column for an existing user."""
    sheet = get_sheet()
    if not sheet: return

    try:
        cell = sheet.find(participant_id)
        if cell:
            # Video is Column 11 (K). 
            sheet.update_cell(cell.row, 11, video_url)
    except Exception as e:
        print(f"Video Save Error: {e}")

def save_final_survey(participant_id, survey_data):
    """Updates the survey columns."""
    sheet = get_sheet()
    if not sheet: return False

    try:
        cell = sheet.find(participant_id)
        
        if cell:
            # Prepare survey values list
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
            
            # Update starting from Column 12 (L)
            sheet.update(range_name=f"L{cell.row}:U{cell.row}", values=[values])
            return True
        else:
            st.error("Error: Participant ID not found in sheet to save survey.")
            return False
            
    except Exception as e:
        st.error(f"Survey Save Error: {e}")
        return False