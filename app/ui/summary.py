"""Data Summary panel for View mode."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.stats import column_summary, dataset_summary

ENTIRE_DATASET = "(Entire dataset)"


def _format_number(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    if isinstance(value, float):
        return f"{value:,.4g}"
    if isinstance(value, (int,)):
        return f"{value:,}"
    return str(value)


def render_summary(df_view: pd.DataFrame) -> None:
    """Render dataset or column summary. Stats are computed on df_view."""
    columns = [ENTIRE_DATASET, *[str(c) for c in df_view.columns]]
    current = st.session_state.selected_column
    index = 0
    if current is not None and str(current) in columns:
        index = columns.index(str(current))

    choice = st.selectbox("Focus", options=columns, index=index, key="summary_focus")
    st.session_state.selected_column = None if choice == ENTIRE_DATASET else choice

    selected = st.session_state.selected_column
    if selected is None:
        summary = dataset_summary(df_view)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{summary['rows']:,}")
        c2.metric("Columns", f"{summary['columns']:,}")
        c3.metric("Missing cells", f"{summary['missing_cells']:,}")
        c4.metric("Duplicate rows", f"{summary['duplicate_rows']:,}")
        counts = summary["dtype_counts"]
        st.caption(
            f"Column types — numeric: {counts['numeric']}, "
            f"datetime: {counts['datetime']}, other: {counts['other']}"
        )
        return

    if selected not in df_view.columns:
        st.warning(f"Column '{selected}' is not in the current view.")
        return

    summary = column_summary(df_view[selected])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Count", f"{summary['count']:,}")
    c2.metric("Missing", f"{summary['missing']:,} ({summary['missing_pct']:.1f}%)")
    c3.metric("Distinct", f"{summary['distinct']:,}")
    c4.metric("Non-null", f"{summary['non_null']:,}")

    if summary["kind"] == "numeric":
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mean", _format_number(summary.get("mean")))
        m2.metric("Median", _format_number(summary.get("median")))
        m3.metric("Min", _format_number(summary.get("min")))
        m4.metric("Max", _format_number(summary.get("max")))
        st.caption(
            f"Std: {_format_number(summary.get('std'))} · "
            f"Q25: {_format_number(summary.get('q25'))} · "
            f"Q75: {_format_number(summary.get('q75'))}"
        )
    elif summary["kind"] == "datetime":
        st.caption(
            f"Range: {_format_number(summary.get('min'))} → {_format_number(summary.get('max'))}"
        )
    else:
        top = summary.get("top_values") or []
        if top:
            top_df = pd.DataFrame(top)
            st.caption(
                f"Avg string length: {_format_number(summary.get('avg_str_length'))}"
            )
            st.dataframe(top_df, hide_index=True, key="top_values_grid")
