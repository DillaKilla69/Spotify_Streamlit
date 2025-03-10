import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
from modules.creds import render_login
from modules.search import top_tracks, search_albums
from modules.state_manager import create_app_state


def main():

    create_app_state()

    if st.session_state["login"] == False:
        render_login()

    options = ["tracks", "albums", "shows"]

    selected_option = st.sidebar.selectbox("Choose a search type:", options)

    if selected_option == "tracks":
        sidebar_input = st.sidebar.text_input("Search for Aritst top tracks:")
        if st.sidebar.button("submit query"):
            top_tracks(
                st.session_state["sp_session"], 
                band=sidebar_input
                )


    if selected_option == "albums":
        sidebar_input = st.sidebar.text_input("Search for Aritst Discography:")
        if st.sidebar.button("submit query"):
            search_albums(
                st.session_state["sp_session"], 
                band=sidebar_input
                )


if __name__ == "__main__":
    main()




