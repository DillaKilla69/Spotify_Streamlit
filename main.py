import streamlit as st
import streamlit.components.v1 as components

from modules.creds import render_login
from modules.state_manager import create_app_state


def main():
    
    create_app_state()

    if st.session_state["login"] == False:
        render_login()


    else:
        st.title("Exploring Music with Spotipy")

    # URL of the webpage you want to embed
    url = "https://spotipy.readthedocs.io/en/2.24.0/"

    # Display the webpage using an iframe
    components.html(
        f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>',
        height=600,
)

if __name__ == "__main__":
    main()