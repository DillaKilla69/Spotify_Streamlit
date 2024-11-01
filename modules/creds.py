import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
from modules.search import get_artist_top_tracks


sp = None

def authenticate_client(client_id:str, client_secret:str):
    #client_id = e18a33b810214ef997ebd806aaf48f0e
    #client_secret = a69ff972d459452987b5d7094d923eaf

    try:
        client_credential_manager = SpotifyClientCredentials(
            client_id = client_id,
            client_secret = client_secret
        )   
        sp = spotipy.Spotify(auth_manager=client_credential_manager)

        results = sp.search(q="some query", type="track")
        if results['tracks']['items']:
            st.session_state.client_id = True
            st.session_state.client_secret = True
            st.success("Valid User Credentials")
            return True
        else:
            st.warning("No tracks found for the query.")
            return False

    except Exception as e:
        st.error(f"{e}")
        return False
    

def create_sp_session(client_id, client_secret):
    try:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
        ))
        if sp:
            st.session_state.login = True
            st.session_state.sp_session = sp
            return sp
    except spotipy.client.SpotifyException as e:
        st.error(f"error validating credentials:", e)


def validate_session(sp):
    results = sp.me
    return results


@st.dialog("login:")
def render_login():

    st.session_state["dialogue_open"] = True

    st.title("enter you client_id and client_secret")
    with st.form("enter your Spotify credentials"):
        st.session_state["client_id"] = st.text_input("e18a33b810214ef997ebd806aaf48f0e")
        st.session_state["client_secret"] = st.text_input("a69ff972d459452987b5d7094d923eaf")

        submitted = st.form_submit_button("submit creds")

        # try:
        #     if submitted:
        #         # sp = create_sp_session(client_id=client_id, client_secret=client_secret)
        #         st.session_state.dialogue_open = False
        #         st.session_state.login = True
        #         st.rerun()
        # except:
        #     st.error("please enter valid credentials")
    if submitted:
        try:
            # sp = create_sp_session(client_id=st.session_state["client_id"],
                                    # client_secret=st.session_state["client_secret"])
            st.session_state.dialogue_open = False
            st.session_state.login = True
            st.rerun()
        except spotipy.client.SpotifyException as e:
            st.error("Error validating credentials:", str(e))


