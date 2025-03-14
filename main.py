import streamlit as st
import streamlit.components.v1 as components

from modules.creds import render_login
from modules.setup import setup_environment
from modules.state_manager import create_app_state

try:
    if "project_setup" not in st.session_state:
        create_app_state()

    else:
        while st.session_state["logged_in"] == False:
            render_login()

        if st.session_state["logged_in"] == True:
            st.title("Exploring Music with Spotipy")

            url = "https://spotipy.readthedocs.io/en/2.24.0/"
            components.html(
                f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>',
                height=600,
            )

except Exception as e:
    pass
