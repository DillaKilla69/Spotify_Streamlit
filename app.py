import streamlit as st
from modules.creds import render_login, create_sp_session
from modules.search import get_artist_top_tracks, test_response, get_band
from modules.state_manager import create_app_state
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
from modules.creds import render_login, create_sp_session
from modules.search import get_artist_top_tracks, test_response
from modules.state_manager import create_app_state
import pandas as pd
import matplotlib.pyplot as plt

def main():
    
    create_app_state()

    if st.session_state["login"] == False:
        render_login()

    else:
        st.title("here we go!")

        with st.sidebar:
            
            band = st.text_input("enter band name")
            
            if st.button("submit query"):
                sp = st.session_state.get("sp_session")
                if sp is None:
                    try:
                        sp = create_sp_session(st.session_state["client_id"], st.session_state["client_secret"])
                        tracks = get_artist_top_tracks(sp, band)
                    except:
                        st.error("check credentials, bitch")
        try:
            tracks_df = pd.json_normalize(tracks)
            st.table(tracks_df)
        except Exception as e:
            st.error(f"{e}")

if __name__ == "__main__":
    main()