import altair as alt
import pandas as pd
import streamlit as st


def get_artist_id(sp, artist_name):
    """Search for an exact artist match and return their Spotify ID."""
    results = sp.search(q=f'artist:"{artist_name}"', type="artist", limit=10)

    for artist in results["artists"]["items"]:
        if artist["name"].lower() == artist_name.lower():  # Exact match check
            return artist["id"]
    return None  # Return None if no exact match found


def search_albums(sp, artist_name, types=None):
    # Search for all data associated with search term and data type

    album_list = st.session_state["albums"]
    album_list = []
    artist_id = get_artist_id(sp, artist_name)

    if not artist_id:
        return f"No exact match found for '{artist_name}'"

    albums = sp.artist_albums(artist_id, album_type="album", include_groups=f"{types}")
    # Expose data within the returned JSON
    album_list = [
        {
            "Title": album["name"],
            "Album Type": album["album_type"],  # Access album type
            "Release Date": album["release_date"],
            "Total Tracks": album["total_tracks"],
        }
        for album in albums["items"]
    ]

    # Sort the album list by release_date in ascending order
    album_sorted_df = pd.DataFrame(album_list).sort_values(
        by="Release Date", ascending=True
    )

    return album_sorted_df if isinstance(album_sorted_df, pd.DataFrame) else None


def top_tracks(sp, band):

    # empty session state after every rerun
    # track_list = st.session_state["tracks"]
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
                "Release Date": release_date,
            }
        )

    sorted_tracks_df = pd.DataFrame(track_list).sort_values(
        by="Popularity", ascending=False
    )

    st.subheader(f"{band} top tracks")
    st.dataframe(sorted_tracks_df, hide_index=True)

    # Ensure 'Release Date' is in datetime format
    sorted_tracks_df["Release Date"] = pd.to_datetime(
        sorted_tracks_df["Release Date"], errors="coerce"
    )

    return sorted_tracks_df


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


def get_artist(sp, band):
    id = get_artist_id(sp, band)
    artist = sp.artist(id)
    return artist
