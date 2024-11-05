import streamlit as st
import pandas as pd
import plotly_express as px
import matplotlib.pyplot as plt

from modules.creds import render_login, create_sp_session
from modules.search import get_artist_top_tracks, test_response, get_band
from modules.state_manager import create_app_state
from modules.ploty_map import create_map


def main():
    
    create_app_state()

    if st.session_state["login"] == False:
        render_login()

    else:
        st.title("here we go!")

        with st.sidebar:
            
            band = st.text_input("enter band name")
            
            if st.button("submit query"):
                sp = st.session_state["sp_session"]
                tracks = get_artist_top_tracks(sp, band)

        try:
            tracks_df = pd.json_normalize(tracks)
            # create_map(tracks_df)
            st.table(tracks_df)
        except Exception as e:
            st.error(f"{e}")

if __name__ == "__main__":
    main()