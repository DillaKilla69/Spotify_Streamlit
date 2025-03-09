import time

import requests
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError


def validate_credentials(client_id, client_secret):

    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(auth_url, {
        "grant_type": "client_credentials",
        "client_id": st.session_state["client_id"],
        "client_secret": st.session_state["client_secret"],
    })

    print("response code:", response.status_code)

    return response.status_code == 200


def create_sp_session(client_id, client_secret):

    if validate_credentials(client_id, client_secret):
        auth_manager = SpotifyClientCredentials(
            client_id=st.session_state["client_id"], 
            client_secret=st.session_state["client_secret"])
        sp = spotipy.Spotify(auth_manager=auth_manager)

        st.session_state["login"] = True
        st.session_state["sp_session"] = sp
        
        return sp

    else:
        print(client_id, client_secret)
        st.error("error: invalid client_id or client_secret")


@st.dialog("Provide your client_id and client_secret")
def render_login():

    with st.form("enter your Spotify credentials"):
        st.session_state["client_id"] = st.text_input("ed8202519b564c468c54ee4b78e81661")
        st.session_state["client_secret"] = st.text_input("3f37d164acdc4b498ef83f1ca572ad51")

        submitted = st.form_submit_button("submit creds")
        
        if submitted:
            sp = create_sp_session(client_id=st.session_state["client_id"],
                                    client_secret=st.session_state["client_secret"])
            if sp:
                with st.spinner("Authenicating Session..."):
                    time.sleep(3)
                st.success("Authenticated!")
                time.sleep(1)
                st.rerun()