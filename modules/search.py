import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import requests

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


def get_artist_top_tracks(sp, band:str, limit=3):


    """Summary

    Args:
        sp (_type_): _description_
        band (str): _description_
        limit (int, optional): _description_. Defaults to 3.

    Returns:
        _type_: _description_
    """
    
    results = sp.search(q=f'artist:{band}', type='track', limit=limit)
    st.session_state["tracks"] = [] 
    for idx, item in enumerate(results['tracks']['items']):
        track = sp.track(item['id'])
        features = sp.audio_features([item['id']])
        st.session_state["tracks"].append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'features': features[0]
        })
    return st.session_state["tracks"]

