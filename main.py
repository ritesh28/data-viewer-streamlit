"""Data Viewer — Streamlit entry point (Milestone 01 skeleton)."""

import streamlit as st

from app.state import init_state
from app.ui.grid import render_grid
from app.ui.sidebar import render_sidebar

st.set_page_config(
    page_title="Data Viewer",
    layout="wide",
)

init_state()
render_sidebar()

st.title("Data Viewer")
render_grid()
