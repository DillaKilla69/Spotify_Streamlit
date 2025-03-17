import pandas as pd
import streamlit as st

from modules.creds import create_sp_session
from modules.etl import (
    album_type_distro,
    album_type_over_time,
    format_number,
    track_popularity,
)
from modules.search import artist_genres, get_artist, search_albums, top_tracks, get_all_albums
from modules.state_manager import create_app_state
from modules.tickets import get_events
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
                label="Albums/Singles",
                value=len(get_all_albums(sp, artist_name=sidebar_input)),
            )
            col4.metric(
                label="Popularity",
                value=(get_artist(sp, sidebar_input))["popularity"],
            )

            with st.expander("top tracks", expanded=False):
                tracks = top_tracks(sp, sidebar_input)
            with st.expander("albums"):
                albums = get_all_albums(sp, sidebar_input)
                st.write(albums)
            with st.expander("events"):
                get_events(st.session_state["ticketmaster"], sidebar_input)

        except Exception as e:
            st.write(e)

    elif st.session_state["selected_option"] == "Top Tracks":
        try:
            st.header(f"{sidebar_input} Track Analysis")
            with st.expander(f"{sidebar_input} Tracklist", expanded=True):
                tracks = top_tracks(sp, band=sidebar_input)
            with st.expander(f"{sidebar_input} Popularity"):
                st.header(f"{sidebar_input} Tracks by Popularity Over Time")
                track_popularity(tracks, sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving top tracks: {e}")

    elif st.session_state["selected_option"] == "Discography":
        try:
            st.header(f"{sidebar_input} Discography Analysis")
            with st.expander(f"{sidebar_input} Discography", expanded=True):
                # albums = search_albums(sp, sidebar_input, types="album,single")
                # st.subheader(f"{sidebar_input} albums")
                # st.dataframe(albums, hide_index=False)
                all_albums = get_all_albums(sp, artist_name=sidebar_input)
                st.write(all_albums)
            with st.expander(f"{sidebar_input} Release Timeline", expanded=False):
                album_type_distro(all_albums)
                album_type_over_time(all_albums)
        except Exception as e:
            st.error(f"🚨 Error retrieving discography: {e}")

    elif st.session_state["selected_option"] == "Artist Genres":
        try:
            band = get_artist(sp, band=sidebar_input)
            artist_genres(sp, band=sidebar_input)
        except Exception as e:
            st.error(f"🚨 Error retrieving artist genres: {e}")
