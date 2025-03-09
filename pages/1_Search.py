import pandas as pd
import streamlit as st

from modules.creds import render_login
from modules.search import get_artist_top_tracks, search_albums
from modules.state_manager import create_app_state


def main():

    create_app_state()

    if st.session_state["login"] == False:
        render_login()

    options = ["tracks", "album", "shows"]

    selected_option = st.sidebar.selectbox("Choose a search type:", options)

    sidebar_input = st.sidebar.text_input("Search Spotify for artist tracks:")

    if st.sidebar.button("submit query"):
        #if "tracks" selected
        if selected_option == "tracks":
            tracks = get_artist_top_tracks(st.session_state["sp_session"], band=sidebar_input)
            tracks_df = pd.json_normalize(tracks)
            st.header(f"{sidebar_input} top tracks") 
            st.table(tracks_df)
            




        if selected_option == "album":
            albums = search_albums(
                st.session_state["sp_session"],
                album=sidebar_input
            )
            albums_df = pd.json_normalize(albums)
            st.header(f"{sidebar_input} Album Results") 
            st.table(albums_df)

if __name__ == "__main__":
    main()