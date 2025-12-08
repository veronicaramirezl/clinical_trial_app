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

def get_gspread_client():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Google Sheets Auth Error: {e}")
        return None

def get_participant_by_id(participant_id):
    """
    Searches for a participant ID in the sheet.
    Returns the row data (dict) if found, else None.
    """
    client = get_gspread_client()
    if not client: return None
    
    try:
        sheet = client.open("Clinical_Trial_Data").sheet1
        # Search for the cell containing the ID
        cell = sheet.find(participant_id)
        
        if cell:
            # Get all values in that row to repopulate session state if needed
            row_values = sheet.row_values(cell.row)
            # We return a basic dict assuming column 2 is ID, 3 is Age, etc.
            # (Adjust indices based on your write_row order)
            return {
                "found": True,
                "row_num": cell.row,
                "age": row_values[2] if len(row_values) > 2 else "",
                "sex": row_values[3] if len(row_values) > 3 else "",
                # Add others if you want to fully restore the form
            }
        return None
    except gspread.exceptions.CellNotFound:
        return None
    except Exception as e:
        st.error(f"Lookup Error: {e}")
        return None

def write_row(user_data, questionnaire_data, video_url):
    """
    Updates the row if ID exists, otherwise Appends a new row.
    """
    client = get_gspread_client()
    if not client: return False

    try:
        sheet = client.open("Clinical_Trial_Data").sheet1
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_id = user_data.get("participant_id", "")
        
        # Prepare the full data row
        row_data = [
            timestamp,
            p_id,
            user_data.get("age", ""),
            user_data.get("sex", ""),
            user_data.get("gender_identity", ""),
            user_data.get("education", ""),
            user_data.get("insurance", ""),
            user_data.get("income", ""),
            str(user_data), # Full dump just in case
            video_url,
            # Survey Data
            questionnaire_data.get("Likert_1", ""),
            questionnaire_data.get("Likert_2", ""),
            questionnaire_data.get("Likert_3", ""),
            questionnaire_data.get("Likert_4", ""),
            questionnaire_data.get("Likert_5", ""),
            questionnaire_data.get("Likert_6", ""),
            questionnaire_data.get("Likert_7", ""),
            questionnaire_data.get("Likert_8", ""),
            questionnaire_data.get("Trust_Level", ""),
            questionnaire_data.get("Competence", "")
        ]

        # 1. Check if user exists
        try:
            cell = sheet.find(p_id)
            # UPDATE existing row
            # We start at col 1. update_cell(row, col, val) is slow loop.
            # Better to use update() with a range.
            # Example: A{row}:T{row}
            # Note: This overwrites the whole row with the new data
            sheet.update(f"A{cell.row}:T{cell.row}", [row_data])
            return True
            
        except gspread.exceptions.CellNotFound:
            # APPEND new row
            sheet.append_row(row_data)
            return True
            
    except Exception as e:
        st.error(f"Write Error: {e}")
        return False