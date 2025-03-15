import streamlit as st

# from modules.state_manager import create_app_state

from modules.etl import album_type_distro, track_popularity, album_type_over_time
from modules.search import artist_genres, search_albums, top_tracks



sidebar_input = st.session_state["sidebar_input"]
options = ["Top Tracks", "Discography", "Artist Genres"]
st.sidebar.header("Search Parameters")

with st.sidebar.form("enter_params"):
    st.session_state["selected_option"] = st.selectbox(
    "Choose a search type:", options=options, index=None
)
    sidebar_input = st.text_input("Enter Artist Name:")
    submit_query = st.form_submit_button("Submit Query")  # One submit button for all options

if st.session_state["selected_option"] is None:
    st.info('Use the search box to get started!')
if submit_query:
    if st.session_state["selected_option"] == "Top Tracks":
        try:
            with st.expander("Tracklist", expanded=True):
                tracks = top_tracks(st.session_state["sp_session"], band=sidebar_input)
            with st.expander("Popularity"):
                st.header(f"{sidebar_input} Tracks by Popularity Over Time")
                track_popularity(tracks, sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving top tracks: {e}")

    elif st.session_state["selected_option"] == "Discography":
        try:
            albums = search_albums(st.session_state["sp_session"], sidebar_input)
            st.header(f'{sidebar_input} Album Type Distribution')
            album_type_distro(albums)
            album_type_over_time(albums)
        except Exception as e:
            st.error(f"🚨 Error retrieving discography: {e}")

    elif st.session_state["selected_option"] == "Artist Genres":
        try:
            artist_genres(st.session_state["sp_session"], band=sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving artist genres: {e}")