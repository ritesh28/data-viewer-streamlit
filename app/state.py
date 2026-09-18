"""Session state defaults and helpers."""

from __future__ import annotations

import streamlit as st

DEFAULTS: dict = {
    "df_raw": None,
    "df": None,
    "source_name": None,
    "source_type": None,
    "mode": "view",
    "cleaning_steps": [],
    "selected_column": None,
    "view_filters": [],
    "view_sort": [],
    # Tracks last successfully loaded upload so we only re-parse on change.
    "upload_fingerprint": None,
    "filter_id_counter": 0,
}


def _copy_default(value):
    return value.copy() if isinstance(value, list) else value


def init_state() -> None:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = _copy_default(value)


def clear_data() -> None:
    for key, value in DEFAULTS.items():
        st.session_state[key] = _copy_default(value)


def set_dataframe(df, *, source_name: str, source_type: str) -> None:
    """Store a newly loaded dataframe as both raw and working copies."""
    st.session_state.df_raw = df.copy()
    st.session_state.df = df.copy()
    st.session_state.source_name = source_name
    st.session_state.source_type = source_type
    st.session_state.cleaning_steps = []
    st.session_state.selected_column = None
    st.session_state.view_filters = []
    st.session_state.view_sort = []
    st.session_state.filter_id_counter = 0


def next_filter_id() -> str:
    st.session_state.filter_id_counter += 1
    return f"f{st.session_state.filter_id_counter}"
