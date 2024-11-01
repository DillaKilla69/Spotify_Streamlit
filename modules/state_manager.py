import streamlit as st

def create_app_state():

    if "login" not in st.session_state:
        st.session_state["login"] = False

    if "dialogue_open" not in st.session_state:
        st.session_state["dialogue_open"] = False

    if "client_id" not in st.session_state:
        st.session_state["client_id"] = False

    if "client_secret" not in st.session_state:
        st.session_state["client_secret"] = False

    if "sp_session" not in st.session_state:
        st.session_state["sp_session"] = None

    if "band" not in st.session_state:
        st.session_state["band"] = None

    if "tracks" not in st.session_state:
        st.session_state["tracks"] = None
