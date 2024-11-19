import streamlit as st
import pandas as pd
from modules.search import get_artist_top_tracks
from modules.creds import render_login


if st.session_state["login"] == False:
    render_login()

with st.sidebar:
        
    band = st.text_input("enter band name")
    
    if st.button("submit query"):
        sp = st.session_state["sp_session"]
        tracks = get_artist_top_tracks(sp, band)

try:    
    tracks_df = pd.json_normalize(tracks)
    # create_map(tracks_df)
    st.header(f"{band} top tracks") 
    st.table(tracks_df)
except:
    st.info("please use the sidebar to query an artist")