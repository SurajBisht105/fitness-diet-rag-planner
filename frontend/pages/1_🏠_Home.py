# frontend/pages/1_🏠_Home.py
"""Home Page - Redirects to main app."""

import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Simply redirect to main app
st.switch_page("app.py")