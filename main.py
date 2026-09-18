"""Data Viewer — Streamlit entry point."""

import streamlit as st

from app.state import init_state
from app.ui.filters import render_filters
from app.ui.grid import render_grid
from app.ui.insights import render_insights
from app.ui.sidebar import render_sidebar
from app.ui.summary import render_summary
from app.view_query import apply_view_query

st.set_page_config(
    page_title="Data Viewer",
    layout="wide",
)

init_state()
render_sidebar()

st.title("Data Viewer")

if st.session_state.df is None:
    render_grid()
else:
    # Sync sort from widget keys so apply_view_query sees the latest choice
    # on the same run the user changes the selectbox/radio.
    sort_col = st.session_state.get("sort_column_select", "(none)")
    sort_dir = st.session_state.get("sort_direction", "Ascending")
    if sort_col and sort_col != "(none)":
        st.session_state.view_sort = [
            {"column": sort_col, "ascending": sort_dir == "Ascending"}
        ]
    elif "sort_column_select" in st.session_state:
        st.session_state.view_sort = []

    df_view, query_warnings = apply_view_query(
        st.session_state.df,
        st.session_state.view_filters,
        st.session_state.view_sort,
    )
    for message in query_warnings:
        st.warning(message)

    render_summary(df_view)
    render_insights(df_view)
    render_filters(st.session_state.df)
    render_grid(df_view, total_rows=len(st.session_state.df))
