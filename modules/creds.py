import time

import requests
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials


def validate_credentials(client_id, client_secret):

    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        auth_url,
        {
            "grant_type": "client_credentials",
            "client_id": st.session_state["client_id"],
            "client_secret": st.session_state["client_secret"],
        },
    )

    print("response code:", response.status_code)

    if response.status_code == 200:
        print("response code:", response.status_code)
        return response.status_code

    else:
        print("nah, you fucked up!")


def create_sp_session(client_id, client_secret):

    if validate_credentials(client_id, client_secret) == 200:
        auth_manager = SpotifyClientCredentials(
            client_id=st.session_state["client_id"],
            client_secret=st.session_state["client_secret"],
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)

        st.session_state["show_login_dialog"] = True
        st.session_state["sp_session"] = sp

        return sp

    else:
        print(client_id, client_secret)
        st.error("error: invalid client_id or client_secret")


# @st.dialog("Enter Credentials")
# def render_login():
#     with st.form("enter your Spotify credentials"):
#         st.session_state["client_id"] = st.text_input(
#             "ed8202519b564c468c54ee4b78e81661", placeholder="client_id"
#         )

#         st.session_state["client_secret"] = st.text_input(
#             "3f37d164acdc4b498ef83f1ca572ad51",
#             type="password",
#             placeholder="client_password",
#         )

#         submitted = st.form_submit_button("Submit Credentials")

#         if submitted:
#             sp = create_sp_session(
#                 client_id=st.session_state["client_id"],
#                 client_secret=st.session_state["client_secret"],
#             )

#             if sp:
#                 with st.spinner("Authenicating Session...", show_time=True):
#                     time.sleep(3)
#                 st.success("Authenticated!")
#                 time.sleep(1)
#                 st.session_state["logged_in"] = True
#                 st.session_state["show_login_dialog"] = False
#                 st.session_state["trigger_rerun"] = (
#                     True  # Ensure main.py detects the change
#                 )
#                 st.rerun()
