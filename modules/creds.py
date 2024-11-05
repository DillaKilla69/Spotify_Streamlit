import spotipy
import requests
from spotipy.oauth2 import SpotifyOauthError
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st


def validate_credentials(client_id, client_secret):

    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(auth_url, {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    })

    return response.status_code == 200


def create_sp_session(client_id, client_secret):

    if validate_credentials(client_id, client_secret):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        st.session_state["login"] = True
        st.session_state["sp_session"] = sp
        
        return sp

    else:
        st.error("error: invalid client_id or client_secret")


@st.dialog("login:")
def render_login():

    st.title("enter you client_id and client_secret")

    with st.form("enter your Spotify credentials"):
        st.session_state["client_id"] = st.text_input("e18a33b810214ef997ebd806aaf48f0e")
        st.session_state["client_secret"] = st.text_input("a69ff972d459452987b5d7094d923eaf")

        submitted = st.form_submit_button("submit creds")
        
        if submitted:
            sp = create_sp_session(client_id=st.session_state["client_id"],
                                    client_secret=st.session_state["client_secret"])
            if sp:
                st.rerun()