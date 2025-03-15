import streamlit as st
import streamlit.components.v1 as components

from modules.state_manager import create_app_state
from modules.creds import create_sp_session
import time
create_app_state()

create_sp_session(st.session_state["client_id"], st.session_state["client_secret"])

st.switch_page('pages/1_Search.py')

if st.session_state["client_id"] is not None:
    st.title("Using Spotipy to Interact with Spofify API")
    st.caption("Docs from Spotipy...")

    url = "https://spotipy.readthedocs.io/en/2.24.0/"
    components.html(
        f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>',
        height=600,
    )
