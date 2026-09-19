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
    page_icon=":material/table_chart:",
    layout="wide",
)

init_state()
render_sidebar()

st.title("Data Viewer")

if st.session_state.df is None:
    render_grid()
else:
    # Sync sort from widget keys so apply_view_query sees the latest choice
    # on the same run the user changes the selectbox / segmented control.
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

    # Explore tools in a secondary panel; data grid stays visible beside them.
    explore_col, grid_col = st.columns([1, 2], gap="large")

    with explore_col:
        # Lazy-run tab bodies so Insights charts don't compute when hidden.
        summary_tab, insights_tab, filters_tab = st.tabs(
            [
                ":material/insights: Summary",
                ":material/bar_chart: Insights",
                ":material/filter_alt: Filters",
            ],
            on_change="rerun",
            key="explore_tabs",
        )
        if summary_tab.open:
            with summary_tab:
                render_summary(df_view)
        if insights_tab.open:
            with insights_tab:
                render_insights(df_view)
        if filters_tab.open:
            with filters_tab:
                render_filters(st.session_state.df)

    with grid_col:
        st.subheader("Data")
        render_grid(df_view, total_rows=len(st.session_state.df))
