import requests
import json
import streamlit as st
from datetime import datetime, timedelta

def get_schedule(user_id, token):
    base_url = "https://api.avaza.com/api/ScheduleAssignment"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    today = datetime.now().strftime("%Y-%m-%d")
    two_weeks_later = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    params = {
        'UserID': user_id,
        'ScheduleDateFrom': today,
        'ScheduleDateTo': two_weeks_later
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    full_url = response.url  # Capture the full URL for debugging
    if response.status_code == 200:
        schedule = response.json()
        st.write("Schedule for the next 2 weeks retrieved successfully:")
        st.json(schedule)  # Debug: Show the schedule
        st.write(f"get URL with params: {full_url}")  # Debug: Print the URL with params
        return schedule
    else:
        st.error("Failed to retrieve schedule.")
        st.write(f"Status Code: {response.status_code}")
        st.write(response.text)
        st.write(f"URL with params: {full_url}")  # Debug: Print the URL with params
        return None