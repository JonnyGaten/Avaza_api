import streamlit as st
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient
import os
import json
from dotenv import load_dotenv


load_dotenv()


# Replace these with your Avaza app details
# client_id = os.getenv('AVAZA_CLIENT_ID')
# client_secret = os.getenv('AVAZA_CLIENT_SECRET')
client_id = st.secrets["avaza"]["AVAZA_CLIENT_ID"]
client_secret = st.secrets["avaza"]["AVAZA_CLIENT_SECRET"]
authorization_base_url = 'https://any.avaza.com/oauth2/authorize'
token_url = 'https://any.avaza.com/oauth2/token'
redirect_uri = st.secrets["avaza"]["RETURN_URL"]

# Disable the InsecureTransportError for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the OAuth client
client = WebApplicationClient(client_id)

st.title("Avaza OAuth Authentication")

# Step 1: User Authorization.
if 'oauth_token' not in st.session_state:
    try:
        # Generate the authorization URL
        authorization_url = client.prepare_request_uri(
            authorization_base_url,
            redirect_uri=redirect_uri
        )
        # st.write(f"### [Click here to authorize]({authorization_url})")
    except Exception as e:
        st.error(f"An error occurred while generating the authorization URL: {str(e)}")

# Step 2: Retrieving an access token.
query_params = st.query_params
code = query_params.get('code')
if code and 'oauth_token' not in st.session_state:
    code = code  # Extract the code from the list
    authorization_response_url = f"{redirect_uri}?code={code}"

    # Debug: Print authorization_response_url to ensure it's correct
    # st.write(f"Authorization Response URL: {authorization_response_url}")

    try:
        oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri)
        token_response = oauth_session.fetch_token(
            token_url=token_url,
            code=code,
            client_secret=client_secret,
            client_id=client_id,
            include_client_id=True
        )
        st.session_state.oauth_token = token_response

        # Debug: Print token response to ensure it's being set
        # st.write(f"Token Response: {token_response}")
    except Exception as e:
        st.error(f"An error occurred while fetching the token: {str(e)}")

# Step 3: Use the token to access Avaza API and get user ID and Email
if 'oauth_token' in st.session_state:
    oauth2_session = OAuth2Session(client_id, token=st.session_state.oauth_token)
    response = oauth2_session.get('https://api.avaza.com/api/UserProfile?CurrentUserOnly=true')
    if response.status_code == 200:
        user_data = response.json()
        if 'Users' in user_data and len(user_data['Users']) > 0:
            user_id = user_data['Users'][0].get('UserID', 'N/A')
            user_email = user_data['Users'][0].get('Email', 'N/A')
            st.success(f"Connected to Avaza API successfully! User ID: {user_id}, User Email: {user_email}")
            # st.json(user_data)
        else:
            st.error("User data not found.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Push example to Schedule'):
                st.write("Push to Schedule Button Clicked")
                # Add functionality to call the scheduling function
                import avaza
                avaza.push_to_schedule(user_id, st.session_state.oauth_token['access_token'])
        with col2:
            if st.button('Get schedule for next 2 weeks'):
                st.write("Get Schedule Button Clicked")
                # Add functionality to call the scheduling function
                import twoweeks
                twoweeks.get_schedule(user_id, st.session_state.oauth_token['access_token'])


    else:
        st.error("Failed to connect to Avaza API.")
        st.write(response.text)
else:
    try:
        # Generate the authorization URL
        authorization_url = client.prepare_request_uri(
            authorization_base_url,
            redirect_uri=redirect_uri
        )
        # st.write(f"### [Authorize Avaza]({authorization_url})")
        if st.button('Authorize Avaza'):
            st.write(f"[Click here to authorize]({authorization_url})")
    except Exception as e:
        st.error(f"An error occurred while generating the authorization URL: {str(e)}")