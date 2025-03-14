import streamlit as st

from modules.creds import render_login
from modules.search import artist_genres, search_albums, top_tracks

if st.session_state["logged_in"] == False:
    render_login()

else:

    options = ["Top Tracks", "Discography", "Shows", "Artist Genres"]

    st.sidebar.header("Search Parameters")
    selected_option = st.sidebar.selectbox(
        "Choose a search type:", options=options, index=None
    )

    if selected_option == "Top Tracks":
        sidebar_input = st.sidebar.text_input("Retreive Artist Top Tracks:")
        if st.sidebar.button("submit query"):
            top_tracks(st.session_state["sp_session"], band=sidebar_input)

    if selected_option == "Discography":
        sidebar_input = st.sidebar.text_input("Search for Artist Discography:")
        if st.sidebar.button("submit query"):
            search_albums(st.session_state["sp_session"], band=sidebar_input)

    if selected_option == "Artist Genres":
        sidebar_input = st.sidebar.text_input("Search for Artist Genres:")
        if st.sidebar.button("submit query"):
            artist_genres(st.session_state["sp_session"], band=sidebar_input)
