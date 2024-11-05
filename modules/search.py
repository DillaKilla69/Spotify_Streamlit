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
    tracks = [] 
    for idx, item in enumerate(results['tracks']['items']):
        track = sp.track(item['id'])
        features = sp.audio_features([item['id']])
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'features': features[0]
        })
    return tracks


def test_response(artist_name, sp, limit=10):
    try:
        response = requests.get(f"https://api.spotify.com/v1/search?q=artist:{artist_name}&type=track&limit={limit}", headers={'Authorization': f'Bearer {sp}'})
        print(f"HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return []

# def get_albums(sp, artist_name):