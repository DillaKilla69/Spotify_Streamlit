import os
import subprocess
import sys
import time

import streamlit as st


def run_command(command):
    """Runs a shell command and returns the output as a string."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()


@st.dialog("🔧 Setting Up Your Environment", width="large")
def setup_environment():
    """Ensures Poetry is installed, sets up the virtual environment, and restarts inside it."""

    while st.session_state["project_setup"] == False:
        st.write("Please wait while we check your setup...")

        with st.status("Checking Poetry installation...", expanded=True) as status:
            poetry_version = run_command(["poetry", "--version"])
            if "Poetry" in poetry_version:
                st.info(f"✅ Poetry is installed: {poetry_version}")
            else:
                st.warning("⚠️ Poetry not found. Installing...")
                install_output = run_command(
                    [sys.executable, "-m", "pip", "install", "--user", "poetry"]
                )
                st.write(install_output)
                st.success("✅ Poetry installed successfully.")

        with st.status(
            "Setting up the project environment...", expanded=True
        ) as status:
            install_output = run_command(["poetry", "install"])
            st.info(install_output)
            st.success("✅ Environment setup complete. You are being directed to login")

        poetry_env_path = run_command(["poetry", "env", "info", "--path"])
        poetry_python = (
            os.path.join(poetry_env_path, "bin", "python")
            if sys.platform != "win32"
            else os.path.join(poetry_env_path, "Scripts", "python.exe")
        )

        if sys.executable != poetry_python:
            st.warning("🔄 Restarting in Poetry virtual environment...")
            subprocess.run(
                [poetry_python, "-m", "streamlit", "run", sys.argv[0]], check=True
            )
            sys.exit()  # Stop the current process

        # ✅ Mark setup as complete
        st.session_state["project_setup"] = True
        st.session_state["trigger_rerun"] = True
        st.session_state["poetry_setup"] = True

    time.sleep(5)
    st.rerun()
