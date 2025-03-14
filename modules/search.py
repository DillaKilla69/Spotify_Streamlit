import pandas as pd
import streamlit as st
import altair as alt


def search_albums(sp, band: str, limit=50):

    # Search for all data associated with search term and data type
    results = sp.search(q=f"artist:{band}", type="album", limit=limit)
    # Empty session state after every rerun
    album_list = st.session_state["albums"]
    album_list = []

    # Expose data within the returned JSON
    for item in results["albums"]["items"]:
        artist = item["artists"][0]["name"]
        album = item["name"]
        type = item["album_type"]
        total_tracks = item["total_tracks"]
        release_date = item["release_date"]

        # Create dictionary to house result columns
        album_list.append(
            {
                "Artist": artist,
                "Album": album,
                "Type": type,
                "Total Tracks": total_tracks,
                "Release Date": release_date,
            }
        )

    # Sort the album list by release_date in ascending order
    album_sorted_df = pd.DataFrame(album_list).sort_values(
        by="Release Date", ascending=True
    )

    st.header(f"{band} Discography")
    st.dataframe(album_sorted_df, hide_index=True)


def top_tracks(sp, band):

    # empty session state after every rerun
    track_list = st.session_state["tracks"]
    track_list = []

    # all results from search
    results_json = sp.search(q=f"artist:{band}", type="artist", limit=20)

    # isolate artist_id
    artist_id = results_json["artists"]["items"][0]["id"]

    # given artist_id, search top tracks - return in json
    top_tracks_json = sp.artist_top_tracks(artist_id)

    # expose data within the returned JSON
    for tracks in top_tracks_json["tracks"]:
        title = tracks["name"]
        artist = ", ".join([artist["name"] for artist in tracks["artists"]])
        album = tracks["album"]["name"]
        popularity = tracks["popularity"]
        release_date = tracks["album"]["release_date"]

        # create list of dictionaries to house result columns
        track_list.append(
            {
                "Title": title,
                "Album": album,
                "Popularity": popularity,
                "Release Date": release_date
            }
        )

    sorted_tracks_df = pd.DataFrame(track_list).sort_values(
        by="Popularity", ascending=False
    )

    st.header(f"{band} top tracks")
    st.dataframe(sorted_tracks_df, hide_index=True)

    # Ensure 'Release Date' is in datetime format
    sorted_tracks_df["Release Date"] = pd.to_datetime(
        sorted_tracks_df["Release Date"],
        errors='coerce'

    )   

    # Get the min and max Popularity values
    min_popularity = sorted_tracks_df["Popularity"].min()
    max_popularity = sorted_tracks_df["Popularity"].max()

    chart = (
        alt.Chart(sorted_tracks_df)
        .mark_line(point=True, smooth=True)
        .encode(
            x=alt.X(
                "Release Date:T", 
                title="Release Date",
                timeUnit='yearmonth'),
            y=alt.Y(
                "Popularity:Q",
                title="Popularity",
                scale=alt.Scale(
                    domain=[min_popularity, max_popularity]
                ), 
            ),
            tooltip=list(sorted_tracks_df.columns),
        )
        .properties(title=f"{band} Track Popularity by Release Date")
    )

    st.altair_chart(chart, use_container_width=True)


def artist_genres(sp, band):
    # empty session state after every rerun
    genres = st.session_state["genres"]
    genres = []

    # all results from search
    results_json = sp.search(q=f"artist:{band}", type="artist", limit=50)

    for item in results_json["artists"]["items"]:
        artist = item["name"]
        genre = item["genres"] if item["genres"] else ["No data provided"]
        if not genre:
            genre = "no data provided"

        genres.append({"artist": artist, "genre": genre})

    genres_table = pd.json_normalize(genres)
    st.write(genres_table)
