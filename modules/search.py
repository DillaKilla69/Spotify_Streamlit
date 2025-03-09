import requests
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials


def get_band():
    """_summary_

    Returns:
        _type_: _description_
    """
    with st.sidebar:
        band = st.text_input("enter band name",help="press enter!")
        if band:
            st.session_state.band = band
            st.write(band)

            return band


def get_artist_top_tracks(sp, band:str, limit=10):


    """Summary

    Args:
        sp (_type_): _description_
        band (str): _description_
        limit (int, optional): _description_. Defaults to 3.

    Returns:
        _type_: _description_
    """
    # Search for all data associated with search term and data type
    results = sp.search(q=f'artist:{band}', type='track', limit=limit)

    #empty session state after every rerun 
    st.session_state["tracks"] = [] 

    #expose data within the returned JSON
    for item in results['tracks']['items']:
        track = item['name']

        #create dictionary to house result columns
        st.session_state["tracks"].append({
            'Name': track,
            'Artist': item['artists'][0]['name'],
            'Album': item['album']['name'],
            'popularity': item['popularity']
        })

    return sorted(st.session_state["tracks"], key=lambda track: track.get("popularity", 0), reverse=True)


#Need further research... does changing 'type' to album aggregate songs by album?
#changes result of albums if line 58 is edited to 'artist:{album}'
def search_albums(sp, album:str, limit=10):
    # Search for all data associated with search term and data type
    results = sp.search(q=f'album:{album}', type='album', limit=limit)
    st.write(results)
    # st.write(q)

    #empty session state after every rerun 
    st.session_state["tracks"] = [] 

    #expose data within the returned JSON
    for item in results['albums']['items']:
        track = item['name']

        #create dictionary to house result columns
        st.session_state["tracks"].append({
            'Album': item['name'],
            'Artist': item['artists'][0]['name']
        })

    return st.session_state["tracks"]

