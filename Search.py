import pandas as pd
import streamlit as st

from modules.creds import create_sp_session
from modules.etl import (
    album_type_distro,
    album_type_over_time,
    format_number,
    track_popularity,
)
from modules.search import artist_genres, get_artist, search_albums, top_tracks
from modules.state_manager import create_app_state

create_app_state()

sp = create_sp_session(st.session_state["client_id"], st.session_state["client_secret"])

sidebar_input = st.session_state["sidebar_input"]
options = ["Artist Profile", "Top Tracks", "Discography"]
st.sidebar.header("Search Parameters")

with st.sidebar.form("enter_params", enter_to_submit=True, border=False):
    st.session_state["selected_option"] = st.selectbox(
        "Choose a search type:", options=options, index=None
    )
    sidebar_input = st.text_input("Enter Artist Name:")
    submit_query = st.form_submit_button(
        "Submit Query"
    )  # One submit button for all options

if st.session_state["selected_option"] is None:
    st.info(
        "Tap or click the sidebar to get started! \n\n(On mobile, tap the arrow in the top-left!)"
    )

if submit_query:
    if st.session_state["selected_option"] == "Artist Profile":

        try:
            st.header(f"{sidebar_input}'s Profile")

            col1, col2, col3, col4 = st.columns(4)

            num_albums = len(st.session_state["albums"])
            num_followers = get_artist(sp, sidebar_input)["followers"]["total"]

            col1.image(get_artist(sp, sidebar_input)["images"][2]["url"])
            col2.metric(label="Followers", value=format_number(num_followers))
            col3.metric(
                label="Albums",
                value=len(search_albums(sp, sidebar_input, types="album")),
            )
            col4.metric(
                label="Popularity",
                value=(get_artist(sp))["popularity"],
            )

            with st.expander("top tracks", expanded=True):
                tracks = top_tracks(sp, sidebar_input)
            with st.expander("albums"):
                albums = search_albums(sp, sidebar_input, types="album,single")
                st.write(albums)

        except Exception as e:
            st.write(e)

    elif st.session_state["selected_option"] == "Top Tracks":
        try:
            st.header(f"{sidebar_input} Track Analysis")
            with st.expander("Tracklist", expanded=True):
                tracks = top_tracks(sp, band=sidebar_input)
            with st.expander("Popularity"):
                st.header(f"{sidebar_input} Tracks by Popularity Over Time")
                track_popularity(tracks, sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving top tracks: {e}")

    elif st.session_state["selected_option"] == "Discography":
        try:
            st.header(f"{sidebar_input} Discography Analysis")
            with st.expander("Discography", expanded=True):
                albums = search_albums(sp, sidebar_input, types="album, single")
                st.subheader(f"{sidebar_input} albums")
                st.dataframe(albums, hide_index=True)
            with st.expander("album distribution", expanded=False):
                album_type_distro(albums)
                album_type_over_time(albums)
        except Exception as e:
            st.error(f"🚨 Error retrieving discography: {e}")

    elif st.session_state["selected_option"] == "Artist Genres":
        try:
            artist_genres(sp, band=sidebar_input)
            get_artist(sp, sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving artist genres: {e}")
