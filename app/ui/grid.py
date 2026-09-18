"""Main grid: empty state, metadata, and dataframe display."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_grid(df_view: pd.DataFrame | None = None, *, total_rows: int | None = None) -> None:
    df = st.session_state.df

    if df is None:
        st.info(
            "Upload a CSV or Excel file from the sidebar, or click **Load sample** "
            "to explore the included demo dataset."
        )
        return

    display = df if df_view is None else df_view
    name = st.session_state.source_name or "Untitled"
    shown_rows, cols = display.shape
    total = len(df) if total_rows is None else total_rows

    filters_active = bool(st.session_state.view_filters) or bool(st.session_state.view_sort)
    if filters_active or shown_rows != total:
        st.caption(f"{name} · {shown_rows:,} of {total:,} rows × {cols:,} columns")
    else:
        st.caption(f"{name} · {shown_rows:,} rows × {cols:,} columns")

    st.dataframe(display, use_container_width=True, hide_index=True)

    with st.expander("Column types"):
        dtype_table = pd.DataFrame(
            {
                "column": df.columns.astype(str),
                "dtype": df.dtypes.astype(str).values,
            }
        )
        st.dataframe(dtype_table, use_container_width=True, hide_index=True)
