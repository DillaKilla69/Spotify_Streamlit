import streamlit as st
import pandas as pd


def search_albums(sp, band: str, limit=20):

    # Search for all data associated with search term and data type
    results = sp.search(q=f'artist:{band}', type='album', limit=limit)

    # Empty session state after every rerun 
    album_list = st.session_state["albums"]
    album_list = []
    
    # Expose data within the returned JSON
    for item in results['albums']['items']:
        artist = item['artists'][0]['name']
        album = item['name']
        type = item['album_type']
        total_tracks = item['total_tracks']
        release_date = item['release_date']

        # Create dictionary to house result columns
        album_list.append({
            'Artist': artist,
            'Album': album,
            'Type': type,
            'total_tracks': total_tracks,
            'Release Date': release_date
        })

    # Sort the album list by release_date in ascending order
    album_list_sorted = sorted(album_list, key=lambda x: x['Release Date'])
    album_sorted_df = pd.json_normalize(album_list_sorted)
    st.header(f"{band} top tracks")
    st.write(album_sorted_df)

def top_tracks(sp, band):

    #empty session state after every rerun 
    track_list = st.session_state["tracks"]
    track_list = []

    #all results from search
    results_json = sp.search(q=f'artist:{band}', type='artist', limit=5)

    #isolate artist_id
    artist_id = results_json["artists"]['items'][0]['id']
    
    #given artist_id, search top tracks - return in json
    top_tracks_json = sp.artist_top_tracks(artist_id)

    # st.write(top_tracks_json)

#expose data within the returned JSON
    for tracks in top_tracks_json['tracks']:
        title = tracks['name']
        artist = ', '.join([artist['name'] for artist in tracks['artists']])
        album = tracks['album']['name']
        popularity = tracks['popularity']

        #create list of dictionaries to house result columns
        track_list.append({
            'Title': title,
            'Artist': artist,
            'Album': album,
            'Popularity': popularity
        })

    track_list = sorted(track_list, key=lambda x: x["Popularity"], reverse=True)
    sorted_tracks_df = pd.DataFrame(track_list)
    st.header(f"{band} top tracks") 
    st.write(sorted_tracks_df)

