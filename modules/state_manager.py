import streamlit as st


def create_app_state():

    # Ensure session state variables exist
    if "project_setup" not in st.session_state:
        st.session_state["project_setup"] = False

    if "show_login_dialog" not in st.session_state:
        st.session_state["show_login_dialog"] = False

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "trigger_rerun" not in st.session_state:
        st.session_state["trigger_rerun"] = False  # New flag to control rerun timing

    if "poetry_setup" not in st.session_state:
        st.session_state["poetry_setup"] = False

    if "client_id" not in st.session_state:
        st.session_state["client_id"] = st.secrets["clientId"]

    if "client_secret" not in st.session_state:
        st.session_state["client_secret"] = st.secrets["clientSecret"]

    if "sp_session" not in st.session_state:
        st.session_state["sp_session"] = None

    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None

    if "sidebar_input" not in st.session_state:
        st.session_state["sidebar_input"] = []

    if "albums" not in st.session_state:
        st.session_state["albums"] = []

    if "followers" not in st.session_state:
        st.session_state["followers"] = []

    if "popularity" not in st.session_state:
        st.session_state["popularity"] = []
