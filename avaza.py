# import requests
# import json
# import streamlit as st

# def push_to_schedule(user_id, token):
#     # Define the URL for the API endpoint
#     url = "https://api.avaza.com/ScheduleSeries/AddBooking"

#     # Define the payload with your data
#     payload = {
#         "UserIDFK": user_id,
#         "HoursPerDay": 5,
#         "DurationType": "HoursPerDay",
#         "ScheduleOnDaysOff": True,
#         "ProjectIDFK": 91321,
#         "CategoryIDFK": 40840,
#         "TaskIDFK": 1062024,
#         "StartDate": "2024-06-19T12:47:06.367Z",
#         "EndDate": "2024-06-19T12:47:06.367Z"
#     }

#     # Define the headers with the OAuth token
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': f'Bearer {token}'
#     }

#     # Send the POST request to the API
#     response = requests.post(url, headers=headers, data=json.dumps(payload))

#     # Check the response status
#     if response.status_code == 200:
#         st.success("Booking added successfully!")
#         st.json(response.json())
#     else:
#         st.error("Failed to add booking.")
#         st.write(f"Status Code: {response.status_code}")
#         st.write(response.text)



#########WORKING

import requests
import json
import streamlit as st
from datetime import datetime

def get_existing_bookings(token, user_id, start_date, end_date):
    base_url = "https://api.avaza.com/api/ScheduleSeries"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Ensure dates are in the correct format
    formatted_start_date = format_date(start_date)
    formatted_end_date = format_date(end_date)

    params = {
        'UserID': user_id,
        # 'ScheduleEndDateFrom': formatted_start_date,
        # 'ScheduleEndDateTo': formatted_end_date
    }
    response = requests.get(base_url, headers=headers, params=params)
    full_url = response.url  # Capture the full URL for debugging
    if response.status_code == 200:
        bookings = response.json()
        st.write("Existing bookings retrieved successfully:")
        #st.json(bookings)  # Debug: Show existing bookings
        st.write(f"URL with params: {full_url}")  # Debug: Print the URL with params
        return bookings
    else:
        st.error("Failed to retrieve existing bookings.")
        st.write(f"Status Code: {response.status_code}")
        st.write(response.text)
        st.write(f"URL with params: {full_url}")  # Debug: Print the URL with params
        return None

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.strftime("%Y-%m-%dT%H:%M:%S")

def parse_date(date_str):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date format for {date_str} is not supported.")

def booking_exists(existing_bookings, payload):
    for booking in existing_bookings['ScheduleSeries']:
        try:
            # Debug: Show each booking being checked
            #st.write(f"Checking booking: {booking}") 
            if (booking.get('UserIDFK') == payload['UserIDFK'] and
                booking.get('ProjectIDFK') == payload['ProjectIDFK'] and
                booking.get('TaskIDFK') == payload['TaskIDFK'] and
                # parse_date(booking.get('StartDate')) == parse_date(payload['StartDate']) and
                # parse_date(booking.get('EndDate')) == parse_date(payload['EndDate']) and
                booking.get('Notes') == payload['Notes']):
                st.write("Match found: This booking already exists.")  # Debug: Match found
                return True
        except (KeyError, TypeError, ValueError):
            continue
    return False

def push_to_schedule(user_id, token):
    # Define the URL for the API endpoint
    url = "https://api.avaza.com/ScheduleSeries/AddBooking"

    # Define the payload with your data
    payload = {
        "UserIDFK": user_id,
        "HoursPerDay": 5,
        "DurationType": "HoursPerDay",
        "ScheduleOnDaysOff": True,
        "ProjectIDFK": 91321,
        "CategoryIDFK": 40840,
        "TaskIDFK": 1062024,
        "Notes": "Test note",
        "StartDate": "2024-06-19T12:47:06.367Z",
        "EndDate": "2024-06-19T12:47:06.367Z"
    }

    # Use the payload data to refine the search for existing bookings
    existing_bookings = get_existing_bookings(token, user_id, payload['StartDate'], payload['EndDate'])
    if existing_bookings and booking_exists(existing_bookings, payload):
        st.info("Booking already exists, not adding a new one.")
        return

    # Define the headers with the OAuth token
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Send the POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response status
    if response.status_code == 200:
        st.success("Booking added successfully!")
        #st.json(response.json())
    else:
        st.error("Failed to add booking.")
        st.write(f"Status Code: {response.status_code}")
        st.write(response.text)
