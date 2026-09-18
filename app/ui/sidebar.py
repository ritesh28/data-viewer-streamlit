"""Sidebar: upload, sample load, clear, and downloads."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.io import (
    DataLoadError,
    dataframe_to_csv_bytes,
    dataframe_to_excel_bytes,
    export_filename,
    load_sample,
    load_uploaded_file,
)
from app.state import clear_data, set_dataframe

SAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "Sample_Data_for_Plotting_and_Filtering.csv"
)


def _upload_fingerprint(uploaded_file) -> str:
    return f"{uploaded_file.name}:{uploaded_file.size}"


def _handle_upload(uploaded_file) -> None:
    # Only re-parse when the uploaded file identity changes (Streamlit re-runs
    # the script on every interaction, so the same UploadedFile would otherwise
    # be loaded repeatedly).
    fingerprint = _upload_fingerprint(uploaded_file)
    if fingerprint == st.session_state.upload_fingerprint:
        return

    try:
        df, source_type = load_uploaded_file(uploaded_file)
    except DataLoadError as exc:
        st.error(str(exc))
        return

    set_dataframe(df, source_name=uploaded_file.name, source_type=source_type)
    st.session_state.upload_fingerprint = fingerprint
    st.success(f"Loaded {uploaded_file.name}")


def _handle_sample() -> None:
    try:
        df = load_sample(SAMPLE_PATH)
    except DataLoadError as exc:
        st.error(str(exc))
        return

    set_dataframe(
        df,
        source_name=SAMPLE_PATH.name,
        source_type="csv",
    )
    st.session_state.upload_fingerprint = None
    st.success(f"Loaded sample: {SAMPLE_PATH.name}")


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Data")

        uploaded_file = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx"],
            help="Supported formats: .csv, .xlsx",
        )
        if uploaded_file is not None:
            _handle_upload(uploaded_file)

        if st.button("Load sample", use_container_width=True):
            _handle_sample()

        st.divider()

        df = st.session_state.df
        if df is not None:
            st.subheader("Download")
            source_name = st.session_state.source_name
            st.download_button(
                label="Download CSV",
                data=dataframe_to_csv_bytes(df),
                file_name=export_filename(source_name, "csv"),
                mime="text/csv",
                use_container_width=True,
            )
            st.download_button(
                label="Download Excel",
                data=dataframe_to_excel_bytes(df),
                file_name=export_filename(source_name, "xlsx"),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            st.divider()
            if st.button("Clear data", use_container_width=True, type="secondary"):
                clear_data()
                st.rerun()
