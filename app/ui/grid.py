"""Main grid: empty state, metadata, and dataframe display."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_grid() -> None:
    df = st.session_state.df

    if df is None:
        st.info(
            "Upload a CSV or Excel file from the sidebar, or click **Load sample** "
            "to explore the included demo dataset."
        )
        return

    name = st.session_state.source_name or "Untitled"
    rows, cols = df.shape
    st.caption(f"{name} · {rows:,} rows × {cols:,} columns")

    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("Column types"):
        dtype_table = pd.DataFrame(
            {
                "column": df.columns.astype(str),
                "dtype": df.dtypes.astype(str).values,
            }
        )
        st.dataframe(dtype_table, use_container_width=True, hide_index=True)
